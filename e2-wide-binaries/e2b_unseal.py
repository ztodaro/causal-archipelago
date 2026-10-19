"""E2b UNSEAL - sealed region computed ONCE, on owner instruction only.
Frozen at pre-unseal (this file committed BEFORE anchoring; never edited
after). Spec: E2B-SPEC.md@d0cf4a7; intake e9f60cd; calibration
e2b_cal.py/e2b_inject.py outputs committed alongside.

Decision framework (frozen):
  PRIMARY  : median vtilde ratio [0.1-1]a0 / [10-100]a0, R<0.01 sample,
             10,000 pair-bootstrap CI. Noise-adjusted anchors:
             R_Newton = 1.115 [1.070, 1.160]; R_MOND = 1.299 [1.238, 1.356].
  SECONDARY: median vtilde in [0.1-0.3]a0 (flicker bin), anchors
             Newton 0.682 [0.639, 0.726]; MOND 0.788 [0.737, 0.841].
  VARIANTS (labeled, robustness): (a) R<0.1 sample, same anchors as
             primary; (b) precision-trimmed e_vtp<0.15, anchors
             Newton 1.009 [0.942, 1.075]; MOND 1.198 [1.129, 1.274].
  Verdict  : symmetric. Report point + CI; state which anchors the CI
             excludes. Primary decides; variants qualify robustness.
  Small-N  : n_low < 500 in the primary -> reduced-power flag.
"""
import json
import numpy as np

z = np.load('/root/ca/e2b/e2b_cal_arrays.npz')
A0 = 1.2e-10
vtp, e_vtp, gN = z['vtp'], z['e_vtp'], z['gN']
bound, primary = z['bound'], z['primary']

ANCH = dict(primary=dict(newton=[1.115, 1.070, 1.160], mond=[1.299, 1.238, 1.356]),
            trim=dict(newton=[1.009, 0.942, 1.075], mond=[1.198, 1.129, 1.274]),
            flicker=dict(newton=[0.682, 0.639, 0.726], mond=[0.788, 0.737, 0.841]))
rng = np.random.default_rng(424242)

def ratio_ci(mask):
    hi = mask & (gN > 10*A0) & (gN < 100*A0)
    lo = mask & (gN > 0.1*A0) & (gN < A0)
    ilo, ihi = np.where(lo)[0], np.where(hi)[0]
    ratio = float(np.median(vtp[ilo])/np.median(vtp[ihi]))
    rs = np.empty(10000)
    for k in range(10000):
        rs[k] = (np.median(vtp[rng.choice(ilo, ilo.size)]) /
                 np.median(vtp[rng.choice(ihi, ihi.size)]))
    return dict(n_low=int(ilo.size), n_high=int(ihi.size),
                median_low=round(float(np.median(vtp[ilo])), 4),
                median_high=round(float(np.median(vtp[ihi])), 4),
                RATIO=round(ratio, 4),
                CI95=[round(float(np.percentile(rs, 2.5)), 4),
                      round(float(np.percentile(rs, 97.5)), 4)])

def flicker_ci(mask):
    fl = mask & (gN > 0.1*A0) & (gN < 0.3*A0)
    i = np.where(fl)[0]
    ms = np.empty(10000)
    for k in range(10000):
        ms[k] = np.median(vtp[rng.choice(i, i.size)])
    return dict(n=int(i.size), MEDIAN=round(float(np.median(vtp[i])), 4),
                CI95=[round(float(np.percentile(ms, 2.5)), 4),
                      round(float(np.percentile(ms, 97.5)), 4)])

def verdict(ci, anch):
    lo95, hi95 = ci
    out = []
    for h in ('newton', 'mond'):
        c, alo, ahi = anch[h]
        out.append(f"{h}: {'EXCLUDED' if (hi95 < alo or lo95 > ahi) else 'not excluded'}")
    return '; '.join(out)

res = dict(spec='E2B-SPEC.md@d0cf4a7', anchors=ANCH)
res['PRIMARY'] = ratio_ci(bound & primary)
res['PRIMARY']['vs_anchors'] = verdict(res['PRIMARY']['CI95'], ANCH['primary'])
res['PRIMARY']['reduced_power_flag'] = bool(res['PRIMARY']['n_low'] < 500)
res['SECONDARY_flicker'] = flicker_ci(bound & primary)
res['SECONDARY_flicker']['vs_anchors'] = verdict(res['SECONDARY_flicker']['CI95'], ANCH['flicker'])
res['variant_R01'] = ratio_ci(bound)
res['variant_R01']['vs_anchors'] = verdict(res['variant_R01']['CI95'], ANCH['primary'])
res['variant_trim'] = ratio_ci(bound & primary & (e_vtp < 0.15))
res['variant_trim']['vs_anchors'] = verdict(res['variant_trim']['CI95'], ANCH['trim'])

# acceleration profile for the figure (both regions, computed at unseal only)
bins = np.array([0.1, 0.3, 1, 3, 10, 30, 100])*A0
prof = []
m = bound & primary
for i in range(len(bins)-1):
    mm = m & (gN >= bins[i]) & (gN < bins[i+1])
    if mm.sum() >= 3:
        prof.append(dict(bin_lo_a0=round(bins[i]/A0, 2), bin_hi_a0=round(bins[i+1]/A0, 2),
                         n=int(mm.sum()), med=round(float(np.median(vtp[mm])), 4)))
res['profile'] = prof
json.dump(res, open('/root/ca/e2b/e2b_UNSEALED.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'profile'}, indent=1))
print('UNSEALED')
