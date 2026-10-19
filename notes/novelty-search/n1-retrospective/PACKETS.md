# N1 retrospective arm — sanitized claim packets (frozen before any judge runs)

Date: 2026-08-31. Written from generation-time records; prior-art
names and deflation context scrubbed. Packet authorship bias recorded
in MANIFEST. These exact texts are what every judge cell receives.

---

## CLM-1

BACKGROUND: Gaia astrometry identifies wide comoving stellar pairs —
separations of roughly 0.01 to 1 parsec, velocity differences under a
few km/s — many of which are believed to be remnants of dissolved
birth clusters rather than chance alignments or bound binaries.

IDEA: If comoving pairs are truly birth siblings, they condensed from
the same chemically near-homogeneous cloud, so their photospheric
abundances should be measurably more similar than those of matched
random field pairs. Cross-matching comoving-pair catalogs against
large spectroscopic survey abundances yields a scalable test: compare
the |Δ[Fe/H]| distribution of comoving pairs against carefully matched
control pairs. Chemistry then serves as an independent certification
channel for kinematically selected sibling candidates at survey scale.

FACETS — purpose: certify dissolved-cluster sibling pairs; mechanism:
birth-cloud chemical homogeneity implies excess abundance similarity
in comoving pairs relative to matched controls; domain: Galactic
archaeology; method: pair selection, control matching, paired
abundance-difference statistics; data: Gaia astrometry crossed with
stellar spectroscopic survey abundances.

---

## CLM-2

BACKGROUND: In a standard expanding ΛCDM universe there is an event
horizon: a maximum comoving distance χ_event from which a light signal
emitted now can ever reach us. A civilization launches probes at
constant peculiar speed v (in units of c) to explore its surroundings.

IDEA: Distinguish touching from knowing. A probe launched at speed v
can eventually reach comoving distance χ_touch = v·χ_event. But for
the home civilization to LEARN anything, the probe's findings must
travel back as a light signal that arrives before expansion forbids
it. The two-way constraint gives a clean closed-form law: the
reporting horizon is χ_know = [v/(1+v)]·χ_event. At the light-speed
limit this saturates at exactly half the event horizon — one eighth of
the reachable volume. Higher probe speed increases absolute reach
while the reporting fraction of reachable volume falls.

FACETS — purpose: quantify what a stay-at-home civilization can ever
come to know in an expanding universe; mechanism: composing the
outbound probe worldline with the return light signal in comoving
coordinates yields the v/(1+v) reporting horizon; domain: cosmology of
horizons; method: conformal-time light-cone algebra, closed form;
data: standard ΛCDM background.

---

## CLM-3

BACKGROUND: Model conscious or communicating loci as nodes embedded in
spacetime (or points with regions of causal access). Integration of
knowledge requires records from multiple loci reaching a shared event.

IDEA: Pairwise mutual reachability, even for ALL pairs, does not imply
the existence of any common receiver event that can collect every
record. The obstruction is geometric: regions can intersect pairwise
without sharing a single common point, so a network in which every
pair can exchange records may still admit no event at which all
records coexist. Collective integration therefore requires a
strictly stronger higher-order condition (a common witness for the
whole set), and any model that infers collective access from pairwise
compatibility systematically overstates what the network can
integrate.

FACETS — purpose: correct the inference from pairwise connectivity to
collective integration; mechanism: pairwise-intersecting causal
regions need not have a common intersection — the higher-order
condition is strictly stronger than the pairwise one; domain: causal
structure of communication networks in spacetime; method: geometric
counterexample plus a formal condition separating pairwise from
common-witness access; data: none (mathematical).

---

## CLM-4

BACKGROUND: Take as given (within the project) a fixed-home reporting
bound in an expanding universe: a stationary archive at the origin,
probes at speed β, a common deadline, and a processing delay define
the comoving region from which reports can arrive in time.

IDEA: Does a MOVING final archive, or splitting into several
archives, beat staying home? Bounded result: the feasible reporting
region for a final archive at z is a compact convex set D(z) with
D(−z) = −D(z); a symmetrization argument (the difference body is
contained in the stationary ball, then a volume inequality) proves
that for uniform comoving target density no choice of final archive
location — and no subluminal collector trajectory — yields more
reporting volume than the stationary origin, at any probe speed. For
two collectors moving oppositely at speed u, counting sites received
by at least one gives a closed-form union fraction F(u), quantifying
what splitting the archive buys when records need not be reunited.

