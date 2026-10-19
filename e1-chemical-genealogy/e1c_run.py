"""E1c - orbit-matched control amendment to E1b, per frozen E1C-SPEC.md.
Loading, masking, treatment definition, C0 control construction, statistic
and bootstrap are copied verbatim from e1b_run.py (E1b, spec ec12d01).
New: E8-style epicyclic actions; graded control tiers C1-C4."""
import csv, json, pickle, sys, hashlib, numpy as np
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
OUT='/root/ca/fresh/e1c'
SELF_SHA=hashlib.sha256(open(__file__,'rb').read()).hexdigest()

# ---- E8 frozen action constants (e8_sieve.py) ----
R0=8.2; VC=233.1; USUN,VSUN,WSUN=11.1,12.24,7.25; NU=73.5; KAP=40.2
def actions(pos, vel):
    x,y,z=pos[:,0],pos[:,1],pos[:,2]
    d=np.column_stack([x-R0*1000,y]); R=np.hypot(d[:,0],d[:,1])/1000.0
    eR=np.column_stack([d[:,0],d[:,1]])/(R[:,None]*1000)
    ephi=np.column_stack([eR[:,1],-eR[:,0]])
    vtot=vel+np.array([USUN,VSUN+VC,WSUN])
    vR=vtot[:,0]*eR[:,0]+vtot[:,1]*eR[:,1]
    vphi=vtot[:,0]*ephi[:,0]+vtot[:,1]*ephi[:,1]
    Lz=R*vphi; Rg=Lz/VC
    Jr=0.5*(vR**2+KAP**2*(Rg-R)**2)/KAP
    Jz=0.5*(vtot[:,2]**2+NU**2*(z/1000.0)**2)/NU
    return R,Lz,Jr,Jz

# ---- masking set (verbatim E1b) ----
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
    return pos,(v@AG.T)

def load_survey(name):
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
    return ids,pos,vel,arr[:,7],arr[:,8],arr[:,9]

def wmed(v,w):
    o=np.argsort(v);v,w=v[o],w[o];cw=np.cumsum(w)
    return v[np.searchsorted(cw,cw[-1]/2)]

def stats(t_d,c_d,t_pairs,c_pairs,ncl,rng):
    """E1b statistic + star-clustered bootstrap, verbatim logic."""
    U,p=mannwhitneyu(t_d,c_d,alternative='less')
    t_pairs=np.array(t_pairs);c_pairs=np.array(c_pairs)
    stars=np.unique(np.concatenate([t_pairs.ravel(),c_pairs.ravel()]))
    smap={s:k for k,s in enumerate(stars)}
    tpi=np.vectorize(smap.get)(t_pairs);cpi=np.vectorize(smap.get)(c_pairs)
    diffs=[]
    for _ in range(1000):
        cnt=np.bincount(rng.integers(0,len(stars),len(stars)),minlength=len(stars))
        wt=cnt[tpi[:,0]]*cnt[tpi[:,1]];wc=cnt[cpi[:,0]]*cnt[cpi[:,1]]
        if wt.sum()==0 or wc.sum()==0: continue
        diffs.append(wmed(t_d,wt)-wmed(c_d,wc))
    lo,hi=np.percentile(diffs,[2.5,97.5])
    return dict(treat=int(len(t_d)),controls=int(len(c_d)),clusters=int(ncl),
        med_treat=round(float(np.median(t_d)),4),med_control=round(float(np.median(c_d)),4),
        med_diff=round(float(np.median(t_d)-np.median(c_d)),4),
        boot_CI=[round(float(lo),4),round(float(hi),4)],p=float(f"{p:.2e}"))

def eff_clusters(treat_sub,n_s):
    gph=sparse.coo_matrix((np.ones(len(treat_sub)),(treat_sub[:,0],treat_sub[:,1])),shape=(n_s,n_s))
    _,lab=connected_components(gph,directed=False)
    return len(np.unique(lab[np.unique(treat_sub.ravel())]))

