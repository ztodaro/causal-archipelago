"""E10b Amendment 1 - per-pair error-anchored conatal width (identifiability), per E10B-AMENDMENT-1.md.
Frozen-run script e10b_run.py is unchanged; this file differs only where marked A1.
Replays E1c's GALAH loading and C1-C4 control construction (seed 1701) to
recover the C4 pair-level data, gates on exact agreement with e1c_results.json,
joins the frozen [Y/Mg] clock, fits the mixture, runs the two oracles, reports."""
import csv, json, pickle, sys, gzip, hashlib, numpy as np
sys.path.insert(0,'/root/ca/m3')
import importlib.util
spec=importlib.util.spec_from_file_location('d40','/root/ca/m3/d40_full_standalone.py')
d40=importlib.util.module_from_spec(spec); spec.loader.exec_module(d40)
AG=d40.AG; KAPPA=4.740470446
from scipy.spatial import cKDTree
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from scipy.optimize import minimize
from scipy.stats import norm
E='/mnt/user-data/uploads/projects/causal-archipelago/e1-chemical-genealogy/data'
V='/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/vetting'
C='/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/crossmatch-catalogs/raw'
ABUND='/mnt/user-data/uploads/projects/causal-archipelago/solar-siblings/data/e8_galah_abund.csv.gz'
E1C='/root/ca/fresh/e1c/e1c_results.json'
OUT='/root/ca/fresh/e10b'
TAG='_a1'
SIG_INT_MAX=0.05   # A1: bound on intrinsic conatal scatter (dex)
SELF_SHA=hashlib.sha256(open(__file__,'rb').read()).hexdigest()
CLOCK_A,CLOCK_B=0.170,0.0371
BINS=[(0,2),(2,4.5),(4.5,8),(8,14)]
R0=8.2; VC=233.1; USUN,VSUN,WSUN=11.1,12.24,7.25; NU=73.5; KAP=40.2
def actions(pos, vel):
    x,y,z=pos[:,0],pos[:,1],pos[:,2]
    d=np.column_stack([x-R0*1000,y]); R=np.hypot(d[:,0],d[:,1])/1000.0
    eR=np.column_stack([d[:,0],d[:,1]])/(R[:,None]*1000)
    ephi=np.column_stack([eR[:,1],-eR[:,0]])
    vtot=vel+np.array([USUN,VSUN+VC,WSUN])
    vR=vtot[:,0]*eR[:,0]+vtot[:,1]*eR[:,1]; vphi=vtot[:,0]*ephi[:,0]+vtot[:,1]*ephi[:,1]
    Lz=R*vphi; Rg=Lz/VC
    Jr=0.5*(vR**2+KAP**2*(Rg-R)**2)/KAP; Jz=0.5*(vtot[:,2]**2+NU**2*(z/1000.0)**2)/NU
    return R,Lz,Jr,Jz
# ---- masking + loading, verbatim E1b/E1c ----
maskids=set()
def addmask(path,col):
    for r in csv.DictReader(open(path)):
        v=r[col].strip()
        if v: maskids.add(v)
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
def phase_space(ra,dec,plx,pmra,pmdec,rv):
    ra_r,dec_r=np.radians(ra),np.radians(dec); dist=1000.0/plx
    ca,sa,cd,sd=np.cos(ra_r),np.sin(ra_r),np.cos(dec_r),np.sin(dec_r)
    rhat=np.column_stack([cd*ca,cd*sa,sd]); phat=np.column_stack([-sa,ca,np.zeros_like(sa)]); qhat=np.column_stack([-sd*ca,-sd*sa,cd])
    pos=(rhat*dist[:,None])@AG.T
    v=(rv[:,None]*rhat+(KAPPA*pmra/plx)[:,None]*phat+(KAPPA*pmdec/plx)[:,None]*qhat)
    return pos,(v@AG.T)
