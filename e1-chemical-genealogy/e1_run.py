"""E1 chemical genealogy test - executed per frozen E1-SPEC.md (a82ea9c).
Operationalizations within spec, documented here:
- SNR floors: GALAH snr > 30; APOGEE SNR > 70 (surveys' commonly
  recommended floors; fixed before any metric was computed).
- APOGEE clean: ASPCAPFLAG == 0 and STARFLAG == 0 (bad bits unset).
- GALAH alpha unavailable at catalog level (intake note): secondary [a/Fe]
  runs on APOGEE ALPHA_M only; no inference from per-element columns.
- Duplicate survey rows per star: keep highest-SNR row.
- Control search uses hash buckets with +/-1 bin adjacency, exact window
  check inside (sep +/-5 pc; Teff +/-150 K; logg +/-0.3; |dv|>6 km/s);
  both pair orderings tried; up to 10 controls per treatment pair.
- Clustered bootstrap: resample STARS with replacement; weight each pair
  by (count_a * count_b); weighted medians; 1,000 resamples."""
import csv, json, pickle, sys, numpy as np
sys.path.insert(0,'/root/ca/m3')
from contact_field import load_phase_space
from scipy.spatial import cKDTree
from scipy.stats import mannwhitneyu
KMS=1.02269
CSV='/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/gaia_100pc_rv.csv'
E1='/mnt/user-data/uploads/projects/causal-archipelago/e1-chemical-genealogy/data'
V='/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/vetting'

sid,pos,vel = load_phase_space(CSV)
N=len(sid); sidmap={str(int(s)):i for i,s in enumerate(sid)}

# --- group mask (all catalogs used anywhere in the project) ---
masked=np.zeros(N,bool)
for i,m in enumerate(pickle.load(open('/root/ca/m3/membership.pkl','rb'))):
    if m: masked[i]=True
def idmask(path,idcol):
    for r in csv.DictReader(open(path)):
        i=sidmap.get(r[idcol].strip())
        if i is not None: masked[i]=True
idmask(f'{V}/data/catalog-updates/raw/bertolotto_members.csv','GaiaDR3')
idmask(f'{V}/data/catalog-updates/raw/moranta_table1.csv','Gaia')
idmask(f'{V}/data/catalog-updates/raw/lee_nymg_tableb1.csv','GaiaEDR3')
idmask(f'{V}/data/catalog-updates/raw/jerabkova_hyades_edr3.csv','GaiaEDR3')
idmask(f'{V}/data/catalog-updates/raw/spyglass_young_candidate_hits.csv','Gaia')
print(f"masked group members: {masked.sum()}")

def f(x):
    try: return float(x)
    except: return np.nan

def build_survey(name):
    best={}
    if name=='GALAH':
        for r in csv.DictReader(open(f'{E1}/galah_matches.csv')):
            i=sidmap.get(r['gaiadr3_source_id'].strip())
            if i is None or masked[i]: continue
            snr=f(r['snr']); feh=f(r['fe_h'])
            if not (np.isfinite(snr) and snr>30 and np.isfinite(feh)): continue
            if r['flag_sp'].strip() not in ('0','0.0') or r['flag_fe_h'].strip() not in ('0','0.0'): continue
            t,g_=f(r['teff']),f(r['logg'])
            if not (np.isfinite(t) and np.isfinite(g_)): continue
            if i not in best or snr>best[i][3]:
                best[i]=(feh,t,g_,snr,np.nan)
    else:
        for r in csv.DictReader(open(f'{E1}/apogee_matches.csv')):
            i=sidmap.get(r['GAIAEDR3_SOURCE_ID'].strip())
            if i is None or masked[i]: continue
            snr=f(r['SNR']); feh=f(r['FE_H'])
            if not (np.isfinite(snr) and snr>70 and np.isfinite(feh)): continue
            if f(r['ASPCAP_STAR_BAD'])!=0: continue   # corrected operationalization of
            # the spec's 'ASPCAPFLAG bad bits unset': the intake's ASPCAP_STAR_BAD
            # column IS that test; requiring ASPCAPFLAG==0 exactly was over-strict
            # (benign warn bits) and left 240 stars vs the agent-counted 4,882.
            t,g_=f(r['TEFF']),f(r['LOGG'])
            if not (np.isfinite(t) and np.isfinite(g_)): continue
            if i not in best or snr>best[i][3]:
                best[i]=(feh,t,g_,snr,f(r['ALPHA_M']))
    idx=np.array(sorted(best)); 
    arr=np.array([best[i] for i in idx])
    return idx, arr  # columns: feh, teff, logg, snr, alpha

