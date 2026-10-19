"""B4 perspective correction, version 2. Dated amendment of 2026-10-19 (DR4-FREEZE-SPEC.md, Amendment 4).

The stamped e2b_perspective.py stays as it was. Its correct_perspective() subtracts the first-order term where it
should add it, and its self-test passed because it injected the same assumed sign. This file gives:

  correct_perspective()   the first-order correction with the sign fixed; both velocities must be in one basis
  relative_tangential()   the exact method: star 1's space velocity is projected at star 2's position, with each star
                          in its own east/north basis, so the perspective term and the basis turn are removed together

and checks them against the geometry itself: one space velocity, projected at two sky positions anywhere on the sky,
must leave no relative velocity.

Run from the repository root:  python notes/dr4-freeze/e2b_perspective_v2.py
It writes notes/dr4-freeze/e2b_perspective_v2_check.json. Needs numpy.
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def unit_vectors(ra, dec):
    """Line of sight, east and north unit vectors at (ra, dec), in radians."""
    n = np.array([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)])
    east = np.array([-np.sin(ra), np.cos(ra), 0.0])
    north = np.array([-np.sin(dec) * np.cos(ra), -np.sin(dec) * np.sin(ra), np.cos(dec)])
    return n, east, north


def tangential(ra, dec, v3d):
    """The (east, north) tangential velocity that a space velocity shows at (ra, dec)."""
    _, east, north = unit_vectors(ra, dec)
    return np.array([v3d @ east, v3d @ north])


def stamped_correct_perspective(dv_ra, dv_dec, v_r, theta_rad, e_hat):
    """The stamped function's arithmetic, repeated here for comparison. It subtracts the term."""
    p = v_r * theta_rad
    return dv_ra - p * e_hat[0], dv_dec - p * e_hat[1]


def correct_perspective(dv_ra, dv_dec, v_r, theta_rad, e_hat):
    """First-order removal of the perspective term (El-Badry 2019), sign fixed.

    dv_ra, dv_dec: tangential-velocity difference, star 2 minus star 1, km/s, both in star 1's east/north basis.
    v_r: systemic radial velocity, km/s. theta_rad: angular separation. e_hat: unit sky vector from star 1 toward
    star 2, in star 1's east/north basis. One shared space velocity shows a difference of -v_r*theta along e_hat,
    so the correction adds v_r*theta along e_hat.
    """
    p = v_r * theta_rad
    return dv_ra + p * e_hat[0], dv_dec + p * e_hat[1]


def relative_tangential(ra1, dec1, ra2, dec2, vt1, vt2, v_r):
    """Star 2's tangential velocity minus the one star 1's space velocity would show at star 2's position.

    vt1, vt2: each star's observed (east, north) tangential velocity in its own basis, km/s. v_r: systemic radial
    velocity, km/s. The result is in star 2's east/north basis. A pair that shares one space velocity returns zero
    to second order in the separation. Use this on raw Gaia proper motions, whose components sit in each star's own
    basis.
    """
    n1, east1, north1 = unit_vectors(ra1, dec1)
    v1 = v_r * n1 + vt1[0] * east1 + vt1[1] * north1
    return np.asarray(vt2, dtype=float) - tangential(ra2, dec2, v1)


def _offset(ra, dec, theta, pa):
    """The sky position theta radians from (ra, dec) at position angle pa (from north through east)."""
    n, east, north = unit_vectors(ra, dec)
    d = np.cos(pa) * north + np.sin(pa) * east
    n2 = np.cos(theta) * n + np.sin(theta) * d
    return np.arctan2(n2[1], n2[0]), np.arcsin(np.clip(n2[2], -1.0, 1.0))


def _direction_from_1_to_2(ra1, dec1, ra2, dec2):
    """Unit sky vector from star 1 toward star 2, as (east, north) components in star 1's basis."""
    n1, east1, north1 = unit_vectors(ra1, dec1)
    n2, _, _ = unit_vectors(ra2, dec2)
    t = n2 - (n2 @ n1) * n1
    t /= np.linalg.norm(t)
    return np.array([t @ east1, t @ north1])


