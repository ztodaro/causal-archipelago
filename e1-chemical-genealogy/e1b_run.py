"""E1b - powered chemical genealogy per frozen E1B-SPEC.md (ec12d01).
Masking caveat (documented): Theia/CG carry DR2 ids; exact numeric joins
across DR2->DR3 miss the minority of re-assigned ids - declared
contamination risk per spec, reported not silently fixed."""
import csv, json, pickle, sys, numpy as np
sys.path.insert(0,'/root/ca/m3')
import importlib.util
spec=importlib.util.spec_from_file_location('d40','/root/ca/m3/d40_full_standalone.py')
d40=importlib.util.module_from_spec(spec); spec.loader.exec_module(d40)
AG=d40.AG; KMS=1.02269; KAPPA=4.740470446
from scipy.spatial import cKDTree
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from scipy.stats import mannwhitneyu
E='/mnt/user-data/uploads/projects/causal-archipelago/e1-chemical-genealogy/data'
V='/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/vetting'
C='/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/crossmatch-catalogs/raw'

# ---- masking set (exact integer-string ids) ----
maskids=set()
def addmask(path,col):
    n0=len(maskids)
    for r in csv.DictReader(open(path)):
        v=r[col].strip()
        if v: maskids.add(v)
    print(f"mask += {path.split('/')[-1]}: {len(maskids)-n0}")
addmask(f'{E}/e1b_cg_members.csv','GaiaDR2')
addmask(f'{C}/theia_clustered_sources.csv','Gaia')
addmask(f'{V}/data/catalog-updates/raw/bertolotto_members.csv','GaiaDR3')
addmask(f'{V}/data/catalog-updates/raw/moranta_table1.csv','Gaia')
addmask(f'{V}/data/catalog-updates/raw/lee_nymg_tableb1.csv','GaiaEDR3')
addmask(f'{V}/data/catalog-updates/raw/jerabkova_hyades_edr3.csv','GaiaEDR3')
addmask(f'{V}/data/catalog-updates/raw/spyglass_young_candidate_hits.csv','Gaia')
sidc,_,_ = d40.load_phase_space_np('/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/gaia_100pc_rv.csv'), None, None
# BANYAN 100pc sky-matches from membership.pkl
import numpy as np
g0=np.genfromtxt('/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/gaia_100pc_rv.csv',delimiter=',',names=True,usecols=(0,),dtype=None,encoding='utf-8')
sids0=[str(int(x)) for x in np.atleast_1d(g0['source_id'])]
for i,m in enumerate(pickle.load(open('/root/ca/m3/membership.pkl','rb'))):
    if m: maskids.add(sids0[i])
print(f"total mask ids: {len(maskids)}")

def phase_space(ra,dec,plx,pmra,pmdec,rv):
    ra_r,dec_r=np.radians(ra),np.radians(dec)
    dist=1000.0/plx
    ca,sa,cd,sd=np.cos(ra_r),np.sin(ra_r),np.cos(dec_r),np.sin(dec_r)
    rhat=np.column_stack([cd*ca,cd*sa,sd])
    phat=np.column_stack([-sa,ca,np.zeros_like(sa)])
    qhat=np.column_stack([-sd*ca,-sd*sa,cd])
    pos=(rhat*dist[:,None])@AG.T
    v=(rv[:,None]*rhat+(KAPPA*pmra/plx)[:,None]*phat+(KAPPA*pmdec/plx)[:,None]*qhat)
    return pos,(v@AG.T)          # pos pc (galactic), vel km/s (galactic)

def load_survey(name):
    ids=[];ra=[];dec=[];plx=[];pmra=[];pmdec=[];rv=[];snr=[];teff=[];logg=[];feh=[]
    if name=='GALAH':
        cols=dict(id='gaiadr3_source_id',ra='ra',dec='dec',plx='parallax',
                  pmra='pmra',pmdec='pmdec',rv='rv',snr='snr',teff='teff',logg='logg',feh='fe_h')
        path=f'{E}/e1b_galah.csv'
    else:
        cols=dict(id='GAIAEDR3_SOURCE_ID',ra='GAIAEDR3_RA',dec='GAIAEDR3_DEC',plx='GAIAEDR3_PARALLAX',
                  pmra='GAIAEDR3_PMRA',pmdec='GAIAEDR3_PMDEC',rv='VHELIO_AVG',snr='SNR',
                  teff='TEFF',logg='LOGG',feh='FE_H')
        path=f'{E}/e1b_apogee.csv'
    best={}
    for r in csv.DictReader(open(path)):
        i=r[cols['id']].strip()
        if not i or i in maskids: continue
        try:
            row=[float(r[cols[k]]) for k in ('ra','dec','plx','pmra','pmdec','rv','snr','teff','logg','feh')]
        except ValueError: continue
        if not all(np.isfinite(row)): continue
        if i not in best or row[6]>best[i][6]: best[i]=row
    ids=list(best); arr=np.array([best[i] for i in ids])
    pos,vel=phase_space(arr[:,0],arr[:,1],arr[:,2],arr[:,3],arr[:,4],arr[:,5])
    return ids,pos,vel,arr[:,7],arr[:,8],arr[:,9]   # teff, logg, feh

