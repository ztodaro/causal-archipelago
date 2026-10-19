"""E10 - the forgetting curve. Chemistry is the fixed ruler (birth [Fe/H]
never decays); what decays is the INFORMATIVENESS of kinematic linkage.
Measure: the E1b chemical twin excess of kinematically linked pairs as a
function of [Y/Mg] clock age -> the disk's kinematic memory decay curve,
with matched-control rigor. Secondary: clock-age agreement fraction of
linked pairs vs controls per bin.

Machinery inherited VERBATIM from e1b_run.py (masking, phase space,
pairing, control matching, clustered bootstrap); age lane per E8's frozen
clock (Nissen 2016, validity box). GALAH decision lane only (APOGEE C/N
deferred, documented). Two phases: --power (counts only, run BEFORE the
spec freeze) and --full (excess computation, run only after E10-SPEC.md
is committed).
"""
import csv, json, pickle, sys, argparse
import numpy as np
import importlib.util
spec = importlib.util.spec_from_file_location('d40', '/root/ca/m3/d40_full_standalone.py')
d40 = importlib.util.module_from_spec(spec); spec.loader.exec_module(d40)
AG = d40.AG; KAPPA = 4.740470446
from scipy.spatial import cKDTree
from scipy import sparse
from scipy.sparse.csgraph import connected_components

E = '/mnt/user-data/uploads/projects/causal-archipelago/e1-chemical-genealogy/data'
V = '/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/vetting'
C = '/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/crossmatch-catalogs/raw'
CLOCK_A, CLOCK_B = 0.170, 0.0371
BINS = [(0.0, 2.0), (2.0, 4.5), (4.5, 8.0)]

# ---- mask (identical to E1b) ----
maskids = set()
def addmask(path, col):
    for r in csv.DictReader(open(path)):
        v = r[col].strip()
        if v: maskids.add(v)
addmask(f'{E}/e1b_cg_members.csv', 'GaiaDR2')
addmask(f'{C}/theia_clustered_sources.csv', 'Gaia')
addmask(f'{V}/data/catalog-updates/raw/bertolotto_members.csv', 'GaiaDR3')
addmask(f'{V}/data/catalog-updates/raw/moranta_table1.csv', 'Gaia')
addmask(f'{V}/data/catalog-updates/raw/lee_nymg_tableb1.csv', 'GaiaEDR3')
addmask(f'{V}/data/catalog-updates/raw/jerabkova_hyades_edr3.csv', 'GaiaEDR3')
addmask(f'{V}/data/catalog-updates/raw/spyglass_young_candidate_hits.csv', 'Gaia')
g0 = np.genfromtxt('/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/gaia_100pc_rv.csv',
                   delimiter=',', names=True, usecols=(0,), dtype=None, encoding='utf-8')
sids0 = [str(int(x)) for x in np.atleast_1d(g0['source_id'])]
for i, m in enumerate(pickle.load(open('/root/ca/m3/membership.pkl', 'rb'))):
    if m: maskids.add(sids0[i])
print(f'mask ids: {len(maskids)}', flush=True)

def phase_space(ra, dec, plx, pmra, pmdec, rv):
    ra_r, dec_r = np.radians(ra), np.radians(dec)
    dist = 1000.0/plx
    ca, sa, cd, sd = np.cos(ra_r), np.sin(ra_r), np.cos(dec_r), np.sin(dec_r)
    rhat = np.column_stack([cd*ca, cd*sa, sd])
    phat = np.column_stack([-sa, ca, np.zeros_like(sa)])
    qhat = np.column_stack([-sd*ca, -sd*sa, cd])
    pos = (rhat*dist[:, None]) @ AG.T
    v = (rv[:, None]*rhat + (KAPPA*pmra/plx)[:, None]*phat + (KAPPA*pmdec/plx)[:, None]*qhat)
    return pos, v @ AG.T

