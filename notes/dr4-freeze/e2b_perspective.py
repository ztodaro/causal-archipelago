"""B4 - El-Badry (2019) perspective term for the E2b wide-binary statistic, per frozen B2-B4-SPEC.md.
(1) correct_perspective(): per-pair correction for use once radial velocities are joined.
(2) Statistical quantification on the sealed bins + perspective-inclusive anchors (no RVs in hand)."""
import json, hashlib, numpy as np
SELF_SHA=hashlib.sha256(open(__file__,'rb').read()).hexdigest()
OUT='/root/ca/fresh/dr4'
AU_PC_RAD=4.848136811e-6      # 1 arcsec in radians; theta[rad] = (sep_AU / d_pc) * this

def correct_perspective(dv_ra,dv_dec,v_r,theta_rad,e_hat):
    """Remove the apparent tangential-velocity difference v_r*theta induced by the two lines of sight.
    dv_*: observed velocity-difference components (km/s, star2 - star1); v_r: systemic RV (km/s);
    theta_rad: angular separation; e_hat: unit vector on the sky from star1 to star2 (ra, dec components)."""
    p=v_r*theta_rad
    return dv_ra-p*e_hat[0], dv_dec-p*e_hat[1]

def _selftest(rng):
    """Inject a known common velocity, verify the correction recovers the uncorrected vector."""
    worst=0.0
    for _ in range(2000):
        v_r=rng.normal(0,30); theta=rng.uniform(1e-5,5e-3); ang=rng.uniform(0,2*np.pi); e=(np.cos(ang),np.sin(ang))
        true=(rng.normal(0,0.3),rng.normal(0,0.3))
        obs=(true[0]+v_r*theta*e[0],true[1]+v_r*theta*e[1])
        rec=correct_perspective(obs[0],obs[1],v_r,theta,e)
        worst=max(worst,abs(rec[0]-true[0]),abs(rec[1]-true[1]))
    return worst

z=np.load('/root/ca/e2b/e2b_cal_arrays.npz')
A0=1.2e-10
vtp,e_vtp,gN=z['vtp'],z['e_vtp'],z['gN']; sep,dmean,vcirc=z['sep'],z['dmean'],z['vcirc']
bound,primary,sealed=z['bound'],z['primary'],z['sealed']
m=bound&primary
hi=m&(gN>10*A0)&(gN<100*A0); lo=m&(gN>0.1*A0)&(gN<A0); fl=m&(gN>0.1*A0)&(gN<0.3*A0)
theta=(sep/dmean)*AU_PC_RAD                    # radians
tmpl=vtp[m&~sealed&(gN>10*A0)]
res=dict(script_sha256=SELF_SHA,selftest_max_abs_residual=float(_selftest(np.random.default_rng(1))),bins={})
for name,mask in (('calibration_10_100a0',hi),('decision_0.1_1a0',lo),('flicker_0.1_0.3a0',fl)):
    b={'n':int(mask.sum()),'theta_rad_p50':float(np.median(theta[mask])),'vcirc_kms_p50':float(np.median(vcirc[mask])),
       'e_vtp_p50':float(np.median(e_vtp[mask]))}
    for s in (20.0,25.0,30.0):
        d=np.abs(np.random.default_rng(7).normal(0,s,mask.sum()))*theta[mask]/vcirc[mask]
        b[f'delta_p50_sigma{int(s)}']=round(float(np.median(d)),5); b[f'delta_p90_sigma{int(s)}']=round(float(np.percentile(d,90)),5)
    res['bins'][name]=b
    print(name,b,flush=True)
# perspective-inclusive anchors: e2b_inject.py's forward model + a signed offset v_r*theta/vcirc along a fixed sky axis
def anchors(sigma_vr,nmc=400,seed=2026):
    rng=np.random.default_rng(seed)
    ilo,ihi,ifl=np.where(lo)[0],np.where(hi)[0],np.where(fl)[0]
    def draw(idx,boost):
        vt=rng.choice(tmpl,idx.size)*boost; ph=rng.uniform(0,2*np.pi,idx.size)
        p=(rng.normal(0,sigma_vr,idx.size)*theta[idx]/vcirc[idx]) if sigma_vr>0 else 0.0
        return np.hypot(vt*np.cos(ph)+rng.normal(0,e_vtp[idx])+p, vt*np.sin(ph)+rng.normal(0,e_vtp[idx]))
    out={}
    for lab,boost in (('newton',1.0),('mond',1.2)):
        rat=[];flm=[]
        for _ in range(nmc):
            ol=draw(ilo,boost); oh=draw(ihi,1.0); of=draw(ifl,boost)
            rat.append(np.median(ol)/np.median(oh)); flm.append(np.median(of))
        rat=np.array(rat); flm=np.array(flm)
        out[lab]=dict(primary_ratio=[round(float(np.median(rat)),4),round(float(np.percentile(rat,2.5)),4),round(float(np.percentile(rat,97.5)),4)],
                      flicker_median=[round(float(np.median(flm)),4),round(float(np.percentile(flm,2.5)),4),round(float(np.percentile(flm,97.5)),4)])
    return out
res['anchors_no_perspective_reproduction']=anchors(0.0)
for s in (20.0,25.0,30.0): res[f'anchors_perspective_sigma{int(s)}']=anchors(s)
res['frozen_anchors']=dict(primary=dict(newton=[1.115,1.070,1.160],mond=[1.299,1.238,1.356]),flicker=dict(newton=[0.682,0.639,0.726],mond=[0.788,0.737,0.841]))
res['unsealed_data']=dict(primary=[1.104,1.063,1.164],flicker=[0.699,0.640,0.733])
for k in ('anchors_no_perspective_reproduction','anchors_perspective_sigma20','anchors_perspective_sigma25','anchors_perspective_sigma30'): print(k,res[k],flush=True)
json.dump(res,open(f'{OUT}/b4_perspective.json','w'),indent=1); print("DONE")
