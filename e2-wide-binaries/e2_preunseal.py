"""E2 pre-unseal steps 1-3. Calibration region ONLY; the seal is untouched.
Step 1: inspect the El-Badry non-overlap pairs.
Step 2: synthetic hierarchical-triple injection - measure how unresolved
  companions inflate vtilde_perp AFTER our screens, and calibrate the
  observed 14.3% tail to an implied contamination fraction.
Step 3: measurement-noise MC (12 realizations): parallax errors (per-star),
  PM errors (DR3 magnitude-based approximation, documented), 10% lognormal
  mass error."""
import csv, json, sys, numpy as np
sys.path.insert(0,'/root/ca/m3')
from contact_field import load_phase_space
KMS=1.02269; KAPPA=4.740470446
G_SI=6.674e-11; MSUN=1.989e30; AU=1.495978707e11
CSV='/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/gaia_100pc_rv.csv'
E2='/mnt/user-data/uploads/projects/causal-archipelago/e2-wide-binaries/data'
sid,pos,vel = load_phase_space(CSV)
g=np.genfromtxt(CSV,delimiter=',',names=True)
z=np.load('/root/ca/m3/e2_cal_pairs.npz')
pairs,dx,Mtot,gN = z['pairs'],z['dx'],z['Mtot'],z['gN']
vcirc=np.sqrt(G_SI*Mtot*MSUN/(dx*AU))/1000.0
d=0.5*(np.linalg.norm(pos[pairs[:,0]],axis=1)+np.linalg.norm(pos[pairs[:,1]],axis=1))
def vperp_of(pm_ra,pm_dec):
    dmu=np.hypot(pm_ra[pairs[:,0]]-pm_ra[pairs[:,1]],pm_dec[pairs[:,0]]-pm_dec[pairs[:,1]])
    return 4.740470446e-3*dmu*d
vtp0 = vperp_of(g['pmra'],g['pmdec'])/vcirc

# ---- Step 1: non-overlap inspection ----
eb={}; comp=set()
for r in csv.DictReader(open(f'{E2}/elbadry_nearby.csv')):
    a,b=r['source_id1'].strip(),r['source_id2'].strip()
    eb[frozenset((a,b))]=r; comp.add(a); comp.add(b)
insp=[]; no_idx=[]
for k,(a,b) in enumerate(pairs):
    key=frozenset((str(int(sid[a])),str(int(sid[b]))))
    if key in eb: continue
    no_idx.append(k)
    ga,gb=str(int(sid[a])),str(int(sid[b]))
    insp.append(dict(pair=k,ids=[ga,gb],sep_AU=round(float(dx[k]),0),
        dist_pc=round(float(d[k]),1),vtilde_perp=round(float(vtp0[k]),2),
        G=[round(float(g['phot_g_mean_mag'][a]),1),round(float(g['phot_g_mean_mag'][b]),1)],
        in_elbadry_with_other=[ga in comp, gb in comp]))
no_idx=np.array(no_idx)
if len(no_idx):
    Gmax=np.array([max(x['G']) for x in insp]); Gmin=np.array([min(x['G']) for x in insp])
    vt_no=vtp0[no_idx]; vt_yes=np.delete(vtp0,no_idx)
    print(f"non-overlaps: {len(no_idx)}/{len(pairs)}  bright(minG<8): {int((Gmin<8).sum())}  "
          f"vtilde med {np.median(vt_no):.2f} (overlap med {np.median(vt_yes):.2f})  "
          f"tail>sqrt2 {np.mean(vt_no>np.sqrt(2)):.2f} vs {np.mean(vt_yes>np.sqrt(2)):.2f}",flush=True)
    for x in insp[:3]: print("example:",json.dumps(x),flush=True)

