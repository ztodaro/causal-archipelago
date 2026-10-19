"""E2b CALIBRATION - open region (g_N > 10 a0) only. Frozen spec: E2B-SPEC.md
at d0cf4a7; intake e9f60cd (SHA 4a8d9cd8..., 125,713 rows). The sealed region
(g_N < 10 a0) is COUNTED but its vtilde statistics are never computed here.

Selection (spec): both Plx >= 5 mas; R_chance_align < 0.01 primary
(< 0.1 labeled variant); per component RUWE < 1.4, IPDfmp <= 2, sepsi < 2,
RPlx >= 20; parallaxes consistent within 3 sigma; sep 500-50,000 AU
(catalog sepAU); no component appearing in any other intake pair.
Carried over from E2: bound-pair screen in PM-only form (vtilde_perp < 2),
Mamajek M_G->mass, observable vtilde_perp = dv_perp / v_circ(s_proj)."""
import json
import numpy as np
import pandas as pd

G_SI = 6.674e-11; MSUN = 1.989e30; AU = 1.495978707e11; A0 = 1.2e-10
KAPPA = 4.740470446e-3  # km/s per (mas/yr * pc)

df = pd.read_csv('/root/ca/e2b/e2b_trim.csv', dtype={'Source1': str, 'Source2': str})
n0 = len(df)

# --- duplicate-component screen (within the frozen intake, R<0.1 either-plx>=5) ---
from collections import Counter
cnt = Counter(df['Source1']); cnt.update(df['Source2'])
dup = df['Source1'].map(cnt).gt(1) | df['Source2'].map(cnt).gt(1)

# --- per-row selection ---
plx_ok = (df['Plx1'] >= 5) & (df['Plx2'] >= 5)
qual = ((df['RUWE1'] < 1.4) & (df['RUWE2'] < 1.4) &
        (df['IPDfmp1'] <= 2) & (df['IPDfmp2'] <= 2) &
        (df['sepsi1'] < 2) & (df['sepsi2'] < 2) &
        (df['RPlx1'] >= 20) & (df['RPlx2'] >= 20))
plx_cons = (np.abs(df['Plx1'] - df['Plx2']) <
            3 * np.sqrt(df['e_Plx1']**2 + df['e_Plx2']**2))
sep_ok = (df['sepAU'] > 500) & (df['sepAU'] < 50000)
# Spec-implied clarification (open phase, pre-anchoring): the frozen mass
# prescription (Mamajek M_G->mass) is defined only for main-sequence stars,
# so both components must be classified MS: BinType == 'MSMS'.
msms = df['BinType'] == 'MSMS'
base = plx_ok & qual & plx_cons & sep_ok & msms & ~dup & df['R'].notna()
steps = dict(intake=n0,
             both_plx_ge5=int(plx_ok.sum()),
             after_quality=int((plx_ok & qual).sum()),
             after_plx_consistency=int((plx_ok & qual & plx_cons).sum()),
             after_sep=int((plx_ok & qual & plx_cons & sep_ok).sum()),
             after_msms=int((plx_ok & qual & plx_cons & sep_ok & msms).sum()),
             after_dup_screen=int(base.sum()),
             dup_components_dropped=int((plx_ok & qual & plx_cons & sep_ok & msms & dup).sum()))
d = df[base].reset_index(drop=True)

# --- masses: Mamajek v2022.04.16 M_G -> mass (same parser as E2) ---
MGs, Ms = [], []
for line in open('/mnt/user-data/uploads/projects/causal-archipelago/e2-wide-binaries/data/mamajek_dwarf_table.txt'):
    if line.startswith('#') or not line.strip(): continue
    p = line.split()
    if len(p) < 31: continue
    try: mg = float(p[13]); m = float(p[30])
    except ValueError: continue
    MGs.append(mg); Ms.append(m)
MGs = np.array(MGs); Ms = np.array(Ms)
o = np.argsort(MGs); MGs, Ms = MGs[o], Ms[o]
u, ui = np.unique(MGs, return_index=True); MGs, Ms = u, Ms[ui]
def m_of(gmag, plx):
    MG = gmag + 5*np.log10(plx) - 10
    return np.interp(np.clip(MG, MGs.min(), MGs.max()), MGs, Ms), MG
m1, MG1 = m_of(d['Gmag1'].values, d['Plx1'].values)
m2, MG2 = m_of(d['Gmag2'].values, d['Plx2'].values)
Mtot = m1 + m2

