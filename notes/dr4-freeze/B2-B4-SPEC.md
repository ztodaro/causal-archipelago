# DR4 bundle items B2 and B4 — pre-tag work, frozen before execution

Dated 2026-09-01. Both computations are deterministic (seeds below).

## B2 — expected DR4 astrometric retention of the GOLD list

Question: of the 221 GOLD stars (solar-siblings/e8_gold_ranked.csv,
frozen), what fraction is expected to remain inside the E8 Tier-2
action window when their actions are recomputed from DR4 astrometry?

Inputs: e8_candidates.csv (tier = GOLD; 221 ids) joined on exact
integer-string gaiadr3_source_id to e8_galah_abund.csv (b3ee7b2) for
ra, dec, parallax, parallax_error, pmra, pmdec, rv_galah, e_rv_galah.
Window and action constants exactly as e8_sieve.py (R0 = 8.2,
VC = 233.1, solar motion 11.1/12.24/7.25, nu = 73.5, kappa = 40.2,
|Lz − 2011.8| ≤ 500, Jz ≤ 25, Jr ≤ 20).

Declared approximations: (i) proper-motion errors are not in the E8
table; sigma_pm (mas/yr) is set equal to parallax_error (mas) for
both components — the DR3 bright-star ratio is close to unity — with
a sensitivity variant at 2× that; (ii) DR4 error scaling from the
66-vs-34-month baseline: parallax × (34/66)^0.5 = 0.718, proper
motion × (34/66)^1.5 = 0.370; (iii) radial velocities are GALAH's and
unchanged by DR4; (iv) flat prior on true astrometry (the DR3
likelihood is taken as the posterior); (v) DR4 systematics ignored.

Method (seed 20261202): for each GOLD star draw 4,000 "truths" from
N(DR3 value, DR3 error) in parallax, pmra, pmdec and rv; add DR4
noise with the scaled errors; recompute actions; retention_i =
fraction of draws inside the window. Report: mean retention (the
prediction), the Poisson-binomial 95% interval on the number of
survivors, the count of stars with retention < 0.5 (the marginal
list), and a control quantity — the same calculation with DR3 noise
in place of DR4 noise (how stable window membership is at present
precision). The 5.9% E8 completeness is chemistry completeness under
survey errors and plays no role here.

Pre-declared prediction form for the bundle: "N_DR4 GOLD stars inside
the Tier-2 window, out of 221, with a 95% interval of [a, b]." No
star becomes a sibling by surviving; E8's claim caps hold.

## B4 — El-Badry perspective term on the E2b sealed bins

The effect: two components of a wide pair are seen along slightly
different lines of sight, so a common space velocity projects to
different tangential velocities. To first order in the angular
separation theta (radians) the apparent tangential velocity
difference along the separation direction is v_r × theta, where v_r
is the pair's systemic radial velocity (El-Badry 2019). In vtilde
units the term is delta = |v_r| theta / v_circ.

Data fact that sets the method: the E2b input (VizieR El-Badry 2021
subset) carries no radial velocities, so a per-pair correction cannot
be applied to the sealed bins today. Two deliverables follow:

1. Implementation, tested: e2b_perspective.py provides
   correct_perspective(dv_ra, dv_dec, v_r, theta, e_hat) that
   subtracts v_r theta along the separation unit vector, and a
   synthetic test that injects a known v_r and recovers the
   uncorrected vector to machine precision. This is the code the DR4
   rerun must call once DR3/DR4 RVs are joined (retrieval request below).
2. Quantification on the sealed bins, statistically: delta_i =
   |v_r| theta_i / v_circ,i with v_r ~ N(0, sigma_vr), sigma_vr =
   25 km/s (declared; the line-of-sight dispersion of a magnitude-
   limited 200 pc disc sample, sensitivity at 20 and 30 km/s), for
   every pair in the primary (bound & R < 0.01) sample. Report P50 and
   P90 of delta per bin — [10–100] a0 (calibration), [0.1–1] a0
   (decision), [0.1–0.3] a0 (flicker) — against Boufourou's
   validation-zone P90 = 0.0016 and deep-bin 0.177. Then re-derive the
   noisy anchors with the perspective term added to the anchor's
   noise model (a signed offset v_r theta / v_circ along a fixed sky
   axis, velocity phase uniform; 400 MC draws as in e2b_inject.py,
   seed 2026 as frozen) for the PRIMARY ratio and the FLICKER median,
   under Newton (boost 1.0) and MOND-scale (1.2). Report the shift of
   each anchor against the frozen values (1.115 [1.070, 1.160];
   1.299 [1.238, 1.356]; flicker 0.682 / 0.788) and state whether the
   unsealed data (1.104 [1.063, 1.164]; flicker 0.699 [0.640, 0.733])
   change their position relative to the perspective-inclusive
   anchors. The frozen E2b verdict is not re-decided here; this is a
   systematics quantification appended alongside it.

Retrieval request (intake only): Gaia DR3
radial_velocity and radial_velocity_error for Source1 and Source2 of
every pair in e2-wide-binaries/data/e2b_elbadry_200pc.csv, joined on
exact integer-string source_id, sentinel-free (no −9999/−10000/
−20000 values), delivered with SHA-256 and row count. With that file
the per-pair correction runs before the tag; without it the
statistical treatment above is what the bundle freezes.

## Execution

Freeze (commit) this spec and both scripts before running; record
script SHA-256s; run each once; append results to
DR4-FREEZE-SPEC.md as Amendment 3 and refresh MANIFEST.sha256.

## Amendment 1 (2026-09-01, before the B2 rerun; B4 unaffected)

The first B2 run (script 64a2bf9b…) joined GOLD rows to the GALAH
table on gaiadr3_source_id. Twenty GOLD rows carry an empty Gaia id
(the robustness note in E8-RESULTS.md records 36,118 such GALAH rows)
and were silently mapped to a single wrong star, which is why the
DR3 point values placed only 201/221 inside a window every GOLD star
passed by construction. The join is changed to the GALAH observation
id (candidates survey_id = table sobject_id), which is unique per
observation and is how E8 itself keyed these rows. The first run's
log is kept (b2_retention_run1_idjoin.log); its numbers are void.
Everything else in B2 is unchanged.
