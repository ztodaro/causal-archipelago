"""E1c post-hoc diagnostic (labelled as such; not decision-bearing).
Question: is the C0->C4 shrink an orbit effect or a subset-composition effect?
Replays E1c tiers (seed 1701) to recover the C4-matched treatment subset, then
recomputes C0-style (E1b: near, dv>6) and C1-C3 controls RESTRICTED to that
subset with a fresh seed (4242), so all tiers are compared on identical pairs."""
import csv, json, pickle, sys, numpy as np
sys.path.insert(0,'/root/ca/m3')
import importlib.util
spec=importlib.util.spec_from_file_location('d40','/root/ca/m3/d40_full_standalone.py')
d40=importlib.util.module_from_spec(spec); spec.loader.exec_module(d40)
AG=d40.AG; KAPPA=4.740470446
from scipy.spatial import cKDTree
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from scipy.stats import mannwhitneyu
from collections import defaultdict
E='/mnt/user-data/uploads/projects/causal-archipelago/e1-chemical-genealogy/data'
V='/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/vetting'
C='/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/crossmatch-catalogs/raw'
OUT='/root/ca/fresh/e1c'
R0=8.2; VC=233.1; USUN,VSUN,WSUN=11.1,12.24,7.25; NU=73.5; KAP=40.2
def actions(pos, vel):
    x,y,z=pos[:,0],pos[:,1],pos[:,2]
    d=np.column_stack([x-R0*1000,y]); R=np.hypot(d[:,0],d[:,1])/1000.0
    eR=np.column_stack([d[:,0],d[:,1]])/(R[:,None]*1000); ephi=np.column_stack([eR[:,1],-eR[:,0]])
    vtot=vel+np.array([USUN,VSUN+VC,WSUN])
    vR=vtot[:,0]*eR[:,0]+vtot[:,1]*eR[:,1]; vphi=vtot[:,0]*ephi[:,0]+vtot[:,1]*ephi[:,1]
    Lz=R*vphi; Rg=Lz/VC
    return R,Lz,0.5*(vR**2+KAP**2*(Rg-R)**2)/KAP,0.5*(vtot[:,2]**2+NU**2*(z/1000.0)**2)/NU
maskids=set()
def addmask(path,col):
    for r in csv.DictReader(open(path)):
        v=r[col].strip()
        if v: maskids.add(v)
addmask(f'{E}/e1b_cg_members.csv','GaiaDR2'); addmask(f'{C}/theia_clustered_sources.csv','Gaia')
addmask(f'{V}/data/catalog-updates/raw/bertolotto_members.csv','GaiaDR3'); addmask(f'{V}/data/catalog-updates/raw/moranta_table1.csv','Gaia')
addmask(f'{V}/data/catalog-updates/raw/lee_nymg_tableb1.csv','GaiaEDR3'); addmask(f'{V}/data/catalog-updates/raw/jerabkova_hyades_edr3.csv','GaiaEDR3')
addmask(f'{V}/data/catalog-updates/raw/spyglass_young_candidate_hits.csv','Gaia')
g0=np.genfromtxt('/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/gaia_100pc_rv.csv',delimiter=',',names=True,usecols=(0,),dtype=None,encoding='utf-8')
sids0=[str(int(x)) for x in np.atleast_1d(g0['source_id'])]
for i,m in enumerate(pickle.load(open('/root/ca/m3/membership.pkl','rb'))):
    if m: maskids.add(sids0[i])
def phase_space(ra,dec,plx,pmra,pmdec,rv):
    ra_r,dec_r=np.radians(ra),np.radians(dec); dist=1000.0/plx
    ca,sa,cd,sd=np.cos(ra_r),np.sin(ra_r),np.cos(dec_r),np.sin(dec_r)
    rhat=np.column_stack([cd*ca,cd*sa,sd]); phat=np.column_stack([-sa,ca,np.zeros_like(sa)]); qhat=np.column_stack([-sd*ca,-sd*sa,cd])
    pos=(rhat*dist[:,None])@AG.T
    v=(rv[:,None]*rhat+(KAPPA*pmra/plx)[:,None]*phat+(KAPPA*pmdec/plx)[:,None]*qhat)
    return pos,(v@AG.T)
