# E10b, correction (19 October 2026)

`E10B-SPEC.md`, `E10B-AMENDMENT-1.md` and `E10B-RESULTS.md` stay as stamped. An independent review on 4 September 2026 found three problems. A rerun of that review's checks on 19 October reproduced its numbers exactly.

## 1. The age mixture was not marginalized jointly

For each pair, the likelihood averaged the conatal fraction over the pair's age-bin probabilities, averaged the chance density the same way, and then mixed the two averages:

`L_i = fbar_i h_i + (1 − fbar_i) gbar_i`

The stated model puts the mixture inside the average:

`L_i = sum_b M_ib [f_b h_i + (1 − f_b) g_b]`

The two differ by `Cov_M(f_b, g_b)`. They agree only when ages are exact, when the fraction is constant, or when the chance density does not change with age.

Refitting with the joint likelihood gives these point estimates:

| Fit | Young fraction | Old fraction | Intrinsic width |
| --- | --- | --- | --- |
| As stamped | 0.576 | 0.018 | 0 |
| Joint marginalization | 0.570 | 0.031 | 0 |

The direction holds. These are point fits. The stamped intervals and false-positive rate do not carry over, and no new bootstrap has been run.

## 2. The chance template was not matched on age

Controls were pooled by the treatment pair's age. Their own ages were never matched. Of the 3,927 control pairs used for the 473 treatment pairs with valid clocks, 1,846 (47.0%) lack a valid clock for one or both stars. For the 2,081 with two clocks, the median gap between their own clock age and the assigned age is 3.22 Gyr, and 43.7% fall on the other side of 4.5 Gyr. These are noisy point estimates of age. They still show that the pooling did not match ages.

## 3. The lower-bound argument does not protect the age ratio

`E10B-SPEC.md` says that siblings among the controls make each fraction a lower bound and affect the old/young ratio less. That holds only if the contamination is the same at every age. Example: a true fraction of 0.6 at every age, with contamination of 0.05 among young controls and 0.50 among old controls, gives fitted fractions of 0.579 and 0.200. Their ratio is 0.345, although nothing declined.

## What stands

The DECAY DETECTED verdict is suspended. The data support a point estimate: under this model, linked pairs younger than about 4.5 Gyr look more chemically alike than older pairs. A verdict needs four things: a jointly marginalized likelihood, controls matched on age, intervals that carry the template's uncertainty, and a test against simulated pairs whose ages and origins are known.

DR4 item B3 takes its inputs from E10b (constant fraction 0.29, young fraction 0.58), so it inherits these caveats.
