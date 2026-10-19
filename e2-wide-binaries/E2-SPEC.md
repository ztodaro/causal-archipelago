# E2 spec — ultra-wide binaries and the low-acceleration gravity test (FROZEN)

Date frozen: 2026-08-30. CRITICAL DISCIPLINE: no wide-binary statistic of
any kind has been computed from this project's data as of this freeze. The
low-acceleration bin is SEALED until every selection, screen, and analysis
choice below is locked by this commit.

## Question

Do ultra-wide binaries in the RV-complete 100 pc sample show the ~20%
velocity excess at accelerations below a₀ ≈ 1.2×10⁻¹⁰ m/s² predicted by
MOND-type gravity (Chae-style claim), or Newtonian behavior (Banik-style
claim)? Contribution: an independent, preregistered, contamination-
audited sample with full 3D velocities (most prior work is proper-motion
only; our RV completeness adds the third component and its binarity
screens).

## Pair selection (frozen)

From the frozen 133,468-star sample: pairs with
- projected separation s ∈ [500, 30,000] AU;
- parallaxes consistent within 3σ and |Δd| < 0.5 pc;
- |Δv_3D| < 2 × v_circ(s, M_tot) with v_circ = sqrt(G·M_tot/s) and
  photometric masses from M_G via a public main-sequence mass-luminosity
  relation (relation choice documented at retrieval time, before any
  velocity statistic is computed);
- both stars: RUWE < 1.4 (already sample-wide), ipd_frac_multi_peak ≤ 2,
  astrometric_excess_noise_sig < 2, rv_amplitude_robust < 5 km/s,
  radial_velocity_error < 1.5 km/s, not duplicated_source;
- no third sample star within 10,000 AU of either component (resolved
  triple screen).

## Blinding protocol (frozen)

1. Calibration region OPEN: pairs with internal Newtonian acceleration
   g_N = G·M_tot/s² > 10 a₀. All pipeline development, error modeling,
   and sanity checks happen here only.
2. SEALED region: g_N < 10 a₀ (this includes the entire test regime).
   Computed once, after the calibration analysis is committed.
3. Cross-check: selection compared against the public El-Badry et al.
   wide-binary catalog (overlap fraction reported; disagreements sampled
   and inspected BEFORE unsealing).

## Analysis (frozen)

- Observable: ṽ = |Δv_perp| / v_circ(s) (and a 3D variant using full Δv),
  binned in log g_N.
- Newtonian expectation for bound orbits: ṽ distribution with known
  support (⟨ṽ⟩ ≈ 0.9, hard cap √2 for bound pairs); MOND-type expectation:
  distribution shifted up ~20% below a₀.
- Contamination model: synthetic hierarchical triples injected at rates
  spanning published estimates; the unresolved-companion velocity
  inflation measured in the calibration region and propagated.
- Noise: RV and PM errors Monte-Carlo'd (12 realizations, house method).
- Decision statistic: ratio of median ṽ in [0.1 a₀, a₀] to median ṽ in
  [10 a₀, 100 a₀], with bootstrap CI clustered by pair. Symmetric
  reporting commitment: the ratio is published with its CI whether it
  lands at 1.0, 1.2, or anywhere else. No result is filed in a drawer.

## Honest scope

At ~100 pc with these quality cuts the pair count may be small (hundreds
at best); if the sealed-region pair count is under 50, the deliverable
contracts to "method + contamination audit + forecast," stated up front —
that outcome is publishable methods work, not failure. Extending beyond
100 pc (dropping RV completeness, PM-only like prior work) is a SEPARATE
future spec, not a silent widening of this one.