# --- observable ---
dist1 = 1000.0/d['Plx1'].values; dist2 = 1000.0/d['Plx2'].values
dmean = 0.5*(dist1 + dist2)
sep = d['sepAU'].values
vcirc = np.sqrt(G_SI*Mtot*MSUN/(sep*AU))/1000.0            # km/s
dmu = np.hypot(d['pmRA1'].values - d['pmRA2'].values,
               d['pmDE1'].values - d['pmDE2'].values)       # mas/yr
dvp = KAPPA*dmu*dmean                                       # km/s
vtp = dvp/vcirc
gN = G_SI*Mtot*MSUN/(sep*AU)**2
# per-pair vtilde error from real PM errors (all four components)
e_dmu = np.sqrt(d['e_pmRA1'].values**2 + d['e_pmRA2'].values**2
              + d['e_pmDE1'].values**2 + d['e_pmDE2'].values**2) / np.sqrt(2)
# (isotropic 1-sigma per axis; magnitude error of a 2-vector with equal axis errors)
e_vtp = KAPPA*e_dmu*dmean/vcirc

# --- carried-over bound screen ---
bound = vtp < 2
primary = d['R'].values < 0.01

sealed = gN < 10*A0
cal = ~sealed
res = dict(spec='E2B-SPEC.md@d0cf4a7', intake='e9f60cd', steps=steps,
           after_bound_screen=int(bound.sum()),
           primary_R001=int((bound & primary).sum()),
           variant_R01=int(bound.sum()),
           sealed_counts=dict(
               primary=int((bound & primary & sealed).sum()),
               variant=int((bound & sealed).sum()),
               primary_01_03=int((bound & primary & (gN < 0.3*A0) & (gN > 0.1*A0)).sum()),
               primary_01_1=int((bound & primary & (gN < A0) & (gN > 0.1*A0)).sum())),
           )

# --- CALIBRATION-REGION statistics (open) ---
def calstats(mask, label):
    out = {}
    for lo_, hi_, name in [(10, 100, 'g10_100'), (100, 1e9, 'g_gt100')]:
        m = mask & cal & (gN > lo_*A0) & (gN < hi_*A0) & bound
        v = vtp[m]
        out[name] = dict(n=int(m.sum()),
                         median=round(float(np.median(v)), 4) if m.sum() else None,
                         p25=round(float(np.percentile(v, 25)), 4) if m.sum() else None,
                         p75=round(float(np.percentile(v, 75)), 4) if m.sum() else None,
                         median_evtp=round(float(np.median(e_vtp[m])), 4) if m.sum() else None)
    # bound-screen sensitivity, calibration region only
    m_all = mask & cal & (gN > 10*A0) & (gN < 100*A0)
    out['bound_screen_kept_frac_10_100'] = round(float((vtp[m_all] < 2).mean()), 4) if m_all.sum() else None
    return out
res['calibration'] = dict(primary=calstats(primary, 'primary'),
                          variant=calstats(np.ones(len(d), bool), 'variant'))

# --- El-Badry-internal consistency checks (open region) ---
# theta is in DEGREES; catalog sepAU = theta*3600 * (1000/Plx1)
theta_sep = d['theta'].values*3600.0*(1000.0/d['Plx1'].values)
chk = np.abs(theta_sep - sep)/sep
res['consistency'] = dict(
    sep_recompute_med_relerr=round(float(np.median(chk)), 5),
    pm_err_p50_masyr=round(float(np.median(e_dmu)), 4),
    pm_err_p90_masyr=round(float(np.percentile(e_dmu, 90)), 4),
    dist_p50_pc=round(float(np.median(dmean)), 1),
    dist_p90_pc=round(float(np.percentile(dmean, 90)), 1),
    mg_range=[round(float(min(MG1.min(), MG2.min())), 2), round(float(max(MG1.max(), MG2.max())), 2)],
    mtot_p50=round(float(np.median(Mtot)), 3))

np.savez_compressed('/root/ca/e2b/e2b_cal_arrays.npz',
    vtp=vtp, e_vtp=e_vtp, gN=gN, sep=sep, dmean=dmean, Mtot=Mtot,
    vcirc=vcirc, bound=bound, primary=primary, sealed=sealed,
    gmag1=d['Gmag1'].values, gmag2=d['Gmag2'].values,
    e_dmu=e_dmu, ruwe1=d['RUWE1'].values, ruwe2=d['RUWE2'].values)
json.dump(res, open('/root/ca/e2b/e2b_cal.json', 'w'), indent=1)
print(json.dumps(res, indent=1))
