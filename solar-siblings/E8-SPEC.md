# E8 Spec — the solar-sibling expedition (FROZEN)

Date frozen: 2026-08-30, before any E8 data retrieval or sieve
computation. Engine A inverted: at the Sun's age (4.568 Gyr) radial
migration has eroded kinematic memory below the <1 Gyr regime where the
M3 selector was validated, so chemistry leads, kinematics ranks, and the
T-statistic is a tiebreaker only. Inherited rules: preregistration,
stability-is-not-correctness, exact integer-string IDs, symmetric
reporting, deviations documented never silently fixed.

## Claim caps (M0 discipline)

Solar-sibling searching is not new (Ramírez et al. 2014 / HD 162826;
Adibekyan et al. 2018 / HD 186302; Webb et al. 2020 orbital integration;
Martínez-Barbosa et al. 2016 dispersal modeling). What is offered here:
a PREREGISTERED, survey-scale sieve with frozen tiers, frozen windows,
an injection-based completeness statement, and a kill condition. Any
GOLD star is a **candidate** until confirmed by independent high-resolution
differential abundance analysis; no "sibling found" claim from survey
pipelines alone.

## Reference values (frozen)

Solar age t☉ = 4.568 Gyr. All survey abundances are differential to the
Sun by construction ([X/H]☉ ≡ 0). Kinematic frame: R₀ = 8.2 kpc,
v_c = 233.1 km/s, solar peculiar motion (U,V,W)☉ = (11.1, 12.24, 7.25)
km/s (Schönrich et al. 2010). Derived: Lz☉ = R₀(v_c + V☉) = 2011.8
kpc·km/s; Jz☉ ≈ 0.35 kpc·km/s. Vertical frequency ν = √(4πGρ₀) with
ρ₀ = 0.10 M☉/pc³ → ν = 73.5 km/s/kpc; epicyclic κ = √2·v_c/R₀ = 40.2
km/s/kpc (flat rotation curve). Age clock (GALAH lane): [Y/Mg] − age
relation of Nissen (2016), t = (0.170 − [Y/Mg])/0.0371 Gyr, validity:
solar-metallicity dwarfs/turnoff.

## Lanes

- **GALAH lane (decision lane):** DR3 main_allstar, ≤ 1 kpc. Carries the
  [Y/Mg] clock and the 13-element GOLD vector.
- **APOGEE lane (exploratory, labeled):** DR17 allStar, ≤ 1 kpc. Near-IR
  has no usable Y lines; its [C/N] giant clock is coarse (σ ≳ 2 Gyr).
  APOGEE survivors are labeled CANDIDATE-APOGEE and cannot reach GOLD
  from survey data alone. No decision weight.

## Tier definitions (frozen thresholds)

**TIER 1 — CANDIDATE (chemistry + age).** GALAH: flag_sp = 0,
flag_fe_h = 0, snr ≥ 30, Teff ∈ [5200, 6300] K, log g ≥ 3.5 (clock
validity domain); |[Fe/H]| ≤ 0.05 with e_fe_h ≤ 0.06; flag_mg_fe = 0 and
flag_y_fe = 0; |[Y/Mg]| ≤ 0.056 (= |t − 4.568| ≤ 1.5 Gyr under the
frozen clock).
APOGEE (exploratory): ASPCAP_STAR_BAD = 0, SNR ≥ 80, Teff ∈ [4200, 5200],
log g ∈ [1.5, 3.5]; |FE_H| ≤ 0.05; ALPHA_M ≤ 0.05 (thin-disk screen);
[C/N] = C_FE − N_FE ∈ [−0.15, +0.05] (broad solar-age band, documented
as coarse).

**TIER 2 — KINEMATIC-CONSISTENT.** Full 6D from survey RV + Gaia
astrometry in the intake. Axisymmetric actions via the frozen constants
above (Lz exact; Jz = Ez/ν with Ez = ½(W² + ν²z²); Jr = E_R/κ with
E_R = ½(v_R² + κ²ΔR_g²), ΔR_g = R_g − R). Windows, deliberately loose
because heating is stochastic: |Lz − Lz☉| ≤ 500 kpc·km/s (≈ ±2.1 kpc in
guiding radius — the migration budget for 4.6 Gyr), Jz ≤ 25 kpc·km/s,
Jr ≤ 20 kpc·km/s. Tier 2 is consistency, not proof; it ranks, it does
not confirm.

**TIER 3 — GOLD (abundance vector).** GALAH only. Element list, frozen:
L = {Na, Mg, Al, Si, Ca, Ti, Cr, Mn, Ni, Cu, Zn, Y, Ba}. Use elements
with flag_X_fe = 0; require n_valid ≥ 8. Statistic: WMAD =
Σ wᵢ|[Xᵢ/Fe]| / Σ wᵢ with wᵢ = 1/max(e_Xᵢ, 0.03)². GOLD requires
Tier 1 ∧ Tier 2 ∧ WMAD ≤ 0.040 dex.

**LINKED flag (bonus, no tier change):** survivor's source_id appears in
the M3 candidate-table structures or the E1b treatment-pair graph.

## Completeness (preregistered, required for any null)

Inject 10,000 synthetic solar clones: abundances = 0 + per-star reported
errors (resampled from the survey's error distribution in the Tier-1
Teff/logg box), [Y/Mg] age scatter σ = 0.8 Gyr. Completeness C = pass
fraction through Tier 1. The null statement reports the expected-sibling
bound as N_detectable = N_sib(model) × f_footprint × C, with
N_sib(model) spanning published dispersal predictions (order 1–10 within
1 kpc; possibly 0 — stated as such).

## Kill condition

Zero Tier-1 survivors in the GALAH decision lane → E8 is a published
null with the completeness/volume statement. No threshold loosening, no
second pass. (A later spec, E8b, may widen the volume or use DR4 — new
freeze, new document.)

## Intake required (agent; provenance + SHA-256 per file; IDs as integer strings)

1. `e8_galah_abund.csv` — GALAH DR3 main_allstar, parallax ≥ 1 mas:
   sobject_id, gaiadr3_source_id, ra, dec, parallax, parallax_error,
   pmra, pmdec, rv_galah (or dr3 rv column), e_rv, snr_c3_iraf (or
   equivalent snr), flag_sp, teff, logg, fe_h, e_fe_h, flag_fe_h, and
   for each X in {Na, Mg, Al, Si, Ca, Ti, Cr, Mn, Ni, Cu, Zn, Y, Ba}:
   X_fe, e_X_fe, flag_X_fe.
2. `e8_apogee_abund.csv` — APOGEE DR17 allStar, GAIAEDR3_PARALLAX ≥ 1:
   APOGEE_ID, GAIAEDR3_SOURCE_ID, GAIAEDR3_RA/DEC/PARALLAX/PMRA/PMDEC,
   VHELIO_AVG, VSCATTER, NVISITS, SNR, TEFF, LOGG, FE_H, FE_H_ERR,
   ALPHA_M, ASPCAP_STAR_BAD, C_FE, N_FE, MG_FE and their errors/flags
   as published.

No filtering beyond the parallax floor at intake; the sieve applies the
frozen cuts. Intake-only; no analysis agent-side.

## Outputs

`E8-RESULTS.md` (tier table, completeness, verdict), `e8_candidates.csv`
(every Tier-1 survivor, all tiers/flags, integer-string IDs), sieve code
committed as executed. Symmetric reporting whatever the count.