# ---- load GALAH (e8 abundance table; E1b-style cleaning) ----
best = {}
for r in csv.DictReader(open('/root/ca/e8/e8_galah_abund.csv')):
    i = r['gaiadr3_source_id'].strip()
    if not i or i in maskids: continue
    try:
        row = [float(r[k]) for k in ('ra', 'dec', 'parallax', 'pmra', 'pmdec',
                                     'rv_galah', 'snr_c3_iraf', 'teff', 'logg', 'fe_h')]
    except (ValueError, KeyError): continue
    if not all(np.isfinite(row)): continue
    if row[2] <= 0 or abs(row[5]) > 400: continue
    flags_ok = all(r.get(f, '1').strip() in ('0', '0.0') for f in
                   ('flag_sp', 'flag_fe_h'))
    clock_ok = (flags_ok and
                all(r.get(f, '1').strip() in ('0', '0.0') for f in ('flag_y_fe', 'flag_mg_fe'))
                and row[6] >= 30 and 5200 <= row[7] <= 6300 and row[8] >= 3.5)
    t = np.nan
    if clock_ok:
        try:
            ymg = float(r['y_fe']) - float(r['mg_fe'])
            t = (CLOCK_A - ymg)/CLOCK_B
        except ValueError:
            t = np.nan
    if i not in best or row[6] > best[i][0][6]:
        best[i] = (row, t, flags_ok)
ids = list(best)
arr = np.array([best[i][0] for i in ids])
tclock = np.array([best[i][1] for i in ids])
ok_feh = np.array([best[i][2] for i in ids])
print(f'clean unmasked stars: {len(ids)}; with valid clock: {int(np.isfinite(tclock).sum())}', flush=True)
P, Vv = phase_space(arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3], arr[:, 4], arr[:, 5])
teff, logg, feh = arr[:, 7], arr[:, 8], arr[:, 9]
dmean_star = np.linalg.norm(P, axis=1)

tree = cKDTree(P)
pairs = tree.query_pairs(25.0, output_type='ndarray')
dxp = np.linalg.norm(P[pairs[:, 0]] - P[pairs[:, 1]], axis=1)
dvp = np.linalg.norm(Vv[pairs[:, 0]] - Vv[pairs[:, 1]], axis=1)
treat = pairs[(dxp < 20) & (dvp < 3)]
cand = pairs[dvp > 6]
print(f'treatment pairs={len(treat)}  control candidates={len(cand)}', flush=True)

t1, t2 = tclock[treat[:, 0]], tclock[treat[:, 1]]
both = np.isfinite(t1) & np.isfinite(t2)
agree = both & (np.abs(t1 - t2) < 3.0)
page = np.where(agree, 0.5*(t1 + t2), np.nan)
gph = sparse.coo_matrix((np.ones(len(treat)), (treat[:, 0], treat[:, 1])),
                        shape=(len(ids), len(ids)))
_, lab = connected_components(gph, directed=False)

counts = []
for lo, hi in BINS:
    m = agree & (page >= lo) & (page < hi)
    ncl = len(np.unique(lab[treat[m][:, 0]])) if m.sum() else 0
    counts.append(dict(bin=f'{lo}-{hi}', pairs_aged=int(m.sum()), clusters=int(ncl)))
    print(f'bin {lo}-{hi}: aged pairs={m.sum()} clusters={ncl}', flush=True)
print(f'both-clock pairs={int(both.sum())}; age-consistent={int(agree.sum())}', flush=True)
json.dump(dict(counts=counts, both=int(both.sum()), agree=int(agree.sum()),
               treat=int(len(treat))), open('/root/ca/e7/e10_power.json', 'w'), indent=1)
if '--power' in sys.argv:
    print('POWER PHASE ONLY - stopping before any excess computation.'); sys.exit(0)

