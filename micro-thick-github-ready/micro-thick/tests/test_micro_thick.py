from __future__ import annotations

import numpy as np

from micro_thick.constants import Cosmology, E_z
from micro_thick.inflation import InflationModel, inflation_parameters
from micro_thick.recombination import compute_visibility, recombination_history
from micro_thick.spectra import sound_horizon, toy_cmb_spectrum


def test_expansion_rate_positive():
    z = np.array([0.0, 100.0, 1089.0])
    assert np.all(E_z(z) > 0)


def test_visibility_normalizes_and_thickness_positive():
    z = np.linspace(3000.0, 100.0, 1200)
    x_e = recombination_history(z)
    result = compute_visibility(z, x_e)
    integral = np.trapz(result.visibility[::-1], z[::-1])
    assert np.isclose(integral, 1.0, rtol=1e-2)
    assert 900.0 < result.z_star < 1300.0
    assert result.sigma_z > 0.0
    assert result.thickness_comoving_mpc > 0.0


def test_spectrum_is_finite():
    z = np.linspace(3000.0, 100.0, 1200)
    x_e = recombination_history(z)
    result = compute_visibility(z, x_e)
    r_s = sound_horizon(z, result.z_star)
    ell, Dl = toy_cmb_spectrum(Cosmology().ns, r_s, result.sigma_z, ell_max=500)
    assert len(ell) == len(Dl)
    assert np.all(np.isfinite(Dl))
    assert np.max(Dl) > 0.0


def test_inflation_parameters_known_model():
    ns, r, As = inflation_parameters(InflationModel("Starobinsky", N=55))
    assert 0.9 < ns < 1.0
    assert 0.0 < r < 0.01
    assert As > 0.0
