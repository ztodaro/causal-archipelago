"""E2b INJECTION + NOISE MC (open phase, pre-anchoring). Seeded, parametric.

(A) Noise MC: forward-model the PRIMARY ratio statistic under Newton (B=1)
and under the preregistered MOND-scale alternative (B=1.2 in the decision
bin), using each sealed-bin pair's REAL per-pair vtilde error (from the
four catalog PM errors) but never its measured vtilde. True-vtilde template
= empirical calibration-region (g>10a0) distribution. Output: noise-adjusted
decision anchors R_Newton and R_MOND with MC scatter.

(B) PM-reflex triple injection: unresolved companions displace the
photocenter; long-period companions add a nearly constant PM offset that
survives clean-astrometry screens, short-period ones average out but bloat
RUWE/aen. Model survival with a magnitude-dependent angular-wobble
detection threshold, propagate surviving offsets into the ratio, report
contamination fraction f and ratio bias dR.

Assumptions (documented for the report): companion frequency per component
30%; q ~ U(0.1,1); lognormal logP(days) mu=5.03 sig=2.28 (Raghavan 2010);
flux ratio l=q^4; photocenter a_ph = a*(q/(1+q) - l/(1+l)); Gaia baseline
T=2.83 yr; period-averaged PM offset envelope: 2*pi*a_ph/P for P>=T,
(2*pi*a_ph/T)*(P/T) for P<T; wobble detection threshold sigma_det(G) =
interp[(13,0.08),(15,0.15),(17,0.40),(19,0.80)] mas (RUWE/aen/ipd proxy).
"""
import json
import numpy as np

z = np.load('/root/ca/e2b/e2b_cal_arrays.npz')
A0 = 1.2e-10; KAPPA = 4.740470446e-3; T_GAIA = 2.83  # yr
vtp, e_vtp, gN = z['vtp'], z['e_vtp'], z['gN']
sep, dmean, Mtot, vcirc = z['sep'], z['dmean'], z['Mtot'], z['vcirc']
bound, primary, sealed = z['bound'], z['primary'], z['sealed']
gmag1, gmag2 = z['gmag1'], z['gmag2']
m = bound & primary
hi = m & (gN > 10*A0) & (gN < 100*A0)
lo = m & (gN > 0.1*A0) & (gN < A0)
lo_fl = m & (gN > 0.1*A0) & (gN < 0.3*A0)
# template of "true" vtilde: calibration region, mildly deconvolved is
# overkill (median error 0.07 << median 0.58); use empirical values
tmpl = vtp[m & ~sealed & (gN > 10*A0)]
rng = np.random.default_rng(2026)

def forward_ratio(boost_lo, nmc=400):
    """predicted median-lo/median-hi under noise; boost applies to lo bin."""
    ilo, ihi = np.where(lo)[0], np.where(hi)[0]
    out = []
    for _ in range(nmc):
        vt_lo = rng.choice(tmpl, ilo.size) * boost_lo
        vt_hi = rng.choice(tmpl, ihi.size)
        phl = rng.uniform(0, 2*np.pi, ilo.size)
        phh = rng.uniform(0, 2*np.pi, ihi.size)
        ol = np.hypot(vt_lo*np.cos(phl) + rng.normal(0, e_vtp[ilo]),
                      vt_lo*np.sin(phl) + rng.normal(0, e_vtp[ilo]))
        oh = np.hypot(vt_hi*np.cos(phh) + rng.normal(0, e_vtp[ihi]),
                      vt_hi*np.sin(phh) + rng.normal(0, e_vtp[ihi]))
        out.append(np.median(ol)/np.median(oh))
    return np.array(out)

rN = forward_ratio(1.0)
rM = forward_ratio(1.2)
res = dict(
    n_hi=int(hi.sum()), n_lo=int(lo.sum()), n_flicker=int(lo_fl.sum()),
    median_evtp_lo=round(float(np.median(e_vtp[lo])), 4),
    median_evtp_hi=round(float(np.median(e_vtp[hi])), 4),
    R_newton=dict(mean=round(float(rN.mean()), 4),
                  ci=[round(float(np.percentile(rN, 2.5)), 4),
                      round(float(np.percentile(rN, 97.5)), 4)]),
    R_mond=dict(mean=round(float(rM.mean()), 4),
                ci=[round(float(np.percentile(rM, 2.5)), 4),
                    round(float(np.percentile(rM, 97.5)), 4)]))