def load_survey(name):
    if name=='GALAH':
        cols=dict(id='gaiadr3_source_id',ra='ra',dec='dec',plx='parallax',pmra='pmra',pmdec='pmdec',rv='rv',snr='snr',teff='teff',logg='logg',feh='fe_h'); path=f'{E}/e1b_galah.csv'
    else:
        cols=dict(id='GAIAEDR3_SOURCE_ID',ra='GAIAEDR3_RA',dec='GAIAEDR3_DEC',plx='GAIAEDR3_PARALLAX',pmra='GAIAEDR3_PMRA',pmdec='GAIAEDR3_PMDEC',rv='VHELIO_AVG',snr='SNR',teff='TEFF',logg='LOGG',feh='FE_H'); path=f'{E}/e1b_apogee.csv'
    best={}
    for r in csv.DictReader(open(path)):
        i=r[cols['id']].strip()
        if not i or i in maskids: continue
        try: row=[float(r[cols[k]]) for k in ('ra','dec','plx','pmra','pmdec','rv','snr','teff','logg','feh')]
        except ValueError: continue
        if not all(np.isfinite(row)): continue
        if i not in best or row[6]>best[i][6]: best[i]=row
    ids=list(best); arr=np.array([best[i] for i in ids])
    pos,vel=phase_space(arr[:,0],arr[:,1],arr[:,2],arr[:,3],arr[:,4],arr[:,5])
    return ids,pos,vel,arr[:,7],arr[:,8],arr[:,9]
def wmed(v,w):
    o=np.argsort(v);v,w=v[o],w[o];cw=np.cumsum(w); return v[np.searchsorted(cw,cw[-1]/2)]
def stats(t_d,c_d,t_pairs,c_pairs,rng):
    t_pairs=np.array(t_pairs);c_pairs=np.array(c_pairs)
    stars=np.unique(np.concatenate([t_pairs.ravel(),c_pairs.ravel()])); smap={s:k for k,s in enumerate(stars)}
    tpi=np.vectorize(smap.get)(t_pairs);cpi=np.vectorize(smap.get)(c_pairs); diffs=[]
    for _ in range(1000):
        cnt=np.bincount(rng.integers(0,len(stars),len(stars)),minlength=len(stars))
        wt=cnt[tpi[:,0]]*cnt[tpi[:,1]];wc=cnt[cpi[:,0]]*cnt[cpi[:,1]]
        if wt.sum()==0 or wc.sum()==0: continue
        diffs.append(wmed(t_d,wt)-wmed(c_d,wc))
    lo,hi=np.percentile(diffs,[2.5,97.5])
    return dict(treat=int(len(t_d)),controls=int(len(c_d)),med_treat=round(float(np.median(t_d)),4),med_control=round(float(np.median(c_d)),4),
                med_diff=round(float(np.median(t_d)-np.median(c_d)),4),boot_CI=[round(float(lo),4),round(float(hi),4)])
