"""Independent analytic check of the B4 perspective fix (notes/dr4-freeze/e2b_perspective_v2.py).

Where the truth comes from: astropy's coordinate and velocity transforms, not the code under test. Two stars
share one 3D space velocity (or differ by a known small velocity). astropy places star 2 relative to star 1
(directional_offset_by), reports each star's pm_ra_cosdec, pm_dec and radial_velocity at its own position and
distance, and gives the separation and position angle. The functions under test must recover the true relative
velocity from those observables.

This file does not call or copy _selftest() from e2b_perspective.py, check() from e2b_perspective_v2.py, or any
of their helpers (unit_vectors, tangential, _offset, _direction_from_1_to_2). The stamped function is pulled out of
the stamped file by its source text, so the comparison uses the frozen bytes rather than a re-typed copy.

Run from the repository root:  python -m pytest tests/test_perspective_sign_analytic.py -v
Needs numpy, astropy, pytest. Override file locations with PERSPECTIVE_V1 / PERSPECTIVE_V2 if needed.
"""
import ast
import importlib.util
import os
from pathlib import Path

import numpy as np
import pytest
import astropy.units as u
from astropy.coordinates import ICRS, CartesianDifferential, SkyCoord, SkyOffsetFrame

ROOT = Path(__file__).resolve().parent.parent
V1 = Path(os.environ.get("PERSPECTIVE_V1", ROOT / "notes/dr4-freeze/e2b_perspective.py"))
V2 = Path(os.environ.get("PERSPECTIVE_V2", ROOT / "notes/dr4-freeze/e2b_perspective_v2.py"))
STAMPED_V1_SHA256 = "cfb446ccc25b6b486bc5666e91cef3a4a5842a57ae48e116c7d01152aad52125"
KMS = u.km / u.s
N_PAIRS = 1500
SEED = 20261124


