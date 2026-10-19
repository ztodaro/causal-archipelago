"""E8 solar-sibling sieve - implements E8-SPEC.md frozen at 28d308e
(SHA f2f249a1...) EXACTLY. Chemistry leads; kinematics ranks; GOLD needs
the 13-element vector. Symmetric reporting; kill condition automatic.

Usage: python3 e8_sieve.py [--galah PATH] [--apogee PATH] [--smoke]
"""
import argparse, csv, json, sys
import numpy as np
import pandas as pd

# ---- frozen constants (spec) ----
T_SUN = 4.568
R0 = 8.2            # kpc
VC = 233.1          # km/s
USUN, VSUN, WSUN = 11.1, 12.24, 7.25
LZ_SUN = R0*(VC + VSUN)          # 2011.8 kpc km/s
NU = 73.5           # km/s/kpc
KAP = 40.2          # km/s/kpc
CLOCK_A, CLOCK_B = 0.170, 0.0371   # t = (A - [Y/Mg])/B
YMG_TOL = 0.056
LZ_WIN, JZ_MAX, JR_MAX = 500.0, 25.0, 20.0
ELEMS = ['Na','Mg','Al','Si','Ca','Ti','Cr','Mn','Ni','Cu','Zn','Y','Ba']
WMAD_MAX, NVALID_MIN, EFLOOR = 0.040, 8, 0.03
KAPPA_PM = 4.740470446e-3
# galactic rotation matrix (ICRS->galactic), as in d40_full_standalone
AG = np.array([[-0.0548755604162154, -0.8734370902348850, -0.4838350155487132],
               [ 0.4941094278755837, -0.4448296299600112,  0.7469822444972189],
               [-0.8676661490190047, -0.1980763734312015,  0.4559837761750669]])

def phase_space(ra, dec, plx, pmra, pmdec, rv):
    ra_r, dec_r = np.radians(ra), np.radians(dec)
    dist = 1000.0/plx  # pc
    ca, sa, cd, sd = np.cos(ra_r), np.sin(ra_r), np.cos(dec_r), np.sin(dec_r)
    rhat = np.column_stack([cd*ca, cd*sa, sd])
    phat = np.column_stack([-sa, ca, np.zeros_like(sa)])
    qhat = np.column_stack([-sd*ca, -sd*sa, cd])
    pos = (rhat*dist[:, None]) @ AG.T
    v = (rv[:, None]*rhat + (1000*KAPPA_PM*pmra/plx)[:, None]*phat
         + (1000*KAPPA_PM*pmdec/plx)[:, None]*qhat)
    return pos, v @ AG.T   # pc, km/s (heliocentric galactic)

def actions(pos, vel):
    """axisymmetric actions per frozen constants; pos pc, vel km/s helio."""
    x, y, z = pos[:, 0], pos[:, 1], pos[:, 2]
    d = np.column_stack([x - R0*1000, y])            # GC->star, pc (planar)
    R = np.hypot(d[:, 0], d[:, 1])/1000.0            # kpc
    eR = np.column_stack([d[:, 0], d[:, 1]])/(R[:, None]*1000)
    ephi = np.column_stack([eR[:, 1], -eR[:, 0]])    # eR x zhat
    vtot = vel + np.array([USUN, VSUN + VC, WSUN])
    vR = vtot[:, 0]*eR[:, 0] + vtot[:, 1]*eR[:, 1]
    vphi = vtot[:, 0]*ephi[:, 0] + vtot[:, 1]*ephi[:, 1]
    Lz = R*vphi
    Rg = Lz/VC
    Jr = 0.5*(vR**2 + KAP**2*(Rg - R)**2)/KAP
    Jz = 0.5*(vtot[:, 2]**2 + NU**2*(z/1000.0)**2)/NU
    return R, Lz, Jr, Jz

def pick(cols, *cands):
    for c in cands:
        if c in cols: return c
    return None

