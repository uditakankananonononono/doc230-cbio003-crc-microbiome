import pandas as pd,numpy as np,json
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,roc_curve,brier_score_loss
from sklearn.model_selection import cross_val_score,StratifiedKFold
from scipy.stats import mannwhitneyu
m=pd.read_csv('/tmp/meta_all.tsv',sep='\t')
m=m[m.Study.str.contains('CRC')&m.Group.isin(['CTR','CRC'])].reset_index(drop=True)
f=pd.read_csv('/tmp/sp.tsv',sep='\t',index_col=0,quoting=3)
X=f[m.Sample_ID].T; X=X.div(X.sum(1),axis=0); y=(m.Group=='CRC').astype(int).values
st=m.Study.values; S=sorted(set(st)); R={}
def tf(A,kind):
    if kind=='log': return np.log10(A+1e-5)
    if kind=='raw': return A
    if kind=='pa': return (A>=1e-3).astype(float)
    if kind=='clr':
        L=np.log(A+1e-5); return L-L.mean(1,keepdims=True)
def loco(kind='log',within=False,k=None,feats=None):
    out={}; P=np.zeros(len(y))
    for s in S:
        te=st==s; tr=~te
        keep=(X[tr].max()>=1e-3).values if feats is None else feats
        A=tf(X.values[tr][:,keep],kind); B=tf(X.values[te][:,keep],kind)
        if within:
            def zs(M,lab):
                M=M.copy()
                for c in set(lab):
                    i=lab==c; M[i]=(M[i]-M[i].mean(0))/(M[i].std(0)+1e-9)
                return M
            A=zs(A,st[tr]); B=zs(B,st[te]); mu=0;sd=1
        else: mu,sd=A.mean(0),A.std(0)+1e-9
        c=LogisticRegression(penalty='l1',solver='liblinear',C=0.1,random_state=0).fit((A-mu)/sd,y[tr])
        if k:
            top=np.argsort(-np.abs(c.coef_[0]))[:k]
            c=LogisticRegression(penalty='l1',solver='liblinear',C=0.1,random_state=0).fit(((A-mu)/sd)[:,top],y[tr])
            p=c.predict_proba(((B-mu)/sd)[:,top])[:,1]
        else: p=c.predict_proba((B-mu)/sd)[:,1]
        P[te]=p; out[s]=roc_auc_score(y[te],p)
    return out,P
base,Pb=loco(); bm=np.median(list(base.values())); R['base_median']=bm
# dir3
ctr=(y==0); Xc=np.log10(X.values[ctr][:,(X[ctr].max()>=1e-3).values]+1e-5)
acc=cross_val_score(LogisticRegression(C=0.1,max_iter=300),(Xc-Xc.mean(0))/(Xc.std(0)+1e-9),st[ctr],cv=StratifiedKFold(5,shuffle=True,random_state=0)).mean()
maj=pd.Series(st[ctr]).value_counts(normalize=True).iloc[0]
z,_=loco(within=True)
R['dir3']=dict(study_from_controls_acc=round(acc,3),majority=round(maj,3),strong_cohort_signal=bool(acc>2*maj),loco_within_cohort_z={k:round(v,3) for k,v in z.items()},median_z=round(float(np.median(list(z.values()))),3),helps=bool(np.median(list(z.values()))-bm>=0.02))
# dir4
R['dir4']={}
for k in [5,10,20,50]:
    a,_=loco(k=k); R['dir4'][k]=dict(median=round(float(np.median(list(a.values()))),3),min=round(min(a.values()),3))
ok=[k for k in [5,10,20,50] if R['dir4'][k]['median']>=bm-0.02]; R['dir4']['smallest_k_within_0.02']=ok[0] if ok else None
# dir5
names=['Fusobacterium nucleatum','Parvimonas micra','Peptostreptococcus stomatis','Gemella morbillorum','Solobacterium moorei','Porphyromonas asaccharolytica']
R['dir5']={}
for n in names:
    gen,sp=n.split(); rows=[r for r in X.columns if sp in r and gen in r]
    if not rows: R['dir5'][n]='not found'; continue
    r=max(rows,key=lambda c:X[c].mean()); up=0; d={}
    for s in S:
        i=st==s; a=X.loc[i&(y==1),r]; b=X.loc[i&(y==0),r]
        p=mannwhitneyu(a,b).pvalue; sign=int(a.median()>b.median() or a.mean()>b.mean()); up+=sign; d[s]=dict(up=sign,p=round(p,4))
    R['dir5'][n]=dict(feature=r,cohorts_enriched_in_CRC=up,replicates=bool(up>=7),per_cohort=d)
# dir7
R['dir7']={}
for kind in ['log','raw','pa','clr']:
    a,_=loco(kind=kind); R['dir7'][kind]=dict(median=round(float(np.median(list(a.values()))),3),min=round(min(a.values()),3))
# dir8
R['dir8']={}
for s in S:
    i=st==s; fpr,tpr,_=roc_curve(y[i],Pb[i]); j=np.where(tpr>=0.9)[0][0]; R['dir8'][s]=dict(spec_at_90sens=round(float(1-fpr[j]),3),brier=round(brier_score_loss(y[i],Pb[i]),3))
R['dir8']['pooled_brier']=round(brier_score_loss(y,Pb),3)
# dir9
mm=m.copy(); mm['g']=(mm.Gender=='M').astype(float); cov=mm[['Age','g','BMI']].apply(pd.to_numeric,errors='coerce')
okc=cov.notna().all(1).values; R['dir9']={'n_complete':int(okc.sum()),'cohorts':{s:int((okc&(st==s)).sum()) for s in S}}
cs=[s for s in S if (okc&(st==s)).sum()>=40]; res={}
for s in cs:
    te=okc&(st==s); tr=okc&(st!=s)
    if len(set(y[te]))<2: continue
    C=cov.values; mu,sd=C[tr].mean(0),C[tr].std(0)
    pc=LogisticRegression(max_iter=500).fit((C[tr]-mu)/sd,y[tr]).predict_proba((C[te]-mu)/sd)[:,1]
    res[s]=dict(cov_only=round(roc_auc_score(y[te],pc),3),micro=round(roc_auc_score(y[te],Pb[te]),3))
R['dir9']['per_cohort']=res
if res:
    R['dir9']['median_cov']=round(float(np.median([v['cov_only'] for v in res.values()])),3); R['dir9']['median_micro']=round(float(np.median([v['micro'] for v in res.values()])),3)
    R['dir9']['gate_micro_adds_0.03']=bool(R['dir9']['median_micro']-R['dir9']['median_cov']>=0.03)
json.dump(R,open('results/dir3_9.json','w'),indent=1,default=float); print(json.dumps(R,indent=0,default=float)[:6000])