# ---------------- (B) triple injection ----------------
GSOL = 4*np.pi**2  # AU^3 / (yr^2 Msun)
det_G = np.array([13., 15., 17., 19.]); det_S = np.array([0.08, 0.15, 0.40, 0.80])
NREAL = 20
fr_survive, fr_flagged, dRs = [], [], []
idx_all = np.where(m)[0]
for _ in range(NREAL):
    has3 = rng.random(idx_all.size*2).reshape(-1, 2) < 0.30  # per component
    # host = component 1 or 2 (mass split ~ half Mtot each is adequate here)
    q = rng.uniform(0.1, 1.0, idx_all.size)
    logP = rng.normal(5.03, 2.28, idx_all.size)   # log10 days
    P = 10**logP/365.25                            # yr
    Mh = Mtot[idx_all]*0.5
    a = (Mh*(1+q)*P**2)**(1/3.)         # AU (Kepler, G=4pi^2 units)
    l = q**4
    a_ph = a*(q/(1+q) - l/(1+l))
    dmu_res = np.where(P >= T_GAIA, 2*np.pi*a_ph/P, (2*np.pi*a_ph/T_GAIA)*(P/T_GAIA))
    dmu_res_mas = dmu_res/dmean[idx_all]*1000.0    # AU/yr at d pc -> mas/yr
    wobble_mas = a_ph/dmean[idx_all]*1000.0
    Ghost = np.minimum(gmag1[idx_all], gmag2[idx_all])
    thresh = np.interp(np.clip(Ghost, det_G[0], det_G[-1]), det_G, det_S)
    any3 = has3.any(axis=1)
    flagged = any3 & (wobble_mas > thresh)
    survive = any3 & ~flagged
    fr_survive.append(survive.mean()); fr_flagged.append(flagged.mean())
    # ratio bias: add surviving offset vectorially to lo/hi bin vtildes
    dv_kms = KAPPA*dmu_res_mas*dmean[idx_all]
    dvt = np.where(survive, dv_kms/vcirc[idx_all], 0.0)
    ilo = np.where(lo)[0]; ihi = np.where(hi)[0]
    pos_lo = np.searchsorted(idx_all, ilo); pos_hi = np.searchsorted(idx_all, ihi)
    vt_lo = rng.choice(tmpl, ilo.size); vt_hi = rng.choice(tmpl, ihi.size)
    ph = rng.uniform(0, 2*np.pi, ilo.size); ph2 = rng.uniform(0, 2*np.pi, ihi.size)
    ol = np.hypot(vt_lo + dvt[pos_lo]*np.cos(ph), dvt[pos_lo]*np.sin(ph))
    oh = np.hypot(vt_hi + dvt[pos_hi]*np.cos(ph2), dvt[pos_hi]*np.sin(ph2))
    # add measurement noise too, for a realistic combined anchor
    ol = np.hypot(ol + rng.normal(0, e_vtp[ilo]), rng.normal(0, e_vtp[ilo]))
    oh = np.hypot(oh + rng.normal(0, e_vtp[ihi]), rng.normal(0, e_vtp[ihi]))
    dRs.append(np.median(ol)/np.median(oh))
dRs = np.array(dRs)
res['triples'] = dict(
    companion_freq_assumed=0.30,
    frac_pairs_with_surviving_triple=round(float(np.mean(fr_survive)), 4),
    frac_pairs_flagged_by_screens=round(float(np.mean(fr_flagged)), 4),
    R_newton_with_triples=dict(mean=round(float(dRs.mean()), 4),
                               ci=[round(float(np.percentile(dRs, 2.5)), 4),
                                   round(float(np.percentile(dRs, 97.5)), 4)]),
    ratio_bias_vs_noise_only=round(float(dRs.mean() - rN.mean()), 4))
json.dump(res, open('/root/ca/e2b/e2b_inject.json', 'w'), indent=1)
print(json.dumps(res, indent=1))