cols=dict(id='gaiadr3_source_id',ra='ra',dec='dec',plx='parallax',pmra='pmra',pmdec='pmdec',rv='rv',snr='snr',teff='teff',logg='logg',feh='fe_h')
best={}
for r in csv.DictReader(open(f'{E}/e1b_galah.csv')):
    i=r[cols['id']].strip()
    if not i or i in maskids: continue
    try: row=[float(r[cols[k]]) for k in ('ra','dec','plx','pmra','pmdec','rv','snr','teff','logg','feh')]
    except ValueError: continue
    if not all(np.isfinite(row)): continue
    if i not in best or row[6]>best[i][6]: best[i]=row
ids=list(best); arr=np.array([best[i] for i in ids])
efeh_map={}   # A1: catalogue [Fe/H] errors, read separately so the E1b selection is untouched
for r in csv.DictReader(open(f'{E}/e1b_galah.csv')):
    i=r['gaiadr3_source_id'].strip()
    if i in best:
        try:
            v=float(r['e_fe_h'])
            if np.isfinite(v) and v>0: efeh_map[i]=v
        except ValueError: pass
P,Vv=phase_space(arr[:,0],arr[:,1],arr[:,2],arr[:,3],arr[:,4],arr[:,5]); teff,logg,feh=arr[:,7],arr[:,8],arr[:,9]
n_s=len(ids); print("GALAH clean stars",n_s,flush=True)
dmean_star=np.linalg.norm(P,axis=1)
tree=cKDTree(P); pairs=tree.query_pairs(25.0,output_type='ndarray')
dxp=np.linalg.norm(P[pairs[:,0]]-P[pairs[:,1]],axis=1); dvp=np.linalg.norm(Vv[pairs[:,0]]-Vv[pairs[:,1]],axis=1)
treat=pairs[(dxp<20)&(dvp<3)]
tmean=0.5*(dmean_star[treat[:,0]]+dmean_star[treat[:,1]])
R,Lz,Jr,Jz=actions(P,Vv)
dL=np.abs(Lz[treat[:,0]]-Lz[treat[:,1]]); dz=np.abs(Jz[treat[:,0]]-Jz[treat[:,1]]); dr=np.abs(Jr[treat[:,0]]-Jr[treat[:,1]])
tauL,tauz,taur=[float(np.percentile(x,90)) for x in (dL,dz,dr)]
e1c=json.load(open(E1C))['surveys']['GALAH']
assert abs(tauL-e1c['tolerances']['tau_Lz'])<1e-3, "tolerance mismatch"
rng2=np.random.default_rng(1701)
Lm=0.5*(Lz[treat[:,0]]+Lz[treat[:,1]]); zm=0.5*(Jz[treat[:,0]]+Jz[treat[:,1]]); rm=0.5*(Jr[treat[:,0]]+Jr[treat[:,1]])
def run_tier(tier,S):   # verbatim E1c, returning pair-level data
    feats=[teff/150.0,logg/0.3,dmean_star/150.0]
    if tier>=2: feats.append(Lz/tauL)
    if tier>=3: feats.append(Jz/tauz)
    if tier>=4: feats.append(Jr/taur)
    F=np.column_stack(feats); kt=cKDTree(F)
    td=[];cd=[];tp=[];cp=[];cidx=[]
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
        td.append(abs(feh[a]-feh[b])); tp.append((a,b))
        for x,y in got: cd.append(abs(feh[x]-feh[y])); cp.append((x,y)); cidx.append(len(td)-1)
    return np.array(td),np.array(cd),np.array(tp),np.array(cp),np.array(cidx)
def replay_boot(tp_,cp_):   # e1c_run.py's stats() consumed 1000 bootstrap draws from rng2 per tier
    stars=np.unique(np.concatenate([np.array(tp_).ravel(),np.array(cp_).ravel()]))
    for _ in range(1000): rng2.integers(0,len(stars),len(stars))
for tier in (1,2,3):
    _,_,tp_,cp_,_=run_tier(tier,300.0); replay_boot(tp_,cp_)   # replay rng consumption
td,cd,tp,cp,cidx=run_tier(4,300.0)
gate=(len(td)==e1c['C4']['treat'] and len(cd)==e1c['C4']['controls']
      and round(float(np.median(td)),4)==e1c['C4']['med_treat'] and round(float(np.median(cd)),4)==e1c['C4']['med_control'])
