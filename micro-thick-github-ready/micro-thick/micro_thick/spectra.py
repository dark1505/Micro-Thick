"""Sound-horizon and toy CMB angular-spectrum functions."""

from __future__ import annotations

import numpy as np
from scipy.constants import c
from scipy.integrate import trapezoid

from .constants import Cosmology, H_z, MPC_METERS


def sound_horizon(z: np.ndarray, z_star: float, cosmology: Cosmology = Cosmology()) -> float:
    """Approximate comoving sound horizon in meters."""

    R_b = 3.0 * cosmology.Omega_b / (4.0 * cosmology.Omega_r) / (1.0 + z)
    c_s = c / np.sqrt(3.0 * (1.0 + R_b))
    mask = z > z_star
    if not np.any(mask):
        raise ValueError("z-grid must contain redshifts larger than z_star.")
    r_s_physical = trapezoid((c_s / H_z(z, cosmology))[mask][::-1], z[mask][::-1])
    return float(r_s_physical * (1.0 + z_star))


def diffusion_damping_scale(cosmology: Cosmology = Cosmology()) -> float:
    """Simple phenomenological Silk damping scale in multipole space."""

    return float(1350.0 * (cosmology.Omega_b / 0.049) ** 0.25 * (cosmology.Omega_m / 0.315) ** 0.1)


def toy_cmb_spectrum(
    ns: float,
    r_s_comoving_m: float,
    z_sigma: float | None = None,
    r: float = 0.0,
    cosmology: Cosmology = Cosmology(),
    ell_max: int = 3000,
) -> tuple[np.ndarray, np.ndarray]:
    """Return a toy temperature spectrum D_ell in micro-K^2."""

    ell = np.arange(2, ell_max)
    D_A_comoving_mpc = 14000.0
    ell_A = np.pi * D_A_comoving_mpc / (r_s_comoving_m / MPC_METERS)
    ell_D = diffusion_damping_scale(cosmology)

    primordial_scalar = cosmology.As * (ell / 100.0) ** (ns - 1.0)
    acoustic = 1.0 + 0.70 * np.cos(2.0 * np.pi * ell / ell_A) + 0.25 * np.cos(4.0 * np.pi * ell / ell_A)
    silk_damping = np.exp(-(ell / ell_D) ** 1.35)
    thickness_damping = 1.0 if z_sigma is None else np.exp(-((ell * z_sigma / 90000.0) ** 2))
    sachs_wolfe = 1.0 / (ell * (ell + 1.0))
    tensor_bump = r * 0.12 * np.exp(-0.5 * ((ell - 80.0) / 45.0) ** 2)

    Cl = primordial_scalar * acoustic**2 * silk_damping * thickness_damping * sachs_wolfe
    Dl = ell * (ell + 1.0) * Cl / (2.0 * np.pi)
    Dl = Dl / np.max(Dl) * 5700.0 + tensor_bump * 5700.0
    return ell, Dl