FACETS — purpose: optimal placement and motion of report-collecting
archives under a deadline; mechanism: convexity and central symmetry
of the feasible region plus a symmetrization volume inequality force
the stationary optimum; domain: relativistic information logistics in
an expanding universe; method: convex geometry, closed-form
integration; data: none (mathematical).

---

## CLM-5

BACKGROUND: Extend the collector setting: multiple targets carrying
different weights (values), multiple collectors, and the requirement
that content be brought together — the full weighted record must reach
a COMMON receipt event by the deadline, not merely reach some
collector somewhere.

IDEA: A framework computing earliest common-receipt times for weighted
target subsets across collector strategies. Feasibility of a common
receipt event is a causal-cone intersection problem; earliest common
receipt is found by convex programs over candidate witness events;
higher-order cases (triples, tetrahedra of targets) have analytic
receipt times with a tightness structure in which the pairwise
conditions do not suffice and the full-set condition binds. Output:
integration-frontier curves — achievable weighted content as a
function of deadline — across archive-count strategies.

FACETS — purpose: when can distributed weighted records be unified at
one event by a deadline; mechanism: common-witness feasibility as
intersection of causal cones, solved by convex programming, with
higher-order intersection conditions strictly beyond pairwise; domain:
relativistic information logistics; method: convex feasibility
programs, analytic small-case solutions, frontier curves; data: none
(mathematical).

---

## CLM-6

BACKGROUND: Whether very wide binaries (separations of thousands of
AU, internal accelerations near 10⁻¹⁰ m/s²) show a gravity boost above
the Newtonian prediction is an active, explicitly disputed question in
the literature, with published claims on both sides drawn from Gaia
data.

IDEA: A decision-grade test design with three commitments made BEFORE
any outcome is computed: (1) preregistration of exactly four
statistics on a public wide-binary catalog (≤200 pc), sealed and
timestamped cryptographically before unblinding, analyzed once; (2)
NOISE-CALIBRATED anchors — the key step: a pure-Newtonian mock with
realistic measurement noise inflates the naive velocity-ratio
statistic substantially (≈ +0.10), so the Newtonian and
modified-gravity reference values are recomputed under the noise model
rather than compared to the naive theoretical anchor, which would
otherwise manufacture a spurious boost detection; (3) an explicit
domain of licensed conclusions stated in advance (sampled separation
and acceleration ranges only).

FACETS — purpose: adjudicate a disputed low-acceleration gravity
anomaly; mechanism: recomputing decision anchors under a
noise-injected null model so that measurement noise cannot masquerade
as a modified-gravity signal, combined with cryptographically sealed
preregistration; domain: gravitational dynamics of wide binaries;
method: preregistered sealed analysis of a public catalog with
calibrated anchors; data: public Gaia-derived wide-binary catalog.

---

## CLM-7

BACKGROUND: An analytical framework in the economics-of-strategy
domain makes substantive claims about when AI substitution of human
work succeeds or fails. The framework has an explicit operational
codebook and a versioned corrections discipline, and has been applied
to its own production process.

IDEA: A named structural property — call it reflexive predictability:
a framework exhibits it when the framework's SUBSTANTIVE theory
directly predicts the conditions under which the framework itself can
be recursively applied to test its own operational integrity, with the
recursive application producing dated empirical evidence that feeds
back through versioning. Five jointly necessary conditions: (R1) a
substantive theoretical scope; (R2) an explicit operational
specification; (R3) the theory predicts when procedures of the
framework's own kind are feasible or fail; (R4) the apparatus can be
recursively applied to the framework's own components; (R5) the
recursive evidence is dated, recorded, and integrated back. The claim:
this CONFIGURATION has not been previously identified or named — the
relationship between theory and recursive applicability is derivable,
not accidental, and no published framework combines all five elements.

FACETS — purpose: identify and name a structural property of
analytical frameworks; mechanism: substantive theory entailing the
conditions of its own recursive testability, with evidence fed back
through versioned discipline; domain: methodology and sociology of
scientific frameworks; method: necessary-and-sufficient conditions
plus a worked instance; data: the framework's own dated trial record.