rng=np.random.default_rng(17)
results={}
for name in ('GALAH','APOGEE'):
    ids,P,Vv,teff,logg,feh=load_survey(name)
    n_s=len(ids); print(f"\n{name}: clean unmasked unique stars = {n_s}", flush=True)
    dmean_star=np.linalg.norm(P,axis=1)
    tree=cKDTree(P)
    pairs=tree.query_pairs(25.0,output_type='ndarray')
    dxp=np.linalg.norm(P[pairs[:,0]]-P[pairs[:,1]],axis=1)
    dvp=np.linalg.norm(Vv[pairs[:,0]]-Vv[pairs[:,1]],axis=1)
    treat=pairs[(dxp<20)&(dvp<3)]
    cand=pairs[dvp>6]; cdx=np.linalg.norm(P[cand[:,0]]-P[cand[:,1]],axis=1)
    print(f"treatment pairs={len(treat)}  control candidates={len(cand)}", flush=True)
    # effective clusters
    gph=sparse.coo_matrix((np.ones(len(treat)),(treat[:,0],treat[:,1])),shape=(n_s,n_s))
    ncomp_all,lab=connected_components(gph,directed=False)
    tstars=np.unique(treat.ravel()); comp_ids=np.unique(lab[tstars])
    ncl=len(comp_ids)
    print(f"effective treatment clusters = {ncl}", flush=True)
    # controls with distance matching
    from collections import defaultdict
    cmean=0.5*(dmean_star[cand[:,0]]+dmean_star[cand[:,1]])
    buck=defaultdict(list)
    for k in range(len(cand)):
        a,b=cand[k]
        buck[(int(cdx[k]//5),int(teff[a]//150),int(logg[a]//0.3)%1000,
              int(teff[b]//150),int(logg[b]//0.3)%1000,int(cmean[k]//150))].append(k)
    tsep=np.linalg.norm(P[treat[:,0]]-P[treat[:,1]],axis=1)
    tmean=0.5*(dmean_star[treat[:,0]]+dmean_star[treat[:,1]])
    t_d=[];c_d=[];t_pairs=[];c_pairs=[];matched=0
    for k,(a,b) in enumerate(treat):
        cs=[]
        for da in (-1,0,1):
            for dm in (-1,0,1):
                for perm in ((a,b),(b,a)):
                    for dt1 in (-1,0,1):
                        for dg1 in (-1,0,1):
                            for dt2 in (-1,0,1):
                                for dg2 in (-1,0,1):
                                    key=(int(tsep[k]//5)+da,int(teff[perm[0]]//150)+dt1,
                                         (int(logg[perm[0]]//0.3)%1000)+dg1,
                                         int(teff[perm[1]]//150)+dt2,
                                         (int(logg[perm[1]]//0.3)%1000)+dg2,
                                         int(tmean[k]//150)+dm)
                                    for kk in buck.get(key,()):
                                        ca,cb=cand[kk]
                                        if abs(cdx[kk]-tsep[k])>5: continue
                                        if abs(cmean[kk]-tmean[k])>150: continue
                                        ok=(abs(teff[ca]-teff[perm[0]])<=150 and abs(logg[ca]-logg[perm[0]])<=0.3
                                            and abs(teff[cb]-teff[perm[1]])<=150 and abs(logg[cb]-logg[perm[1]])<=0.3)
                                        if ok: cs.append(kk)
        if not cs: continue
        pick=rng.choice(len(cs),size=min(10,len(cs)),replace=False)
        matched+=1
        t_d.append(abs(feh[a]-feh[b])); t_pairs.append((a,b))
        for pk in pick:
            ca,cb=cand[cs[pk]]; c_d.append(abs(feh[ca]-feh[cb])); c_pairs.append((ca,cb))
    t_d=np.array(t_d);c_d=np.array(c_d)
    print(f"matched treatment pairs={matched} control pairs={len(c_d)}", flush=True)
    if matched<20 or ncl<30:
        results[name]=dict(status='underpowered',matched=int(matched),clusters=int(ncl)); continue
    U,p=mannwhitneyu(t_d,c_d,alternative='less')
    t_pairs=np.array(t_pairs);c_pairs=np.array(c_pairs)
    stars=np.unique(np.concatenate([t_pairs.ravel(),c_pairs.ravel()]))
    smap={s:k for k,s in enumerate(stars)}
    tpi=np.vectorize(smap.get)(t_pairs);cpi=np.vectorize(smap.get)(c_pairs)
    def wmed(v,w):
        o=np.argsort(v);v,w=v[o],w[o];cw=np.cumsum(w)
        return v[np.searchsorted(cw,cw[-1]/2)]
    diffs=[]
    for _ in range(1000):
        cnt=np.bincount(rng.integers(0,len(stars),len(stars)),minlength=len(stars))
        wt=cnt[tpi[:,0]]*cnt[tpi[:,1]];wc=cnt[cpi[:,0]]*cnt[cpi[:,1]]
        if wt.sum()==0 or wc.sum()==0: continue
        diffs.append(wmed(t_d,wt)-wmed(c_d,wc))
    lo,hi=np.percentile(diffs,[2.5,97.5])
    conf = bool(hi<0 and ncl>=30)
    results[name]=dict(status='ok',stars=int(n_s),treat=int(matched),controls=int(len(c_d)),
        clusters=int(ncl),med_treat=round(float(np.median(t_d)),4),
        med_control=round(float(np.median(c_d)),4),
        med_diff=round(float(np.median(t_d)-np.median(c_d)),4),
        boot_CI=[round(float(lo),4),round(float(hi),4)],p=float(f"{p:.2e}"),
        CONFIRMED=conf)
    print(f"{name}: |dFeH| treat={np.median(t_d):.4f} ctrl={np.median(c_d):.4f} "
          f"diff={np.median(t_d)-np.median(c_d):+.4f} CI[{lo:.4f},{hi:.4f}] p={p:.2e} "
          f"clusters={ncl} -> {'CONFIRMED' if conf else 'not confirmed'}", flush=True)
np.save('/root/ca/m3/e1b_t_d.npy', t_d); np.save('/root/ca/m3/e1b_c_d.npy', c_d)
json.dump(results,open('/root/ca/m3/e1b_results.json','w'),indent=1)
print("\nDONE")
