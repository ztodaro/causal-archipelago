"""Paper I triple-model stress test (post-audit hold-lifter).
Question: how large can unresolved-triple contamination bias the E2b
PRIMARY ratio, across adversarial variations of the parametric model,
including a no-screens worst case? Compare the bias envelope to the
0.18 Newton-MOND anchor separation.

Grid: companion frequency {0.2, 0.3, 0.5} x detection-threshold scale
{0.5, 1, 2, inf} x period distribution {raghavan (mu=5.03, sig=2.28),
wide (sig=3.0), loguniform [1 d, 3e5 yr]}. 12 realizations per cell.
Machinery identical to e2b_inject.py (committed, anchored); only the
varied parameters differ. Seeded."""
import json
import numpy as np

z = np.load('/root/ca/e2b/e2b_cal_arrays.npz')
A0 = 1.2e-10; KAPPA = 4.740470446e-3; T_GAIA = 2.83
vtp, e_vtp, gN = z['vtp'], z['e_vtp'], z['gN']
dmean, Mtot, vcirc = z['dmean'], z['Mtot'], z['vcirc']
bound, primary, sealed = z['bound'], z['primary'], z['sealed']
gmag1, gmag2 = z['gmag1'], z['gmag2']
m = bound & primary
hi = m & (gN > 10*A0) & (gN < 100*A0)
lo = m & (gN > 0.1*A0) & (gN < A0)
tmpl = vtp[m & ~sealed & (gN > 10*A0)]
rng = np.random.default_rng(818)
det_G = np.array([13., 15., 17., 19.]); det_S0 = np.array([0.08, 0.15, 0.40, 0.80])
idx_all = np.where(m)[0]
ilo, ihi = np.where(lo)[0], np.where(hi)[0]
pos_lo = np.searchsorted(idx_all, ilo); pos_hi = np.searchsorted(idx_all, ihi)

def draw_period(kind, n):
    if kind == 'raghavan': return 10**rng.normal(5.03, 2.28, n)/365.25
    if kind == 'wide':     return 10**rng.normal(5.03, 3.00, n)/365.25
    lo_, hi_ = np.log10(1/365.25), np.log10(3e5)
    return 10**rng.uniform(lo_, hi_, n)

def run_cell(freq, thr_scale, pkind, nreal=12):
    biases = []
    for _ in range(nreal):
        has3 = rng.random((idx_all.size, 2)) < freq
        q = rng.uniform(0.1, 1.0, idx_all.size)
        P = draw_period(pkind, idx_all.size)
        Mh = Mtot[idx_all]*0.5
        a = (Mh*(1+q)*P**2)**(1/3.)
        l = q**4
        a_ph = a*(q/(1+q) - l/(1+l))
        dmu_res = np.where(P >= T_GAIA, 2*np.pi*a_ph/P, (2*np.pi*a_ph/T_GAIA)*(P/T_GAIA))
        dmu_mas = dmu_res/dmean[idx_all]*1000.0
        wob = a_ph/dmean[idx_all]*1000.0
        Gh = np.minimum(gmag1[idx_all], gmag2[idx_all])
        any3 = has3.any(axis=1)
        if np.isinf(thr_scale):
            survive = any3
        else:
            thr = np.interp(np.clip(Gh, det_G[0], det_G[-1]), det_G, det_S0)*thr_scale
            survive = any3 & ~(wob > thr)
        dvt = np.where(survive, KAPPA*dmu_mas*dmean[idx_all]/vcirc[idx_all], 0.0)
        def med(idx, pos):
            vt = rng.choice(tmpl, idx.size)
            ph = rng.uniform(0, 2*np.pi, idx.size)
            o = np.hypot(vt + dvt[pos]*np.cos(ph), dvt[pos]*np.sin(ph))
            o = np.hypot(o + rng.normal(0, e_vtp[idx]), rng.normal(0, e_vtp[idx]))
            return np.median(o)
        r_tr = med(ilo, pos_lo)/med(ihi, pos_hi)
        # noise-only reference within same realization
        dvt0 = np.zeros_like(dvt)
        def med0(idx):
            vt = rng.choice(tmpl, idx.size)
            ph = rng.uniform(0, 2*np.pi, idx.size)
            o = np.hypot(vt, 0.0)
            o = np.hypot(o + rng.normal(0, e_vtp[idx]), rng.normal(0, e_vtp[idx]))
            return np.median(o)
        r_0 = med0(ilo)/med0(ihi)
        biases.append(r_tr - r_0)
    b = np.array(biases)
    return float(b.mean()), float(b.std())

cells = []
for freq in (0.2, 0.3, 0.5):
    for thr in (0.5, 1.0, 2.0, np.inf):
        for pk in ('raghavan', 'wide', 'loguniform'):
            mb, sb = run_cell(freq, thr, pk)
            cells.append(dict(freq=freq, thr_scale=('none' if np.isinf(thr) else thr),
                              periods=pk, bias=round(mb, 4), sd=round(sb, 4)))
            print(cells[-1], flush=True)
worst = max(cells, key=lambda c: abs(c['bias']))
out = dict(grid_cells=len(cells), anchor_gap=0.18,
           worst=worst, max_abs_bias=abs(worst['bias']),
           envelope_ok=bool(abs(worst['bias']) < 0.06),
           cells=cells)
json.dump(out, open('/root/ca/e2b/e2b_stress.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'cells'}, indent=1))
