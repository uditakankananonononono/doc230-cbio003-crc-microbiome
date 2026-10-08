import pandas as pd,numpy as np,json,sys
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import RepeatedStratifiedKFold
m=pd.read_csv('/tmp/meta_all.tsv',sep='\t')
m=m[m.Study.str.contains('CRC')&m.Group.isin(['CTR','CRC'])].reset_index(drop=True)
f=pd.read_csv('/tmp/sp.tsv',sep='\t',index_col=0,quoting=3)
X=f[m.Sample_ID].T; X=X.div(X.sum(1),axis=0); y=(m.Group=='CRC').astype(int).values
def fit_pred(tr,te):
    keep=X.iloc[tr].max()>=1e-3
    A=np.log10(X.iloc[tr].loc[:,keep].values+1e-5); B=np.log10(X.iloc[te].loc[:,keep].values+1e-5)
    mu,sd=A.mean(0),A.std(0)+1e-9
    c=LogisticRegression(penalty='l1',solver='liblinear',C=0.1,random_state=0).fit((A-mu)/sd,y[tr])
    return c.predict_proba((B-mu)/sd)[:,1],int(keep.sum())
res={'dir1':{},'dir2':{}}
for s in sorted(m.Study.unique()):
    idx=np.where(m.Study==s)[0]; a=[]
    for tr,te in RepeatedStratifiedKFold(n_splits=5,n_repeats=10,random_state=0).split(idx,y[idx]):
        p,_=fit_pred(idx[tr],idx[te]); a.append(roc_auc_score(y[idx[te]],p))
    res['dir1'][s]=dict(auroc=round(float(np.mean(a)),3),sd=round(float(np.std(a)),3),n=int(len(idx)))
    tr=np.where(m.Study!=s)[0]; p,nf=fit_pred(tr,idx)
    res['dir2'][s]=dict(auroc=round(float(roc_auc_score(y[idx],p)),3),n_test=int(len(idx)),n_train=int(len(tr)),n_features=nf)
a1=[v['auroc'] for v in res['dir1'].values()]; a2=[v['auroc'] for v in res['dir2'].values()]
res['summary']=dict(dir1_median=float(np.median(a1)),dir1_gate_pass=bool(np.median(a1)>=0.70),dir2_median=float(np.median(a2)),dir2_min=min(a2),dir2_gate_pass=bool(np.median(a2)>=0.70 and min(a2)>=0.60))
json.dump(res,open('results/dir1_dir2.json','w'),indent=1); print(json.dumps(res,indent=1))
