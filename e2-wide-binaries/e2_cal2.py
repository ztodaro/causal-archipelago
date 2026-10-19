"""Calibration refinement: PM-based vtilde_perp (the spec's primary
observable) on the same 112 calibration pairs. RV-based 3D vtilde is
demoted to diagnostic (RV errors ~ vcirc). Also: NaN-mass accounting."""
import json, numpy as np, sys
sys.path.insert(0,'/root/ca/m3')
from contact_field import load_phase_space
KAPPA=4.740470446
CSV='/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/gaia_100pc_rv.csv'
sid,pos,vel = load_phase_space(CSV)
g=np.genfromtxt(CSV,delimiter=',',names=True)
z=np.load('/root/ca/m3/e2_cal_pairs.npz')
pairs,dx,Mtot,vt3,gN = z['pairs'],z['dx'],z['Mtot'],z['vtilde'],z['gN']
G_SI=6.674e-11; MSUN=1.989e30; AU=1.495978707e11
vcirc=np.sqrt(G_SI*Mtot*MSUN/(dx*AU))/1000.0
d = 0.5*(np.linalg.norm(pos[pairs[:,0]],axis=1)+np.linalg.norm(pos[pairs[:,1]],axis=1))
dmu = np.hypot(g['pmra'][pairs[:,0]]-g['pmra'][pairs[:,1]],
               g['pmdec'][pairs[:,0]]-g['pmdec'][pairs[:,1]])
vperp = KAPPA*1e-3*dmu*d*1000.0/1000.0   # mas/yr * pc -> km/s : 4.74047e-3*dmu*d
vperp = 4.740470446e-3*dmu*d
vtp = vperp/vcirc
ok=np.isfinite(vtp)
print(f"pairs with finite vtilde_perp: {ok.sum()}/{len(vtp)} (NaN masses from blank G mags: {np.isnan(Mtot).sum()})")
v=vtp[ok]
out=dict(n=int(ok.sum()),
  vtilde_perp=dict(median=round(float(np.median(v)),3),
    p25=round(float(np.percentile(v,25)),3), p75=round(float(np.percentile(v,75)),3),
    frac_above_sqrt2=round(float(np.mean(v>np.sqrt(2))),3),
    frac_above_2=round(float(np.mean(v>2)),3)))
print(json.dumps(out,indent=1))
json.dump(out, open('/root/ca/m3/e2_cal_perp.json','w'), indent=1)