print("C4 replay gate:", "PASS" if gate else "FAIL", len(td), len(cd), np.median(td), np.median(cd), flush=True)
if not gate: sys.exit("replay gate failed")
# ---- ages from the frozen [Y/Mg] clock ----
clock={}
with gzip.open(ABUND,'rt') as f:
    for r in csv.DictReader(f):
        try:
            if r['flag_y_fe'].strip()!='0' or r['flag_mg_fe'].strip()!='0': continue
            y,ey,mg,emg=float(r['y_fe']),float(r['e_y_fe']),float(r['mg_fe']),float(r['e_mg_fe'])
        except (ValueError,KeyError): continue
        if not all(np.isfinite([y,ey,mg,emg])): continue
        sid=r['gaiadr3_source_id'].strip()
        t=(CLOCK_A-(y-mg))/CLOCK_B; st=np.sqrt(ey**2+emg**2)/CLOCK_B
        clock[sid]=(t,st)
ta=[];sa=[];keep=[]
for k,(a,b) in enumerate(tp):
    ca_=clock.get(ids[a]); cb_=clock.get(ids[b])
    if ca_ is None or cb_ is None: continue
    w1,w2=1/ca_[1]**2,1/cb_[1]**2
    ta.append((ca_[0]*w1+cb_[0]*w2)/(w1+w2)); sa.append(np.sqrt(1/(w1+w2))); keep.append(k)
keep=np.array(keep); ta=np.array(ta); sa=np.array(sa)
print("pairs with two valid clocks:",len(keep),"of",len(td),flush=True)
d=td[keep]
ctrl_of=[cd[cidx==k] for k in keep]
_med_e=float(np.median(list(efeh_map.values())))
sig0=np.array([np.sqrt(efeh_map.get(ids[tp[k][0]],_med_e)**2+efeh_map.get(ids[tp[k][1]],_med_e)**2) for k in keep])   # A1 per-pair measurement width
print("A1: median per-pair [Fe/H] error width",round(float(np.median(sig0)),4),"stars missing e_fe_h:",sum(1 for k in keep for j in (0,1) if ids[tp[k][j]] not in efeh_map),flush=True)
# ---- bin machinery (decision: two bins; descriptive: four bins) ----
BINS2=[(0,4.5),(4.5,14)]; BINS4=[(0,2),(2,4.5),(4.5,8),(8,14)]
def binmass(t,s,bins):
    M=np.zeros((len(t),len(bins)))
    for j,(lo,hi) in enumerate(bins): M[:,j]=norm.cdf((hi-t)/s)-norm.cdf((lo-t)/s)
    M[:,0]+=norm.cdf((0-t)/s); M[:,-1]+=1-norm.cdf((14-t)/s)
    return M
edges=np.arange(0,1.0001,0.02)
def hist_density(vals):
    h,_=np.histogram(np.clip(vals,0,0.9999),bins=edges); h=h/max(h.sum(),1)/0.02
    return np.maximum(h,1e-3)
def prep(bins,t,s):
    M=binmass(t,s,bins); modal=np.argmax(M,axis=1)
    pooled=[np.concatenate([ctrl_of[i] for i in range(len(keep)) if modal[i]==b]) if np.any(modal==b) else np.array([0.2]) for b in range(len(bins))]
    G=np.array([hist_density(p) for p in pooled])
    return M,modal,G,pooled
def gval(G,dd,b): return G[b][np.minimum((np.clip(dd,0,0.9999)/0.02).astype(int),len(edges)-2)]
def gmat(G,dd): return np.column_stack([gval(G,dd,b) for b in range(len(G))])
def halfnorm(dd,s): return np.sqrt(2/np.pi)/s*np.exp(-dd**2/(2*s**2))
def nll(theta,Mm,dd,Gdd,tt=None,parametric=False,const=False,s0=None):
    s0=sig0 if s0 is None else s0
    if const: f=np.full(len(dd),theta[0]); si=theta[1]
    elif parametric: f=theta[0]*np.exp(-np.clip(tt,0,14)/theta[1]); si=theta[2]
    else: f=Mm@theta[:-1]; si=theta[-1]
    s=np.sqrt(s0**2+si**2)   # A1: per-pair conatal width = measurement + bounded intrinsic
    like=f*halfnorm(dd,s)+(1-f)*(Mm*Gdd).sum(axis=1)
    return -np.sum(np.log(np.maximum(like,1e-300)))