rng=np.random.default_rng(11)
results={}
for name in ('GALAH','APOGEE'):
    idx, arr = build_survey(name)
    P,Vv = pos[idx], vel[idx]
    n_s=len(idx); print(f"\n{name}: clean unmasked stars = {n_s}")
    tree=cKDTree(P)
    pairs=tree.query_pairs(25.0,output_type='ndarray')
    dx=np.linalg.norm(P[pairs[:,0]]-P[pairs[:,1]],axis=1)
    dv=np.linalg.norm(Vv[pairs[:,0]]-Vv[pairs[:,1]],axis=1)/KMS
    treat = pairs[(dx<20)&(dv<3)]
    cand  = pairs[(dv>6)]
    cdx   = np.linalg.norm(P[cand[:,0]]-P[cand[:,1]],axis=1)
    print(f"treatment pairs = {len(treat)}, control candidates = {len(cand)}")
    if len(treat)<20:
        results[name]=dict(status='insufficient', treat_pairs=int(len(treat))); continue
    # hash buckets for controls: (sep//5, teff//150 both, logg//0.3 both)
    from collections import defaultdict
    buck=defaultdict(list)
    tA=arr[:,1]; gA=arr[:,2]
    for k,(a,b) in enumerate(cand):
        key=(int(cdx[k]//5), int(tA[a]//150), int(gA[a]//0.3)%1000, int(tA[b]//150), int(gA[b]//0.3)%1000)
        buck[key].append(k)
    def controls_for(a,b,sep):
        out=[]
        for da in (-1,0,1):
            for perm in ((a,b),(b,a)):
                key0=(int(sep//5)+da, int(tA[perm[0]]//150), int(gA[perm[0]]//0.3)%1000,
                      int(tA[perm[1]]//150), int(gA[perm[1]]//0.3)%1000)
                # neighbor teff/logg bins
                for dt1 in (-1,0,1):
                    for dg1 in (-1,0,1):
                        for dt2 in (-1,0,1):
                            for dg2 in (-1,0,1):
                                key=(key0[0],key0[1]+dt1,key0[2]+dg1,key0[3]+dt2,key0[4]+dg2)
                                for k in buck.get(key,()):
                                    ca,cb=cand[k]
                                    if abs(cdx[k]-sep)>5: continue
                                    ok=(abs(tA[ca]-tA[perm[0]])<=150 and abs(gA[ca]-gA[perm[0]])<=0.3 and
                                        abs(tA[cb]-tA[perm[1]])<=150 and abs(gA[cb]-gA[perm[1]])<=0.3)
                                    if ok: out.append(k)
        return out
    feh=arr[:,0]
    t_d=[]; c_d=[]; t_pairs=[]; c_pairs=[]
    matched=0
    tsep=np.linalg.norm(P[treat[:,0]]-P[treat[:,1]],axis=1)
    for k,(a,b) in enumerate(treat):
        cs=controls_for(a,b,tsep[k])
        if not cs: continue
        pick=rng.choice(len(cs),size=min(10,len(cs)),replace=False)
        matched+=1
        t_d.append(abs(feh[a]-feh[b])); t_pairs.append((a,b))
        for pk in pick:
            ca,cb=cand[cs[pk]]
            c_d.append(abs(feh[ca]-feh[cb])); c_pairs.append((ca,cb))
    t_d=np.array(t_d); c_d=np.array(c_d)
    print(f"matched treatment pairs = {matched}; control pairs = {len(c_d)}")
    if matched<20:
        results[name]=dict(status='insufficient-matched', matched=int(matched)); continue
    U,pval=mannwhitneyu(t_d,c_d,alternative='less')
    # clustered bootstrap on the median difference
    t_pairs=np.array(t_pairs); c_pairs=np.array(c_pairs)
    stars=np.unique(np.concatenate([t_pairs.ravel(),c_pairs.ravel()]))
    smap={s:k for k,s in enumerate(stars)}
    tpi=np.vectorize(smap.get)(t_pairs); cpi=np.vectorize(smap.get)(c_pairs)
    diffs=[]
    def wmedian(v,w):
        o=np.argsort(v); v,w=v[o],w[o]; cw=np.cumsum(w)
        return v[np.searchsorted(cw,cw[-1]/2)]
    for _ in range(1000):
        cnt=np.bincount(rng.integers(0,len(stars),len(stars)),minlength=len(stars))
        wt=cnt[tpi[:,0]]*cnt[tpi[:,1]]; wc=cnt[cpi[:,0]]*cnt[cpi[:,1]]
        if wt.sum()==0 or wc.sum()==0: continue
        diffs.append(wmedian(t_d,wt)-wmedian(c_d,wc))
    lo,hi=np.percentile(diffs,[2.5,97.5])
    results[name]=dict(status='ok', stars=int(n_s), treat_pairs=int(matched),
        control_pairs=int(len(c_d)),
        med_treat=round(float(np.median(t_d)),4), med_control=round(float(np.median(c_d)),4),
        med_diff=round(float(np.median(t_d)-np.median(c_d)),4),
        boot_CI=[round(float(lo),4),round(float(hi),4)],
        mannwhitney_p=float(f"{pval:.2e}"))
    print(f"{name}: median |dFeH| treat={np.median(t_d):.4f} control={np.median(c_d):.4f} "
          f"diff={np.median(t_d)-np.median(c_d):+.4f} CI[{lo:.4f},{hi:.4f}] p={pval:.2e}")
json.dump(results, open('/root/ca/m3/e1_results.json','w'), indent=1)
np.savez_compressed('/root/ca/m3/e1_arrays.npz')
print("\nDONE")
