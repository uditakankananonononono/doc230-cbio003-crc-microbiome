import pandas as pd,numpy as np,json
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
m=pd.read_csv('/tmp/meta_all.tsv',sep='\t')
m=m[m.Study.str.contains('CRC')&m.Group.isin(['CTR','CRC','ADA'])].reset_index(drop=True)
f=pd.read_csv('/tmp/sp.tsv',sep='\t',index_col=0,quoting=3)
X=f[m.Sample_ID].T; X=X.div(X.sum(1),axis=0); g=m.Group.values; st=m.Study.values
def fit(tr,pos):
    keep=(X.iloc[tr].max()>=1e-3).values; A=np.log10(X.values[tr][:,keep]+1e-5); mu,sd=A.mean(0),A.std(0)+1e-9
    c=LogisticRegression(penalty='l1',solver='liblinear',C=0.1,random_state=0).fit((A-mu)/sd,(g[tr]==pos).astype(int))
    return lambda i:c.predict_proba((np.log10(X.values[i][:,keep]+1e-5)-mu)/sd)[:,1]
AD=['AT-CRC','FR-CRC','IT-CRC','US-CRC-2']; R={'a':{},'b':{},'order':{}}
for s in AD:
    te=np.where(st==s)[0]; 
    tr=np.where((st!=s)&np.isin(st,AD)&np.isin(g,['CTR','ADA']))[0]
    p=fit(tr,'ADA')(te); k=g[te]!='CRC'; R['a'][s]=dict(auroc=round(roc_auc_score(g[te][k]=='ADA',p[k]),3),n_ada=int((g[te]=='ADA').sum()),n_ctr=int((g[te]=='CTR').sum()))
    tr2=np.where((st!=s)&np.isin(g,['CTR','CRC']))[0]; q=fit(tr2,'CRC')(te)
    R['b'][s]=round(roc_auc_score(g[te][k]=='ADA',q[k]),3)
    R['order'][s]={x:round(float(np.median(q[g[te]==x])),3) for x in ['CTR','ADA','CRC']}
a=[v['auroc'] for v in R['a'].values()]; b=list(R['b'].values())
R['summary']=dict(a_median=float(np.median(a)),a_gate=bool(np.median(a)>=0.65),b_median=float(np.median(b)),b_gate=bool(np.median(b)>=0.60))
json.dump(R,open('results/dir6.json','w'),indent=1); print(json.dumps(R))