def fit(Mm,dd,Gdd,mode='bins',rng=None,tt=None,nstart=8,s0=None):
    rng=rng or np.random.default_rng(0); best=None; nb=Mm.shape[1]
    for _ in range(nstart):
        if mode=='bins':
            x0=np.concatenate([rng.uniform(0.05,0.8,nb),[rng.uniform(0.0,SIG_INT_MAX)]]); bnds=[(0,1)]*nb+[(0.0,SIG_INT_MAX)]
            fn=lambda th: nll(th,Mm,dd,Gdd,s0=s0)
        elif mode=='const':
            x0=[rng.uniform(0.05,0.8),rng.uniform(0.0,SIG_INT_MAX)]; bnds=[(0,1),(0.0,SIG_INT_MAX)]
            fn=lambda th: nll(th,Mm,dd,Gdd,const=True,s0=s0)
        else:
            x0=[rng.uniform(0.1,0.9),rng.uniform(0.5,8),rng.uniform(0.0,SIG_INT_MAX)]; bnds=[(0,1),(0.1,50),(0.0,SIG_INT_MAX)]
            fn=lambda th: nll(th,Mm,dd,Gdd,tt=tt,parametric=True,s0=s0)
        r=minimize(fn,x0,bounds=bnds,method='L-BFGS-B')
        if best is None or r.fun<best.fun: best=r
    return best
def simulate(fvec,s,Mm,pooled,rng):
    out=np.empty(len(fvec)); sw=np.sqrt(sig0**2+s**2)   # A1: s is the intrinsic scatter; width per pair
    for i in range(len(fvec)):
        if rng.random()<fvec[i]: out[i]=abs(rng.normal(0,sw[i]))
        else:
            b=rng.choice(len(pooled),p=Mm[i]/Mm[i].sum()); out[i]=rng.choice(np.clip(pooled[b],0,1))
    return out
def boot_fit(Mm,dd,Gdd,tp_,n=500,rng=None,nstart=3):
    rng=rng or np.random.default_rng(7)
    stars=np.unique(tp_.ravel()); smap={s:k for k,s in enumerate(stars)}; tpi=np.vectorize(smap.get)(tp_); outs=[]
    for _ in range(n):
        cnt=np.bincount(rng.integers(0,len(stars),len(stars)),minlength=len(stars))
        w=cnt[tpi[:,0]]*cnt[tpi[:,1]]; idx=np.repeat(np.arange(len(dd)),w)
        if len(idx)<20: continue
        outs.append(fit(Mm[idx],dd[idx],Gdd[idx],'bins',rng,nstart=nstart,s0=sig0[idx]).x)
    return np.array(outs)
def verdict_from(bs,fpt,n_gt_half):   # A1: shared verdict logic so the injection can measure FP/power
    Rb=bs[:,1]/np.maximum(bs[:,0],1e-6); Rlo,Rhi=np.percentile(Rb,[2.5,97.5])
    if not (n_gt_half[0]>=60 and n_gt_half[1]>=60): return 'UNDERPOWERED',Rlo,Rhi
    if Rhi<1 and Rlo>0.5: return 'MILD DECAY',Rlo,Rhi
    if Rhi<1: return 'DECAY DETECTED',Rlo,Rhi
    if Rlo>0.5: return 'PERSISTENCE',Rlo,Rhi
    return 'UNRESOLVED',Rlo,Rhi
SMOKE=(len(sys.argv)>1 and sys.argv[1]=='smoke')
M2,modal2,G2,pooled2=prep(BINS2,ta,sa); M4,modal4,G4,pooled4=prep(BINS4,ta,sa)
if SMOKE:   # synthetic substitute for the real chemistry: timing/plumbing only, reveals nothing
    _r=np.random.default_rng(3)
    d=np.array([abs(_r.normal(0,0.06)) if _r.random()<0.3 else _r.choice(np.clip(ctrl_of[i],0,1)) for i in range(len(keep))])
