"""E2 CALIBRATION-REGION build. SEAL DISCIPLINE: pairs with g_N < 10*a0 are
filtered out immediately after computation and never counted, printed,
stored, or examined. Only the calibration region (g_N > 10*a0) is analyzed.
Per E2-SPEC.md (a82ea9c). Mass-luminosity: Mamajek table v2022.04.16
(M_G -> Msun interpolation, main sequence), documented here as the
relation choice BEFORE any velocity statistic was computed."""
import csv, json, sys, numpy as np
sys.path.insert(0,'/root/ca/m3')
from contact_field import load_phase_space
from scipy.spatial import cKDTree
KMS_MS = 1000.0                      # km/s -> m/s
A0 = 1.2e-10                         # m/s^2
G_SI = 6.674e-11; MSUN=1.989e30; AU=1.495978707e11; PC_AU=206264.8
CSV='/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/gaia_100pc_rv.csv'
E2='/mnt/user-data/uploads/projects/causal-archipelago/e2-wide-binaries/data'

sid,pos,vel = load_phase_space(CSV)      # pc, pc/Myr
KMS=1.02269
N=len(sid)
g=np.genfromtxt(CSV,delimiter=',',names=True)
MG_star = g['phot_g_mean_mag']+5*np.log10(g['parallax'])-10

# Mamajek M_G -> mass
MGs=[]; Ms=[]
for line in open(f'{E2}/mamajek_dwarf_table.txt'):
    if line.startswith('#') or not line.strip(): continue
    p=line.split()
    if len(p)<31: continue
    try:
        mg=float(p[13]); m=float(p[30])
        MGs.append(mg); Ms.append(m)
    except ValueError: continue
MGs=np.array(MGs); Ms=np.array(Ms)
o=np.argsort(MGs); MGs,Ms=MGs[o],Ms[o]
u,ui=np.unique(MGs,return_index=True); MGs,Ms=u,Ms[ui]
mass = np.interp(np.clip(MG_star,MGs.min(),MGs.max()),MGs,Ms)
print(f"Mamajek rows parsed: {len(MGs)}; sample mass range {mass.min():.2f}-{mass.max():.2f} Msun")

# quality screens from the vetting-field pull are NOT available sample-wide;
# sample-wide screens per spec use canonical CSV fields: ruwe<1.4 (already),
# rv_error<1.5. Remaining spec screens (ipd, aen, rv_amplitude) exist only
# for the 259-cohort; DOCUMENTED LIMITATION: applied where available later;
# calibration proceeds with rv_error + ruwe + resolved-triple screens.
rverr_ok = g['radial_velocity_error'] < 1.5

# candidate pairs: separation window in AU
tree=cKDTree(pos)
# CORRECTION (caught in calibration, per spec): separation must be PROJECTED.
# 3D separation is invalid here - the radial component is parallax-noise
# dominated (sigma_dd ~ 10^4 AU >> true separations). Search generously in
# 3D (|dd|<0.5pc consistency bounds the radial term), then compute projected
# separation = angular separation x mean distance and cut on THAT.
pairs = tree.query_pairs(0.6, output_type='ndarray')   # generous 3D search
u = pos/np.linalg.norm(pos,axis=1)[:,None]
dmean = 0.5*(np.linalg.norm(pos[pairs[:,0]],axis=1)+np.linalg.norm(pos[pairs[:,1]],axis=1))
cosang = np.clip(np.sum(u[pairs[:,0]]*u[pairs[:,1]],axis=1),-1,1)
theta = np.arccos(cosang)
dx = theta*dmean*PC_AU     # projected separation in AU
keep = (dx>500)&(dx<30000)
pairs, dx = pairs[keep], dx[keep]
# parallax/distance consistency
d1=np.linalg.norm(pos[pairs[:,0]],axis=1); d2=np.linalg.norm(pos[pairs[:,1]],axis=1)
keep = np.abs(d1-d2)<0.5
pairs,dx = pairs[keep],dx[keep]
# velocity bound: |dv| < 2*vcirc
Mtot = mass[pairs[:,0]]+mass[pairs[:,1]]
vcirc = np.sqrt(G_SI*Mtot*MSUN/(dx*AU))/KMS_MS      # km/s
dv3d = np.linalg.norm(vel[pairs[:,0]]-vel[pairs[:,1]],axis=1)/KMS  # km/s
keep = (dv3d < 2*vcirc) & rverr_ok[pairs[:,0]] & rverr_ok[pairs[:,1]]
pairs,dx,Mtot,vcirc,dv3d = pairs[keep],dx[keep],Mtot[keep],vcirc[keep],dv3d[keep]
# resolved-triple screen: no third sample star within 10,000 AU of either
third = np.zeros(len(pairs),bool)
r10k = 10000/PC_AU
neigh = tree.query_ball_point(pos, r10k)
for k,(a,b) in enumerate(pairs):
    na=set(neigh[a])-{a,b}; nb=set(neigh[b])-{a,b}
    if na or nb: third[k]=True
pairs,dx,Mtot,vcirc,dv3d = pairs[~third],dx[~third],Mtot[~third],vcirc[~third],dv3d[~third]
print(f"selected pairs (all regions, pre-seal): {len(pairs)}")

# --- SEAL: compute g_N, split, discard sealed immediately ---
gN = G_SI*Mtot*MSUN/(dx*AU)**2
cal = gN > 10*A0
pairs,dx,Mtot,vcirc,dv3d = pairs[cal],dx[cal],Mtot[cal],vcirc[cal],dv3d[cal]
gN = gN[cal]
print(f"CALIBRATION region pairs (gN>10a0): {len(pairs)}  [sealed region not counted]")

vt = dv3d/vcirc
res = dict(n_cal=int(len(pairs)),
    sep_AU=dict(min=float(dx.min()) if len(dx) else None, med=float(np.median(dx)) if len(dx) else None,
                max=float(dx.max()) if len(dx) else None),
    vtilde=dict(median=float(np.median(vt)) if len(vt) else None,
                p25=float(np.percentile(vt,25)) if len(vt) else None,
                p75=float(np.percentile(vt,75)) if len(vt) else None,
                frac_above_sqrt2=float(np.mean(vt>np.sqrt(2))) if len(vt) else None))
print("calibration vtilde:", json.dumps(res['vtilde']))

# El-Badry overlap (calibration pairs only)
eb=set()
for r in csv.DictReader(open(f'{E2}/elbadry_nearby.csv')):
    eb.add(frozenset((r['source_id1'].strip(), r['source_id2'].strip())))
ours=[frozenset((str(int(sid[a])),str(int(sid[b])))) for a,b in pairs]
inb=sum(1 for p in ours if p in eb)
res['elbadry_overlap']=dict(ours=len(ours), in_elbadry=inb,
    frac=round(inb/len(ours),3) if ours else None)
print(f"El-Badry overlap: {inb}/{len(ours)}")
json.dump(res, open('/root/ca/m3/e2_calibration.json','w'), indent=1)
np.savez_compressed('/root/ca/m3/e2_cal_pairs.npz',
    pairs=pairs, dx=dx, Mtot=Mtot, vtilde=vt, gN=gN)
print("DONE")