e1c=json.load(open(f'{OUT}/e1c_results.json'))
out={}
for name in ('GALAH','APOGEE'):
    ids,P,Vv,teff,logg,feh=load_survey(name); n_s=len(ids)
    dmean_star=np.linalg.norm(P,axis=1); tree=cKDTree(P); pairs=tree.query_pairs(25.0,output_type='ndarray')
    dxp=np.linalg.norm(P[pairs[:,0]]-P[pairs[:,1]],axis=1); dvp=np.linalg.norm(Vv[pairs[:,0]]-Vv[pairs[:,1]],axis=1)
    treat=pairs[(dxp<20)&(dvp<3)]; cand=pairs[dvp>6]; cdx=np.linalg.norm(P[cand[:,0]]-P[cand[:,1]],axis=1)
    tsep=np.linalg.norm(P[treat[:,0]]-P[treat[:,1]],axis=1); tmean=0.5*(dmean_star[treat[:,0]]+dmean_star[treat[:,1]])
    R,Lz,Jr,Jz=actions(P,Vv)
    dL=np.abs(Lz[treat[:,0]]-Lz[treat[:,1]]); dz=np.abs(Jz[treat[:,0]]-Jz[treat[:,1]]); dr=np.abs(Jr[treat[:,0]]-Jr[treat[:,1]])
    tauL,tauz,taur=[float(np.percentile(x,90)) for x in (dL,dz,dr)]
    assert abs(tauL-e1c['surveys'][name]['tolerances']['tau_Lz'])<1e-3
    Lm=0.5*(Lz[treat[:,0]]+Lz[treat[:,1]]); zm=0.5*(Jz[treat[:,0]]+Jz[treat[:,1]]); rm=0.5*(Jr[treat[:,0]]+Jr[treat[:,1]])
    def run_tier(tier,S,rng,subset=None):
        feats=[teff/150.0,logg/0.3,dmean_star/150.0]
        if tier>=2: feats.append(Lz/tauL)
        if tier>=3: feats.append(Jz/tauz)
        if tier>=4: feats.append(Jr/taur)
        F=np.column_stack(feats); kt=cKDTree(F)
        td=[];cd=[];tp=[];cp=[];ks=[]
        for k,(a,b) in enumerate(treat):
            if subset is not None and k not in subset: continue
            qa=[teff[a]/150.0,logg[a]/0.3,tmean[k]/150.0]; qb=[teff[b]/150.0,logg[b]/0.3,tmean[k]/150.0]; extra=[]
            if tier>=2: extra.append(Lm[k]/tauL)
            if tier>=3: extra.append(zm[k]/tauz)
            if tier>=4: extra.append(rm[k]/taur)
            A=np.array(kt.query_ball_point(qa+extra,1.0,p=np.inf)); B=np.array(kt.query_ball_point(qb+extra,1.0,p=np.inf))
            if len(A)==0 or len(B)==0: continue
            A=A[(np.linalg.norm(P[A]-P[a],axis=1)>S)&(np.linalg.norm(P[A]-P[b],axis=1)>S)]
            B=B[(np.linalg.norm(P[B]-P[a],axis=1)>S)&(np.linalg.norm(P[B]-P[b],axis=1)>S)]
            if len(A)==0 or len(B)==0: continue
            got=[];tries=0;seen=set()
            while len(got)<10 and tries<60:
                tries+=1; x=int(A[rng.integers(len(A))]); y=int(B[rng.integers(len(B))])
                if x==y or (x,y) in seen or (y,x) in seen: continue
                if np.linalg.norm(P[x]-P[y])<=S: continue
                seen.add((x,y)); got.append((x,y))
            if not got: continue
            td.append(abs(feh[a]-feh[b])); tp.append((a,b)); ks.append(k)
            for x,y in got: cd.append(abs(feh[x]-feh[y])); cp.append((x,y))
        return np.array(td),np.array(cd),tp,cp,ks
    rng2=np.random.default_rng(1701)
    def replay_boot(tp,cp,rng):   # e1c_run.py's stats() consumed 1000 bootstrap draws from rng2 per tier
        stars=np.unique(np.concatenate([np.array(tp).ravel(),np.array(cp).ravel()]))
        for _ in range(1000): rng.integers(0,len(stars),len(stars))
    for tier in (1,2,3):
        _,_,tp_,cp_,_=run_tier(tier,300.0,rng2); replay_boot(tp_,cp_,rng2)
    td4,cd4,tp4,cp4,ks4=run_tier(4,300.0,rng2)
    ref=e1c['surveys'][name]['C4']
    assert len(td4)==ref['treat'] and len(cd4)==ref['controls'], "C4 replay mismatch"
    print(f"{name}: C4 replay ok, subset={len(ks4)}",flush=True)
    sub=set(ks4); rngd=np.random.default_rng(4242); res={}
    # C0-style controls restricted to subset (E1b construction, fresh seed)
    cmean=0.5*(dmean_star[cand[:,0]]+dmean_star[cand[:,1]]); buck=defaultdict(list)
    for k in range(len(cand)):
        a,b=cand[k]; buck[(int(cdx[k]//5),int(teff[a]//150),int(logg[a]//0.3)%1000,int(teff[b]//150),int(logg[b]//0.3)%1000,int(cmean[k]//150))].append(k)
    t_d=[];c_d=[];t_p=[];c_p=[]
    for k,(a,b) in enumerate(treat):
        if k not in sub: continue
        cs=[]
        for da in (-1,0,1):
            for dm in (-1,0,1):
                for perm in ((a,b),(b,a)):
                    for dt1 in (-1,0,1):
                        for dg1 in (-1,0,1):
                            for dt2 in (-1,0,1):
                                for dg2 in (-1,0,1):
                                    key=(int(tsep[k]//5)+da,int(teff[perm[0]]//150)+dt1,(int(logg[perm[0]]//0.3)%1000)+dg1,int(teff[perm[1]]//150)+dt2,(int(logg[perm[1]]//0.3)%1000)+dg2,int(tmean[k]//150)+dm)
                                    for kk in buck.get(key,()):
                                        ca,cb=cand[kk]
                                        if abs(cdx[kk]-tsep[k])>5 or abs(cmean[kk]-tmean[k])>150: continue
                                        if (abs(teff[ca]-teff[perm[0]])<=150 and abs(logg[ca]-logg[perm[0]])<=0.3 and abs(teff[cb]-teff[perm[1]])<=150 and abs(logg[cb]-logg[perm[1]])<=0.3): cs.append(kk)
        if not cs: continue
        pick=rngd.choice(len(cs),size=min(10,len(cs)),replace=False)
        t_d.append(abs(feh[a]-feh[b])); t_p.append((a,b))
        for pk in pick:
            ca,cb=cand[cs[pk]]; c_d.append(abs(feh[ca]-feh[cb])); c_p.append((ca,cb))
    res['C0_on_C4subset']=stats(np.array(t_d),np.array(c_d),t_p,c_p,rngd)
    for tier in (1,2,3):
        td,cd,tp,cp,ks=run_tier(tier,300.0,rngd,subset=sub)
        res[f'C{tier}_on_C4subset']=stats(td,cd,tp,cp,rngd)
    res['C4']=stats(td4,cd4,tp4,cp4,rngd)
    # composition: treatment |dFeH| median on the C4 subset vs the rest
    allt=np.abs(feh[treat[:,0]]-feh[treat[:,1]]); insub=np.array([k in sub for k in range(len(treat))])
    res['treat_median_all']=round(float(np.median(allt)),4); res['treat_median_C4subset']=round(float(np.median(allt[insub])),4); res['treat_median_rest']=round(float(np.median(allt[~insub])),4)
    # what distinguishes the subset: action-space density (cell occupancy) and |z|
    res['subset_median_Jz']=round(float(np.median(zm[insub])),3); res['rest_median_Jz']=round(float(np.median(zm[~insub])),3)
    res['subset_median_Jr']=round(float(np.median(rm[insub])),3); res['rest_median_Jr']=round(float(np.median(rm[~insub])),3)
    res['subset_median_dist_pc']=round(float(np.median(tmean[insub])),1); res['rest_median_dist_pc']=round(float(np.median(tmean[~insub])),1)
    out[name]=res; print(name,json.dumps(res,indent=1),flush=True)
json.dump(out,open(f'{OUT}/e1c_diag.json','w'),indent=1); print("DONE")