def run_galah(path):
    df = pd.read_csv(path, dtype={'gaiadr3_source_id': str, 'sobject_id': str,
                                  'gaia_dr2_source_id': str})
    df['gaiadr3_source_id'] = df['gaiadr3_source_id'].fillna('')
    cols = df.columns
    rvc = pick(cols, 'rv_galah', 'rv', 'rv_obst', 'dr3_rv')
    snrc = pick(cols, 'snr_c3_iraf', 'snr', 'snr_c2_iraf')
    n0 = len(df)
    t1 = (df['flag_sp'].fillna(1) == 0) & (df['flag_fe_h'].fillna(1) == 0)
    t1 &= df[snrc] >= 30
    t1 &= df['teff'].between(5200, 6300) & (df['logg'] >= 3.5)
    t1 &= (df['fe_h'].abs() <= 0.05) & (df['e_fe_h'] <= 0.06)
    t1 &= (df['flag_mg_fe'].fillna(1) == 0) & (df['flag_y_fe'].fillna(1) == 0)
    ymg = df['y_fe'] - df['mg_fe']
    t1 &= ymg.abs() <= YMG_TOL
    cand = df[t1.fillna(False)].copy()
    cand['ymg'] = ymg[t1.fillna(False)]
    cand['age_gyr'] = (CLOCK_A - cand['ymg'])/CLOCK_B
    # tier 2
    ok6 = cand[[rvc, 'parallax', 'pmra', 'pmdec', 'ra', 'dec']].notna().all(axis=1) & (cand['parallax'] > 0)
    cand = cand[ok6]
    pos, vel = phase_space(cand['ra'].values, cand['dec'].values, cand['parallax'].values,
                           cand['pmra'].values, cand['pmdec'].values, cand[rvc].values)
    R, Lz, Jr, Jz = actions(pos, vel)
    cand['R_kpc'], cand['Lz'], cand['Jr'], cand['Jz'] = R, Lz, Jr, Jz
    cand['tier2'] = (np.abs(Lz - LZ_SUN) <= LZ_WIN) & (Jz <= JZ_MAX) & (Jr <= JR_MAX)
    # tier 3
    wmads, nvals = [], []
    for _, r in cand.iterrows():
        num = den = 0.0; nv = 0
        for E in ELEMS:
            xc, ec, fc = f'{E.lower()}_fe', f'e_{E.lower()}_fe', f'flag_{E.lower()}_fe'
            if xc in cols and fc in cols and pd.notna(r[xc]) and r[fc] == 0:
                e = r[ec] if (ec in cols and pd.notna(r[ec])) else EFLOOR
                w = 1.0/max(float(e), EFLOOR)**2
                num += w*abs(float(r[xc])); den += w; nv += 1
        wmads.append(num/den if den > 0 else np.nan); nvals.append(nv)
    cand['wmad'] = wmads; cand['n_elem'] = nvals
    cand['tier3'] = cand['tier2'] & (cand['n_elem'] >= NVALID_MIN) & (cand['wmad'] <= WMAD_MAX)
    # completeness injection (conditional on clean Teff/logg box)
    box = df[(df['teff'].between(5200, 6300)) & (df['logg'] >= 3.5) &
             (df['flag_sp'].fillna(1) == 0) & (df['flag_fe_h'].fillna(1) == 0) &
             (df['flag_mg_fe'].fillna(1) == 0) & (df['flag_y_fe'].fillna(1) == 0) &
             (df[snrc] >= 30)]
    rng = np.random.default_rng(4568)
    if len(box) >= 100:
        idx = rng.integers(0, len(box), 10000)
        efe = box['e_fe_h'].values[idx]
        ey = box['e_y_fe'].values[idx] if 'e_y_fe' in cols else np.full(10000, 0.06)
        emg = box['e_mg_fe'].values[idx] if 'e_mg_fe' in cols else np.full(10000, 0.04)
        ey = np.nan_to_num(ey, nan=0.06); emg = np.nan_to_num(emg, nan=0.04)
        ymg_true = CLOCK_A - CLOCK_B*T_SUN
        feh_obs = rng.normal(0, np.maximum(efe, 1e-3))
        ymg_obs = (ymg_true + rng.normal(0, CLOCK_B*0.8, 10000)
                   + rng.normal(0, np.sqrt(ey**2 + emg**2)))
        passed = (np.abs(feh_obs) <= 0.05) & (efe <= 0.06) & (np.abs(ymg_obs) <= YMG_TOL)
        completeness = float(passed.mean())
    else:
        completeness = float('nan')
    stats = dict(rows=n0, tier1=int(len(cand)), tier2=int(cand['tier2'].sum()),
                 gold=int(cand['tier3'].sum()), completeness_tier1_conditional=round(completeness, 3))
    return cand, stats, rvc