def check():
    out = {}

    # 1. The case in the 4 September review: stars at (0, 0) and (theta, 0) share the space velocity (v_r, 0, 0).
    theta, v_r = 1e-3, 30.0
    v = np.array([v_r, 0.0, 0.0])
    vt1, vt2 = tangential(0.0, 0.0, v), tangential(theta, 0.0, v)
    dv = vt2 - vt1
    e_hat = _direction_from_1_to_2(0.0, 0.0, theta, 0.0)
    out["review_case"] = {
        "theta_rad": theta, "systemic_rv_kms": v_r, "true_relative_velocity_kms": 0.0,
        "observed_ra_difference_kms": float(dv[0]),
        "stamped_function_kms": float(stamped_correct_perspective(dv[0], dv[1], v_r, theta, e_hat)[0]),
        "fixed_first_order_kms": float(correct_perspective(dv[0], dv[1], v_r, theta, e_hat)[0]),
        "exact_method_kms": float(relative_tangential(0.0, 0.0, theta, 0.0, vt1, vt2, v_r)[0]),
    }

    # 2. Pairs anywhere on the sky, each sharing one random space velocity.
    rng = np.random.default_rng(20261019)
    rows = []
    for _ in range(20000):
        ra1 = rng.uniform(0, 2 * np.pi)
        dec1 = np.arcsin(rng.uniform(-0.999, 0.999))
        theta = 10 ** rng.uniform(-5, np.log10(5e-3))
        ra2, dec2 = _offset(ra1, dec1, theta, rng.uniform(0, 2 * np.pi))
        v = rng.normal(0, 40, 3)
        n1, east1, north1 = unit_vectors(ra1, dec1)
        n2, _, _ = unit_vectors(ra2, dec2)
        v_r = v @ ((n1 + n2) / np.linalg.norm(n1 + n2))   # the pair's systemic radial velocity
        vt1, vt2 = tangential(ra1, dec1, v), tangential(ra2, dec2, v)
        t2_in_1 = np.array([v @ east1, v @ north1]) - (v @ n2) * np.array([n2 @ east1, n2 @ north1])
        dv_one_basis = t2_in_1 - vt1                       # star 2's tangential velocity carried into star 1's basis
        dv_raw = vt2 - vt1                                 # raw component difference, each star in its own basis
        e_hat = _direction_from_1_to_2(ra1, dec1, ra2, dec2)
        scale = theta**2 * np.linalg.norm(v)               # the size of a second-order term
        rows.append((theta, np.linalg.norm(v), v_r,
                     np.linalg.norm(relative_tangential(ra1, dec1, ra2, dec2, vt1, vt2, v_r)) / scale,
                     np.linalg.norm(correct_perspective(*dv_one_basis, v_r, theta, e_hat)) / scale,
                     np.linalg.norm(stamped_correct_perspective(*dv_one_basis, v_r, theta, e_hat)) / (2 * abs(v_r) * theta),
                     np.linalg.norm(dv_raw - dv_one_basis) / (theta * np.linalg.norm(v))))
    r = np.array(rows)
    small = r[:, 0] <= 1e-3
    out["all_sky"] = {
        "pairs": len(r), "theta_rad_range": [float(r[:, 0].min()), float(r[:, 0].max())],
        "exact_method_max_residual_over_theta2_v": float(r[:, 3].max()),
        "fixed_first_order_max_residual_over_theta2_v": float(r[:, 4].max()),
        "stamped_function_median_error_over_2_vr_theta": float(np.median(r[:, 5])),
        "basis_turn_median_over_theta_v": float(np.median(r[:, 6])),
        "exact_method_max_residual_kms_theta_le_1e-3": float((r[small, 3] * r[small, 0] ** 2 * r[small, 1]).max()),
    }
    out["passes"] = bool(
        abs(out["review_case"]["stamped_function_kms"] + 0.06) < 1e-6
        and abs(out["review_case"]["fixed_first_order_kms"]) < 1e-7
        and abs(out["review_case"]["exact_method_kms"]) < 1e-9
        and out["all_sky"]["exact_method_max_residual_over_theta2_v"] <= 1.0
        and out["all_sky"]["fixed_first_order_max_residual_over_theta2_v"] <= 1.0
        and abs(out["all_sky"]["stamped_function_median_error_over_2_vr_theta"] - 1.0) < 0.05
    )
    return out


if __name__ == "__main__":
    result = check()
    (HERE / "e2b_perspective_v2_check.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=1))