Gd2=gmat(G2,d); Gd4=gmat(G4,d)
n_gt_half=[int((M2[:,b]>0.5).sum()) for b in range(2)]
print("pairs with posterior mass>0.5 in decision bins:",n_gt_half,"| four-bin:",[int((M4[:,b]>0.5).sum()) for b in range(4)],flush=True)
# ---- oracle 1: constant-f simulation reproduces the observed treatment median ----
fc=fit(M2,d,Gd2,'const')
rng=np.random.default_rng(2026)
sim_meds=[np.median(simulate(np.full(len(d),fc.x[0]),fc.x[1],M2,pooled2,rng)) for _ in range(200)]
o1=dict(observed_median=round(float(np.median(d)),4),simulated_median=round(float(np.mean(sim_meds)),4),f_const=round(float(fc.x[0]),4),sigma_int_const=round(float(fc.x[1]),4),pass_=bool(abs(np.mean(sim_meds)-np.median(d))<=0.01))
print("oracle1:",o1,flush=True)
# ---- oracle 2: injection-recovery coverage on the two decision bins ----
def inject_test(ftrue_fn,nreal,rng):
    cover=np.zeros(2); widths=[]; verdicts=[]
    for _ in range(nreal):
        ttrue=np.clip(ta+rng.normal(0,sa),0,14); ftrue=ftrue_fn(ttrue)
        tobs=ttrue+rng.normal(0,sa); Mm=binmass(tobs,sa,BINS2)
        dd=simulate(ftrue,0.03,Mm,pooled2,rng); Gdd=gmat(G2,dd)   # A1: true intrinsic scatter 0.03 dex
        bs=boot_fit(Mm,dd,Gdd,tp[keep],n=(10 if SMOKE else 60),rng=rng)
        lo,hi=np.percentile(bs[:,:2],[2.5,97.5],axis=0)
        tb=np.array([ftrue[(ttrue>=l)&(ttrue<h)].mean() if np.any((ttrue>=l)&(ttrue<h)) else np.nan for (l,h) in BINS2])
        cover+=((tb>=lo)&(tb<=hi))|np.isnan(tb); widths.append(hi-lo)
        verdicts.append(verdict_from(bs,None,[int((Mm[:,b]>0.5).sum()) for b in range(2)])[0])
    widths=np.array(widths)
    return cover/nreal, np.median(widths,axis=0), verdicts
NREAL=2 if SMOKE else 200
cov_exp,w_exp,v_exp=inject_test(lambda t:0.6*np.exp(-t/1.5),NREAL,np.random.default_rng(11))
cov_const,w_const,v_const=inject_test(lambda t:np.full(len(t),0.35),NREAL,np.random.default_rng(12))
fp=sum(v in ('DECAY DETECTED','MILD DECAY') for v in v_const)/NREAL; power=sum(v in ('DECAY DETECTED','MILD DECAY') for v in v_exp)/NREAL
o2=dict(n_realisations=NREAL,coverage_exp=[round(float(x),3) for x in cov_exp],coverage_const=[round(float(x),3) for x in cov_const],
        median_width_exp=[round(float(x),3) for x in w_exp],median_width_const=[round(float(x),3) for x in w_const],
        false_positive_rate=round(fp,3),power_exp=round(power,3),
        pass_=bool(min(cov_exp.min(),cov_const.min())>=0.90 and max(w_exp.max(),w_const.max())<=0.6 and fp<=0.10))
print("oracle2:",o2,flush=True)
results=dict(script_sha256=SELF_SHA,spec='E10B-SPEC.md + E10B-AMENDMENT-1.md',n_pairs_C4=int(len(td)),n_pairs_with_clocks=int(len(keep)),
             tolerances=e1c['tolerances'],decision_bins=BINS2,descriptive_bins=BINS4,
             pairs_mass_gt_half_decision=n_gt_half,pairs_mass_gt_half_descriptive=[int((M4[:,b]>0.5).sum()) for b in range(4)],
             median_age=round(float(np.median(ta)),3),median_age_err=round(float(np.median(sa)),3),oracle1=o1,oracle2=o2)
