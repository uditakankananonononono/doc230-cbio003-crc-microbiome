import pandas as pd,numpy as np,json
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
m=pd.read_csv('/tmp/meta_all.tsv',sep='\t'); m=m[m.Study.str.contains('CRC')&m.Group.isin(['CTR','CRC'])]
sp=pd.read_csv('/tmp/sp.tsv',sep='\t',index_col=0,quoting=3)
K1=pd.read_csv('/tmp/kegg_meta.tsv',sep='\t',index_col=0,low_memory=False); K2=pd.read_csv('/tmp/kegg_ext.tsv',sep='\t',index_col=0,low_memory=False)
K=K1.join(K2.loc[:,[c for c in K2.columns if c not in K1.columns]],how='outer').fillna(0)
m=m[m.Sample_ID.isin(K.columns)&m.Sample_ID.isin(sp.columns)].reset_index(drop=True)
y=(m.Group=='CRC').astype(int).values; st=m.Study.values
def mk(M):
    X=M[m.Sample_ID].T.astype(float); return (X.div(X.sum(1),axis=0)).values
Xs=mk(sp); Xk=mk(K)
disc=['AT-CRC','CN-CRC','DE-CRC','FR-CRC','US-CRC']; ext=[s for s in sorted(set(st)) if s not in disc]
def run(X,tr,te,thr):
    keep=X[tr].max(0)>=thr; A=np.log10(X[tr][:,keep]+1e-5); mu,sd=A.mean(0),A.std(0)+1e-9
    c=LogisticRegression(penalty='l1',solver='liblinear',C=0.1,random_state=0).fit((A-mu)/sd,y[tr])
    return roc_auc_score(y[te],c.predict_proba((np.log10(X[te][:,keep]+1e-5)-mu)/sd)[:,1])
R={'cohort_n':{s:int((st==s).sum()) for s in sorted(set(st))},'a':{},'b':{}}
for s in disc:
    te=st==s; tr=np.isin(st,disc)&~te
    R['a'][s]=dict(species=round(run(Xs,tr,te,1e-3),3),kegg=round(run(Xk,tr,te,1e-4),3))
tr=np.isin(st,disc)
for s in ext:
    te=st==s; R['b'][s]=dict(species=round(run(Xs,tr,te,1e-3),3),kegg=round(run(Xk,tr,te,1e-4),3))
med=lambda d,k:float(np.median([v[k] for v in d.values()]))
S=dict(a_species=med(R['a'],'species'),a_kegg=med(R['a'],'kegg'),b_species=med(R['b'],'species'),b_kegg=med(R['b'],'kegg'))
S['function_better_gate']=bool(S['a_kegg']-S['a_species']>=0.02 and S['b_kegg']-S['b_species']>=0.02); R['summary']=S
json.dump(R,open('results/dir10.json','w'),indent=1); print(json.dumps(R))