def _load_v2():
    spec = importlib.util.spec_from_file_location("e2b_perspective_v2", V2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _stamped_correct_perspective():
    """correct_perspective() exactly as stamped. The stamped file runs an analysis at import, so only this
    function's definition is executed."""
    import hashlib
    raw = V1.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == STAMPED_V1_SHA256, "e2b_perspective.py is not the stamped file"
    tree = ast.parse(raw.decode("utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "correct_perspective")
    ns = {"np": np}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(V1), "exec"), ns)
    return ns["correct_perspective"]


v2 = _load_v2()
stamped = _stamped_correct_perspective()


def observe(coord, v_xyz):
    """Give a position a space velocity (ICRS Cartesian, km/s); return (east, north) tangential velocity in km/s
    in the star's own basis, the radial velocity, and the coordinate carrying the velocity."""
    cart = coord.icrs.cartesian.without_differentials().with_differentials(CartesianDifferential(v_xyz * KMS))
    s = SkyCoord(ICRS(cart))
    d = s.distance
    vt = np.stack([(s.pm_ra_cosdec * d).to_value(KMS, u.dimensionless_angles()),
                   (s.pm_dec * d).to_value(KMS, u.dimensionless_angles())])
    return vt, s.radial_velocity.to_value(KMS), s


def offset_frame_tangential(s, origin):
    """Tangential velocity of s in the sky-offset frame centred on origin. Near the origin this basis agrees with
    the origin star's east/north basis to second order in the separation."""
    o = s.transform_to(SkyOffsetFrame(origin=origin))
    d = o.distance
    return np.stack([(o.pm_lon_coslat * d).to_value(KMS, u.dimensionless_angles()),
                     (o.pm_lat * d).to_value(KMS, u.dimensionless_angles())])


def make_pairs(rng, n, theta_max=5e-3, dec_range=(-0.999, 0.999), dv_sigma=0.0):
    ra = rng.uniform(0, 360, n) * u.deg
    dec = np.degrees(np.arcsin(rng.uniform(*dec_range, n))) * u.deg
    d1 = rng.uniform(30, 200, n) * u.pc
    theta = 10 ** rng.uniform(-5, np.log10(theta_max), n) * u.rad
    pa = rng.uniform(0, 360, n) * u.deg
    c1 = SkyCoord(ra=ra, dec=dec, distance=d1, frame="icrs")
    c2_sky = c1.directional_offset_by(pa, theta)
    d2 = d1 * (1 + rng.normal(0, 1e-3, n))
    c2 = SkyCoord(ra=c2_sky.ra, dec=c2_sky.dec, distance=d2, frame="icrs")
    v = rng.normal(0, 40, (3, n))                         # common space velocity, km/s
    dv = rng.normal(0, dv_sigma, (3, n)) if dv_sigma else np.zeros((3, n))
    vt1, rv1, s1 = observe(c1, v)
    vt2, rv2, s2 = observe(c2, v + dv)
    sep = c1.separation(c2).to_value(u.rad)               # astropy's own separation and position angle
    pa_obs = c1.position_angle(c2).to_value(u.rad)
    e_hat = np.stack([np.sin(pa_obs), np.cos(pa_obs)])    # (east, north) toward star 2, star 1's basis
    return dict(c1=c1, c2=c2, s1=s1, s2=s2, v=v, dv=dv, vt1=vt1, vt2=vt2, rv1=rv1, rv2=rv2,
                v_r=0.5 * (rv1 + rv2), theta=sep, e_hat=e_hat, speed=np.linalg.norm(v, axis=0))


@pytest.fixture(scope="module")
def pairs():
    return make_pairs(np.random.default_rng(SEED), N_PAIRS)


def one_basis_difference(p):
    """Star 2 minus star 1 tangential velocity, both in star 1's basis (to second order), from astropy."""
    return np.stack([offset_frame_tangential(p["s2"][i], p["c1"][i]) - offset_frame_tangential(p["s1"][i], p["c1"][i])
                     for i in range(len(p["theta"]))], axis=1)


@pytest.fixture(scope="module")
def dv_one(pairs):
    return one_basis_difference(pairs)


def test_geometry_receding_pair_converges():
    """Physics, no code under test: one shared velocity with v_r > 0 makes the pair look like it is closing,
    a difference of -v_r*theta along the star-1-to-star-2 direction."""
    theta, v_r = 1e-3, 30.0
    c1 = SkyCoord(ra=0 * u.deg, dec=0 * u.deg, distance=100 * u.pc, frame="icrs")
    c2 = c1.directional_offset_by(90 * u.deg, theta * u.rad)
    c2 = SkyCoord(ra=c2.ra, dec=c2.dec, distance=100 * u.pc, frame="icrs")
    v = np.array([v_r, 0.0, 0.0])
    vt1, _, _ = observe(c1, v)
    vt2, _, _ = observe(c2, v)
    along = (vt2 - vt1)[0]                                # east is the separation direction here
    assert along < 0
    assert along == pytest.approx(-v_r * np.sin(theta), rel=1e-9)


def test_stamped_function_doubles_the_term(pairs, dv_one):
    """The stamped correct_perspective() moves the residual to about -2*v_r*theta*e_hat instead of removing it."""
    p = pairs
    out = np.array(stamped(dv_one[0], dv_one[1], p["v_r"], p["theta"], p["e_hat"]))
    ratio = np.linalg.norm(out, axis=0) / (2 * np.abs(p["v_r"]) * p["theta"])
    mask = np.abs(p["v_r"]) > 5                           # avoid dividing by a near-zero term
    assert np.median(ratio[mask]) == pytest.approx(1.0, abs=0.02)


def test_first_order_fix_in_one_basis(pairs, dv_one):
    """v2.correct_perspective() on a one-basis difference leaves only a second-order remainder."""
    p = pairs
    out = np.array(v2.correct_perspective(dv_one[0], dv_one[1], p["v_r"], p["theta"], p["e_hat"]))
    resid = np.linalg.norm(out, axis=0)
    bound = p["theta"] ** 2 * p["speed"] + 1e-9
    assert np.all(resid <= bound), f"worst residual/bound {np.max(resid / bound):.3f}"
    small = p["theta"] <= 1e-3
    assert resid[small].max() < 1e-4                      # km/s, the range the E2b sample occupies


def test_exact_method_on_raw_components(pairs):
    """v2.relative_tangential() on raw per-star east/north components (what Gaia publishes) returns ~0."""
    p = pairs
    resid = np.array([np.linalg.norm(v2.relative_tangential(
        p["c1"][i].ra.rad, p["c1"][i].dec.rad, p["c2"][i].ra.rad, p["c2"][i].dec.rad,
        p["vt1"][:, i], p["vt2"][:, i], p["v_r"][i])) for i in range(len(p["theta"]))])
    bound = p["theta"] ** 2 * p["speed"] + 1e-9
    assert np.all(resid <= bound), f"worst residual/bound {np.max(resid / bound):.3f}"


def test_exact_method_with_star1_rv_is_exact(pairs):
    """With star 1's own radial velocity in place of the pair mean, the exact method has no geometric remainder."""
    p = pairs
    resid = np.array([np.linalg.norm(v2.relative_tangential(
        p["c1"][i].ra.rad, p["c1"][i].dec.rad, p["c2"][i].ra.rad, p["c2"][i].dec.rad,
        p["vt1"][:, i], p["vt2"][:, i], p["rv1"][i])) for i in range(len(p["theta"]))])
    assert resid.max() < 1e-8


def test_exact_method_recovers_an_injected_relative_velocity():
    """Give star 2 an extra ~0.5 km/s. relative_tangential() must return that extra velocity as projected at star 2
    (astropy's answer), up to theta^2*|v| + theta*|dv|."""
    rng = np.random.default_rng(SEED + 1)
    p = make_pairs(rng, 600, dv_sigma=0.5)
    truth = np.stack([observe(p["c2"][i], p["v"][:, i] + p["dv"][:, i])[0] - observe(p["c2"][i], p["v"][:, i])[0]
                      for i in range(600)], axis=1)
    got = np.stack([v2.relative_tangential(
        p["c1"][i].ra.rad, p["c1"][i].dec.rad, p["c2"][i].ra.rad, p["c2"][i].dec.rad,
        p["vt1"][:, i], p["vt2"][:, i], p["v_r"][i]) for i in range(600)], axis=1)
    err = np.linalg.norm(got - truth, axis=0)
    bound = p["theta"] ** 2 * p["speed"] + p["theta"] * np.linalg.norm(p["dv"], axis=0) + 1e-9
    assert np.all(err <= bound), f"worst error/bound {np.max(err / bound):.3f}"


def test_raw_differences_need_basis_treatment():
    """Hazard check: the first-order formula applied to raw per-star component differences leaves a first-order
    error from the turn between the two stars' east/north bases, largest far from the equator."""
    rng = np.random.default_rng(SEED + 2)
    p = make_pairs(rng, 400, dec_range=(0.87, 0.999))     # |dec| above ~60 deg
    raw = p["vt2"] - p["vt1"]
    out = np.array(v2.correct_perspective(raw[0], raw[1], p["v_r"], p["theta"], p["e_hat"]))
    ratio = np.linalg.norm(out, axis=0) / (p["theta"] * p["speed"])
    assert np.median(ratio) > 0.2
