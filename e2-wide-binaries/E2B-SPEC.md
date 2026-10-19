# E2b spec — the powered wide-binary gravity test (FROZEN)

Date frozen: 2026-08-30, before any E2b data retrieval. E2 stands as run
(ratio 1.070 [0.849, 1.252], symmetric verdict, publicly anchored). E2b is
its statistically powered successor. Everything not amended below carries
over from E2-SPEC.md + the pre-unseal amendments verbatim, including the
sealed-bin ritual, symmetric reporting, and the drawer-opens-once rule.

## Motivation sentence (the flicker's one honest appearance)

E2's deepest bin (0.1–0.3 a₀, 18 pairs) sat at median ṽ ≈ 0.73 against a
Newtonian baseline of 0.58 — statistically empty, hypothesis-generating
only. E2b preregisters that bin as a SECONDARY statistic so the anecdote
becomes a test.

## Sample (amended)

- Source: El-Badry, Rix & Heintz 2021 catalog, both components parallax
  ≥ 5 mas (d ≤ 200 pc). PM-only: NO radial-velocity requirement.
- Purity: R_chance_align < 0.01 (primary); < 0.1 retained as labeled
  variant. Neither component may appear in any other catalog pair
  (resolved-multiple screen).
- Per-component quality (from catalog columns or a Gaia DR3 ID-join in
  the intake): ruwe < 1.4, ipd_frac_multi_peak ≤ 2,
  astrometric_excess_noise_sig < 2, parallax_over_error ≥ 20, parallaxes
  consistent within 3σ.
- Projected separation 500–50,000 AU. Masses: Mamajek v2022.04.16
  M_G→mass (held), unchanged.

## Screens re-derived for PM-only data (replaces the RV screens)

Unresolved companions now enter through astrometric wobble and photocenter
motion rather than RV variability. The calibration phase must inject
PM-reflex triples (companion-induced photocenter proper-motion offsets,
period-averaged for periods ≪ and ≫ the Gaia baseline) and measure
survival through the ruwe/ipd/aen screens, exactly as E2 did for RV
triples. Real per-star PM errors (now in the intake) replace the
magnitude-based approximation in the noise MC.

## Observable and statistics (unchanged + one addition)

- Observable: ṽ_perp = Δv_perp / v_circ(s_proj), PM-based.
- PRIMARY decision statistic: median ṽ ratio, [0.1–1] a₀ over
  [10–100] a₀, pair bootstrap CI (10,000). Newtonian ≈ 1.0; MOND ≈ 1.2.
- SECONDARY (new, preregistered): median ṽ in [0.1–0.3] a₀ with CI,
  compared against the high-acceleration baseline — the flicker bin,
  tested properly this time.
- Power expectation: thousands of decision-bin pairs; CI half-width
  ~±0.03–0.05, separating the hypotheses. Small-N clause: n_low < 500
  → reduced-power flag (not expected).

## Ritual (unchanged, restated because it is the point)

1. Calibration region (g_N > 10 a₀) open for all development.
2. Injection + noise MC + El-Badry-internal consistency checks committed.
3. Public anchoring: tag pre-unseal-e2b, GitHub push, OpenTimestamps —
   BEFORE any sealed computation.
4. Optional adversarial window (owner's call, formally left open here).
5. Unseal once, on owner instruction. Symmetric reporting wherever it
   lands.

## Intake required (agent; provenance per file; IDs as integer strings)

1. El-Badry 2021 catalog rows with parallax1 ≥ 5 OR parallax2 ≥ 5 and
   R_chance_align < 0.1 — ALL published columns (component astrometry,
   PM errors, magnitudes included). Expect order 10⁴–10⁵ rows.
2. If ruwe / ipd_frac_multi_peak / astrometric_excess_noise(_sig) or PM
   errors are absent from the catalog columns: exact source-ID join to
   Gaia DR3 for both components to fetch them (no sky matching).