if not (o1['pass_'] and o2['pass_']):
    results['status']='UNVALIDATED'; json.dump(results,open(f'{OUT}/e10b{TAG}_results{"_smoke" if SMOKE else ""}.json','w'),indent=1); sys.exit("oracle failed; report UNVALIDATED")
# ---- main result: decision fit (two bins) ----
fb=fit(M2,d,Gd2,'bins'); fp=fit(M2,d,Gd2,'param',tt=ta); fb4=fit(M4,d,Gd4,'bins')
print("2-bin fit:",fb.x,-fb.fun,"| const:",fc.x,-fc.fun,"| param:",fp.x,-fp.fun,"| 4-bin:",fb4.x,-fb4.fun,flush=True)
bs=boot_fit(M2,d,Gd2,tp[keep],n=(20 if SMOKE else 500),rng=np.random.default_rng(99))
lo,hi=np.percentile(bs,[2.5,97.5],axis=0)
Rpt=fb.x[1]/max(fb.x[0],1e-6)
verdict,Rlo,Rhi=verdict_from(bs,Rpt,n_gt_half)
bs4=boot_fit(M4,d,Gd4,tp[keep],n=(20 if SMOKE else 300),rng=np.random.default_rng(98))
lo4,hi4=np.percentile(bs4,[2.5,97.5],axis=0)
bsp=[]; stars=np.unique(tp[keep].ravel()); smap={s:k for k,s in enumerate(stars)}; tpi=np.vectorize(smap.get)(tp[keep]); rr=np.random.default_rng(5)
for _ in range(20 if SMOKE else 300):
    cnt=np.bincount(rr.integers(0,len(stars),len(stars)),minlength=len(stars)); w=cnt[tpi[:,0]]*cnt[tpi[:,1]]; idx=np.repeat(np.arange(len(d)),w)
    if len(idx)<20: continue
    bsp.append(fit(M2[idx],d[idx],Gd2[idx],'param',rr,tt=ta[idx],nstart=3,s0=sig0[idx]).x)
bsp=np.array(bsp)
results.update(status=('SMOKE-SYNTHETIC' if SMOKE else 'ok'),
    f_young=round(float(fb.x[0]),4),f_young_CI=[round(float(lo[0]),4),round(float(hi[0]),4)],
    f_old=round(float(fb.x[1]),4),f_old_CI=[round(float(lo[1]),4),round(float(hi[1]),4)],
    sigma_int=round(float(fb.x[2]),4),sigma_int_CI=[round(float(lo[2]),4),round(float(hi[2]),4)],median_pair_meas_width=round(float(np.median(sig0)),4),
    ratio_old_young=round(float(Rpt),4),ratio_CI=[round(float(Rlo),4),round(float(Rhi),4)],verdict=verdict,
    loglike_2bin=round(float(-fb.fun),3),loglike_const=round(float(-fc.fun),3),loglike_param=round(float(-fp.fun),3),
    param_f0=round(float(fp.x[0]),4),param_tau_gyr=round(float(fp.x[1]),3),param_tau_CI=[round(float(np.percentile(bsp[:,1],2.5)),3),round(float(np.percentile(bsp[:,1],97.5)),3)],
    f_4bin=[round(float(x),4) for x in fb4.x[:4]],f_4bin_CI=[[round(float(a),4),round(float(b),4)] for a,b in zip(lo4[:4],hi4[:4])],
    median_d_treat=round(float(np.median(d)),4))
json.dump(results,open(f'{OUT}/e10b{TAG}_results{"_smoke" if SMOKE else ""}.json','w'),indent=1)
np.savez(f'{OUT}/e10b{TAG}_pairs{"_smoke" if SMOKE else ""}.npz',d=d,ta=ta,sa=sa,M2=M2,M4=M4,G2=G2,G4=G4,boot=bs,boot4=bs4,bootp=bsp)
print(json.dumps({k:v for k,v in results.items() if k not in ('tolerances',)},indent=1)); print("DONE")