E1B_UPPER={'GALAH':-0.0825,'APOGEE':-0.0883}
E1B_REF=json.load(open('/root/ca/m3/e1b_results.json'))
results={'script_sha256':SELF_SHA,'spec':'E1C-SPEC.md','surveys':{}}
rng=np.random.default_rng(17)      # E1b seed, consumed by C0 exactly as e1b_run.py
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
    ncl=eff_clusters(treat,n_s)
    # ---------------- C0: E1b verbatim ----------------
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
                                         (int(logg[perm[0]]//0.3)%1000)+dg1,int(teff[perm[1]]//150)+dt2,
                                         (int(logg[perm[1]]//0.3)%1000)+dg2,int(tmean[k]//150)+dm)
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
    c0=stats(t_d,c_d,t_pairs,c_pairs,ncl,rng)
    ref=E1B_REF[name]
    gate=(c0['treat']==ref['treat'] and c0['controls']==ref['controls'] and c0['clusters']==ref['clusters']
          and c0['med_diff']==ref['med_diff'] and c0['boot_CI']==ref['boot_CI'])
    print(f"C0 reproduce-first gate {name}: {'PASS' if gate else 'FAIL'} {c0}", flush=True)
    sv={'C0':dict(c0,gate='PASS' if gate else 'FAIL')}
    if not gate:
        results['surveys'][name]=sv; continue
    # ---------------- actions and tolerances ----------------
    R,Lz,Jr,Jz=actions(P,Vv)
    dL=np.abs(Lz[treat[:,0]]-Lz[treat[:,1]]); dz=np.abs(Jz[treat[:,0]]-Jz[treat[:,1]]); dr=np.abs(Jr[treat[:,0]]-Jr[treat[:,1]])
    tauL,tauz,taur=[float(np.percentile(x,90)) for x in (dL,dz,dr)]
    sv['tolerances']=dict(tau_Lz=round(tauL,3),tau_Jz=round(tauz,4),tau_Jr=round(taur,4),
                          treat_median_dLz=round(float(np.median(dL)),3),treat_median_dJz=round(float(np.median(dz)),4),
                          treat_median_dJr=round(float(np.median(dr)),4))
    print(f"tolerances {name}: {sv['tolerances']}", flush=True)
    # ---------------- graded tiers ----------------
    rng2=np.random.default_rng(1701)
    Lm=0.5*(Lz[treat[:,0]]+Lz[treat[:,1]]); zm=0.5*(Jz[treat[:,0]]+Jz[treat[:,1]]); rm=0.5*(Jr[treat[:,0]]+Jr[treat[:,1]])
    def run_tier(tier,S):
        feats=[teff/150.0,logg/0.3,dmean_star/150.0]
        qcols=[]
        if tier>=2: feats.append(Lz/tauL)
        if tier>=3: feats.append(Jz/tauz)
        if tier>=4: feats.append(Jr/taur)
        F=np.column_stack(feats); kt=cKDTree(F)
        td=[];cd=[];tp=[];cp=[];nmatch=0
        for k,(a,b) in enumerate(treat):
            qa=[teff[a]/150.0,logg[a]/0.3,tmean[k]/150.0]; qb=[teff[b]/150.0,logg[b]/0.3,tmean[k]/150.0]
            extra=[]
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
                tries+=1
                x=int(A[rng2.integers(len(A))]); y=int(B[rng2.integers(len(B))])
                if x==y or (x,y) in seen or (y,x) in seen: continue
                if np.linalg.norm(P[x]-P[y])<=S: continue
                seen.add((x,y)); got.append((x,y))
            if not got: continue
            nmatch+=1; td.append(abs(feh[a]-feh[b])); tp.append((a,b))
            for x,y in got: cd.append(abs(feh[x]-feh[y])); cp.append((x,y))
        td=np.array(td);cd=np.array(cd)
        if nmatch==0: return dict(status='no matches',treat=0)
        ncl_t=eff_clusters(np.array(tp),n_s)
        out=stats(td,cd,tp,cp,ncl_t,rng2)
        out['status']='ok' if (nmatch>=200 and ncl_t>=30) else 'UNDERPOWERED'
        out['S_min_pc']=S
        return out
    for tier in (1,2,3,4):
        r=run_tier(tier,300.0); sv[f'C{tier}']=r
        print(f"{name} C{tier} S=300: {r}", flush=True)
    for S in (100.0,1000.0):
        r=run_tier(4,S); sv[f'C4_S{int(S)}']=r
        print(f"{name} C4 S={int(S)}: {r}", flush=True)
    # ---------------- verdict ----------------
    c4=sv['C4']
    if c4.get('status')!='ok': verdict='UNDERPOWERED'
    elif c4['boot_CI'][1]<0 and c4['med_diff']<=E1B_UPPER[name]: verdict='SURVIVES'
    elif c4['boot_CI'][1]<0: verdict='SHRINKS'
    else: verdict='VANISHES'
    sv['verdict']=verdict
    print(f"\n{name} VERDICT (C4, S=300): {verdict}", flush=True)
    results['surveys'][name]=sv
order={'VANISHES':0,'SHRINKS':1,'SURVIVES':2,'UNDERPOWERED':-1}
vs=[results['surveys'][n].get('verdict','UNDERPOWERED') for n in results['surveys']]
results['project_verdict']=min(vs,key=lambda v:order[v]) if vs else 'NOT RUN'
json.dump(results,open(f'{OUT}/e1c_results.json','w'),indent=1)
print("\nPROJECT VERDICT:",results['project_verdict']); print("DONE")