def run_apogee(path):
    df = pd.read_csv(path, dtype={'GAIAEDR3_SOURCE_ID': str, 'APOGEE_ID': str})
    n0 = len(df)
    t1 = (df['ASPCAP_STAR_BAD'] == 0) & (df['SNR'] >= 80)
    t1 &= df['TEFF'].between(4200, 5200) & df['LOGG'].between(1.5, 3.5)
    t1 &= (df['FE_H'].abs() <= 0.05) & (df['ALPHA_M'] <= 0.05)
    cn = df['C_FE'] - df['N_FE']
    t1 &= (cn >= -0.15) & (cn <= 0.05)
    cand = df[t1.fillna(False)].copy()
    cand['c_n'] = cn[t1.fillna(False)]
    ok6 = cand[['VHELIO_AVG', 'GAIAEDR3_PARALLAX', 'GAIAEDR3_PMRA',
                'GAIAEDR3_PMDEC']].notna().all(axis=1) & (cand['GAIAEDR3_PARALLAX'] > 0)
    cand = cand[ok6]
    pos, vel = phase_space(cand['GAIAEDR3_RA'].values, cand['GAIAEDR3_DEC'].values,
                           cand['GAIAEDR3_PARALLAX'].values, cand['GAIAEDR3_PMRA'].values,
                           cand['GAIAEDR3_PMDEC'].values, cand['VHELIO_AVG'].values)
    R, Lz, Jr, Jz = actions(pos, vel)
    cand['R_kpc'], cand['Lz'], cand['Jr'], cand['Jz'] = R, Lz, Jr, Jz
    cand['tier2'] = (np.abs(Lz - LZ_SUN) <= LZ_WIN) & (Jz <= JZ_MAX) & (Jr <= JR_MAX)
    stats = dict(rows=n0, tier1=int(len(cand)), tier2=int(cand['tier2'].sum()),
                 note='exploratory lane; no GOLD from survey data (spec)')
    return cand, stats

def linked_flags(ids):
    """LINKED if id in M3 candidate table (best-effort; absent file -> none)."""
    linked = set()
    try:
        ct = pd.read_csv('/mnt/user-data/uploads/projects/causal-archipelago/'
                         'm3-pathfinder/candidate-table.csv', dtype=str)
        idcol = pick(ct.columns, 'source_id', 'gaia_dr3', 'GaiaDR3', 'sid')
        if idcol:
            m3 = set(ct[idcol].str.strip())
            linked = set(i for i in ids if i in m3)
    except Exception as e:
        print(f'LINKED check skipped: {e}')
    return linked

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--galah', default='/root/ca/e8/e8_galah_abund.csv')
    ap.add_argument('--apogee', default='/root/ca/e8/e8_apogee_abund.csv')
    ap.add_argument('--smoke', action='store_true')
    a = ap.parse_args()
    out = dict(spec='E8-SPEC.md@28d308e')
    g, gs, rvc = run_galah(a.galah)
    out['GALAH'] = gs
    ap_c, aps = run_apogee(a.apogee)
    out['APOGEE'] = aps
    lk = linked_flags(list(g['gaiadr3_source_id']) + list(ap_c['GAIAEDR3_SOURCE_ID']))
    g['linked'] = g['gaiadr3_source_id'].isin(lk)
    ap_c['linked'] = ap_c['GAIAEDR3_SOURCE_ID'].isin(lk)
    out['kill_condition_triggered'] = bool(gs['tier1'] == 0)
    # candidate table
    rows = []
    for _, r in g.iterrows():
        rows.append(dict(lane='GALAH', source_id=r['gaiadr3_source_id'],
                         survey_id=r['sobject_id'], teff=r['teff'], logg=r['logg'],
                         fe_h=r['fe_h'], ymg=round(r['ymg'], 4), age_gyr=round(r['age_gyr'], 2),
                         Lz=round(r['Lz'], 1), Jr=round(r['Jr'], 2), Jz=round(r['Jz'], 2),
                         wmad=(round(r['wmad'], 4) if pd.notna(r['wmad']) else ''),
                         n_elem=r['n_elem'],
                         tier=('GOLD' if r['tier3'] else
                               'KINEMATIC-CONSISTENT' if r['tier2'] else 'CANDIDATE'),
                         linked=bool(r['linked'])))
    for _, r in ap_c.iterrows():
        rows.append(dict(lane='APOGEE-exploratory', source_id=r['GAIAEDR3_SOURCE_ID'],
                         survey_id=r['APOGEE_ID'], teff=r['TEFF'], logg=r['LOGG'],
                         fe_h=r['FE_H'], ymg='', age_gyr='', Lz=round(r['Lz'], 1),
                         Jr=round(r['Jr'], 2), Jz=round(r['Jz'], 2), wmad='', n_elem='',
                         tier=('KINEMATIC-CONSISTENT' if r['tier2'] else 'CANDIDATE'),
                         linked=bool(r['linked'])))
    pd.DataFrame(rows).to_csv('/root/ca/e8/e8_candidates.csv', index=False)
    json.dump(out, open('/root/ca/e8/e8_sieve_stats.json', 'w'), indent=1)
    print(json.dumps(out, indent=1))
    print(f'candidates written: {len(rows)} (GALAH rv col: {rvc})')

if __name__ == '__main__':
    main()