# ---- Step 2: triple injection ----
rng=np.random.default_rng(21)
NINJ=4000
m1 = np.minimum(Mtot[rng.integers(0,len(pairs),NINJ)],1.2)  # host mass draw from sample scale
q  = rng.uniform(0.1,1.0,NINJ)
a_in = 10**rng.uniform(-1,1.48,NINJ)     # 0.1 - 30 AU
v_orb = np.sqrt(G_SI*(m1*(1+q))*MSUN/(a_in*AU))/1000.0 * (q/(1+q))  # reflex speed km/s
# random orientation: project onto sky (2 of 3 components) and LOS (1)
u=rng.normal(size=(NINJ,3)); u/=np.linalg.norm(u,axis=1)[:,None]
v_ref = v_orb[:,None]*u
# host pair template: draw a real calibration pair for each injection
tpl = rng.integers(0,len(pairs),NINJ)
vc_t = vcirc[tpl]; vt_true = vtp0[tpl]
# screens: (a) RV screen: |LOS reflex| adds to rv_error budget; our sample cut
# rv_error<1.5 and vetting rv_amplitude<10 -> approximate surviving screen:
# reject injected systems whose LOS reflex exceeds 4 km/s (would inflate
# Gaia rv_error / show amplitude); (b) selection cut |dv3D| < 2 vcirc.
los_ok = np.abs(v_ref[:,2]) < 4.0
dv3d_new = np.sqrt((vt_true*vc_t)**2 + v_orb**2)  # conservative: add in quadrature
sel_ok = dv3d_new < 2*vc_t
surv = los_ok & sel_ok
# vtilde_perp of survivors: sky components of reflex add to pair dv_perp
dvp_new = np.sqrt((vt_true*vc_t)**2 + v_ref[:,0]**2 + v_ref[:,1]**2)
vtp_inj = (dvp_new/vc_t)[surv]
print(f"\ninjection: {NINJ} triples -> screens pass {surv.mean():.1%}")
print(f"survivor vtilde_perp: median {np.median(vtp_inj):.2f}, frac>sqrt2 {np.mean(vtp_inj>np.sqrt(2)):.2f}")
# mixture calibration: observed tail T = (1-f)*t_clean + f*t_triple
t_clean_guess = 0.05   # bound Newtonian pairs measurement-noise tail (from step 3)
t_triple = float(np.mean(vtp_inj>np.sqrt(2)))
obs_tail = float(np.mean(vtp0>np.sqrt(2)))
f_implied = max(0.0,(obs_tail-t_clean_guess)/(t_triple-t_clean_guess)) if t_triple>t_clean_guess else None
print(f"observed tail {obs_tail:.3f} -> implied contamination f ≈ {f_implied:.2f} (clean-tail prior {t_clean_guess})")
med_inflation = {}
for f in (0.0,0.1,0.15,0.2):
    mix=np.concatenate([vtp0[rng.random(len(vtp0))>f], rng.choice(vtp_inj,size=int(f*len(vtp0)))]) if f>0 else vtp0
    med_inflation[f]=round(float(np.median(mix)),3)
print("median vtilde vs contamination f:",med_inflation)

# ---- Step 3: noise MC ----
def sigma_pm(G):
    return np.where(G<14,0.03,np.where(G<15,0.045,np.where(G<16,0.07,0.12)))  # mas/yr, DR3-era approx
meds=[]; tails=[]
for s in range(12):
    r=np.random.default_rng(300+s)
    plx = g['parallax'] + r.normal(0,1,len(sid))*g['parallax_error']
    scale = g['parallax']/plx                       # distance rescale factor
    d_n = d * 0.5*(scale[pairs[:,0]]+scale[pairs[:,1]])
    pmra_n = g['pmra'] + r.normal(0,1,len(sid))*sigma_pm(g['phot_g_mean_mag'])
    pmdec_n= g['pmdec']+ r.normal(0,1,len(sid))*sigma_pm(g['phot_g_mean_mag'])
    dmu=np.hypot(pmra_n[pairs[:,0]]-pmra_n[pairs[:,1]],pmdec_n[pairs[:,0]]-pmdec_n[pairs[:,1]])
    vperp_n = 4.740470446e-3*dmu*d_n
    M_n = Mtot*np.exp(r.normal(0,0.1,len(pairs)))
    sep_n = dx * 0.5*(scale[pairs[:,0]]+scale[pairs[:,1]])
    vc_n = np.sqrt(G_SI*M_n*MSUN/(sep_n*AU))/1000.0
    vt_n = vperp_n/vc_n
    meds.append(float(np.median(vt_n))); tails.append(float(np.mean(vt_n>np.sqrt(2))))
print(f"\nnoise MC: median vtilde {np.mean(meds):.3f} ± {np.std(meds):.3f}; tail {np.mean(tails):.3f} ± {np.std(tails):.3f}")
json.dump(dict(nonoverlap=insp,
    injection=dict(n=NINJ, screen_pass=round(float(surv.mean()),3),
        survivor_tail=t_triple, observed_tail=obs_tail,
        implied_f=round(float(f_implied),3) if f_implied is not None else None,
        median_vs_f=med_inflation),
    noise_mc=dict(median=round(float(np.mean(meds)),3), median_sd=round(float(np.std(meds)),4),
        tail=round(float(np.mean(tails)),3), tail_sd=round(float(np.std(tails)),4))),
    open('/root/ca/m3/e2_preunseal.json','w'), indent=1)
print("DONE")