# ================= FULL PHASE (only after E10-SPEC.md committed) =================
rng = np.random.default_rng(1010)
from collections import defaultdict
cdx = np.linalg.norm(P[cand[:, 0]] - P[cand[:, 1]], axis=1)
cmean = 0.5*(dmean_star[cand[:, 0]] + dmean_star[cand[:, 1]])
buck = defaultdict(list)
for k in range(len(cand)):
    a, b = cand[k]
    buck[(int(cdx[k]//5), int(teff[a]//150), int(logg[a]//0.3) % 1000,
          int(teff[b]//150), int(logg[b]//0.3) % 1000, int(cmean[k]//150))].append(k)
tsep = np.linalg.norm(P[treat[:, 0]] - P[treat[:, 1]], axis=1)
tmean = 0.5*(dmean_star[treat[:, 0]] + dmean_star[treat[:, 1]])

def controls_for(k, a, b):
    cs = []
    for da in (-1, 0, 1):
        for dm in (-1, 0, 1):
            for perm in ((a, b), (b, a)):
                for dt1 in (-1, 0, 1):
                    for dg1 in (-1, 0, 1):
                        for dt2 in (-1, 0, 1):
                            for dg2 in (-1, 0, 1):
                                key = (int(tsep[k]//5)+da, int(teff[perm[0]]//150)+dt1,
                                       (int(logg[perm[0]]//0.3) % 1000)+dg1,
                                       int(teff[perm[1]]//150)+dt2,
                                       (int(logg[perm[1]]//0.3) % 1000)+dg2,
                                       int(tmean[k]//150)+dm)
                                for kk in buck.get(key, ()):
                                    ca_, cb_ = cand[kk]
                                    if abs(cdx[kk]-tsep[k]) > 5: continue
                                    if abs(cmean[kk]-tmean[k]) > 150: continue
                                    if (abs(teff[ca_]-teff[perm[0]]) <= 150 and abs(logg[ca_]-logg[perm[0]]) <= 0.3
                                            and abs(teff[cb_]-teff[perm[1]]) <= 150 and abs(logg[cb_]-logg[perm[1]]) <= 0.3):
                                        cs.append(kk)
    return cs

def wmed(v, w):
    o = np.argsort(v); v, w = v[o], w[o]; cw = np.cumsum(w)
    return v[np.searchsorted(cw, cw[-1]/2)]

results = dict(spec='E10-SPEC.md', bins=[])
for lo, hi in BINS:
    sel = np.where(agree & (page >= lo) & (page < hi))[0]
    t_d, c_d, t_pairs, c_pairs, ctrl_dt, treat_dt = [], [], [], [], [], []
    matched = 0
    for k in sel:
        a, b = treat[k]
        cs = controls_for(k, a, b)
        if not cs: continue
        pick = rng.choice(len(cs), size=min(10, len(cs)), replace=False)
        matched += 1
        t_d.append(abs(feh[a]-feh[b])); t_pairs.append((a, b))
        treat_dt.append(abs(t1[k]-t2[k]))
        for pk in pick:
            ca_, cb_ = cand[cs[pk]]
            c_d.append(abs(feh[ca_]-feh[cb_])); c_pairs.append((ca_, cb_))
            if np.isfinite(tclock[ca_]) and np.isfinite(tclock[cb_]):
                ctrl_dt.append(abs(tclock[ca_]-tclock[cb_]))
    t_d, c_d = np.array(t_d), np.array(c_d)
    out = dict(bin=f'{lo}-{hi}', matched=int(matched), controls=int(len(c_d)))
    ncl = len(np.unique(lab[treat[sel][:, 0]])) if len(sel) else 0
    out['clusters'] = int(ncl)
    if matched < 25 or ncl < 15:
        out['status'] = 'underpowered'
        if matched:   # descriptive point estimates only, per spec reporting rule
            out.update(med_treat=round(float(np.median(t_d)), 4),
                       med_ctrl=round(float(np.median(c_d)), 4),
                       excess_descriptive=round(float(np.median(t_d)-np.median(c_d)), 4),
                       sec_treat_dt_med=round(float(np.median(treat_dt)), 2) if treat_dt else None,
                       sec_ctrl_dt_med=round(float(np.median(ctrl_dt)), 2) if ctrl_dt else None)
        results['bins'].append(out); print(out, flush=True); continue
    t_pairs = np.array(t_pairs); c_pairs = np.array(c_pairs)
    stars = np.unique(np.concatenate([t_pairs.ravel(), c_pairs.ravel()]))
    smap = {s: k2 for k2, s in enumerate(stars)}
    tpi = np.vectorize(smap.get)(t_pairs); cpi = np.vectorize(smap.get)(c_pairs)
    diffs = []
    for _ in range(1000):
        cnt = np.bincount(rng.integers(0, len(stars), len(stars)), minlength=len(stars))
        wt = cnt[tpi[:, 0]]*cnt[tpi[:, 1]]; wc = cnt[cpi[:, 0]]*cnt[cpi[:, 1]]
        if wt.sum() == 0 or wc.sum() == 0: continue
        diffs.append(wmed(t_d, wt) - wmed(c_d, wc))
    lo95, hi95 = np.percentile(diffs, [2.5, 97.5])
    out.update(med_treat=round(float(np.median(t_d)), 4),
               med_ctrl=round(float(np.median(c_d)), 4),
               excess=round(float(np.median(t_d)-np.median(c_d)), 4),
               CI=[round(float(lo95), 4), round(float(hi95), 4)],
               excludes_zero=bool(hi95 < 0),
               sec_treat_dt_med=round(float(np.median(treat_dt)), 2) if treat_dt else None,
               sec_ctrl_dt_med=round(float(np.median(ctrl_dt)), 2) if ctrl_dt else None)
    results['bins'].append(out); print(out, flush=True)
json.dump(results, open('/root/ca/e7/e10_results.json', 'w'), indent=1)
print('E10 DONE', flush=True)
