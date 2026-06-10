"""Approximate recombination, optical-depth, visibility, and thickness utilities."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.constants import c, m_p
from scipy.integrate import cumulative_trapezoid, trapezoid

from .constants import Cosmology, H_z, MPC_METERS, SIGMA_T


@dataclass(frozen=True)
class ThicknessResult:
    z: np.ndarray
    x_e: np.ndarray
    tau: np.ndarray
    visibility: np.ndarray
    z_star: float
    sigma_z: float
    thickness_physical_mpc: float
    thickness_comoving_mpc: float


def recombination_history(
    z: np.ndarray,
    z_rec: float = 1089.0,
    delta_z: float = 80.0,
    x_e_residual: float = 2e-4,
) -> np.ndarray:
    """Return a smooth tanh toy ionization history x_e(z)."""

    return x_e_residual + 0.5 * (1.0 - x_e_residual) * (
        1.0 + np.tanh((z - z_rec) / delta_z)
    )


def inflation_modified_recombination_history(
    z: np.ndarray,
    ns: float,
    r: float,
    z_rec: float = 1089.0,
    base_width: float = 80.0,
) -> tuple[np.ndarray, float]:
    """Toy recombination width with a weak phenomenological dependence on ns and r."""

    tilt_effect = 1.0 + 0.8 * (ns - 0.965)
    tensor_effect = 1.0 + 0.15 * r
    delta_z = max(base_width * tilt_effect * tensor_effect, 40.0)
    return recombination_history(z, z_rec=z_rec, delta_z=delta_z), delta_z


def compute_visibility(
    z: np.ndarray,
    x_e: np.ndarray,
    cosmology: Cosmology = Cosmology(),
) -> ThicknessResult:
    """Compute optical depth, normalized visibility g(z), and last-scattering thickness."""

    n_b = cosmology.rho_b0 * (1.0 + z) ** 3 / m_p
    n_e = x_e * n_b * (1.0 - cosmology.Yp / 2.0)
    dtaudz = c * SIGMA_T * n_e / ((1.0 + z) * H_z(z, cosmology))

    z_forward = z[::-1]
    tau_forward = cumulative_trapezoid(dtaudz[::-1], z_forward, initial=0.0)
    tau = tau_forward[::-1]

    visibility = np.exp(-tau) * dtaudz
    norm = trapezoid(visibility[::-1], z[::-1])
    if norm <= 0 or not np.isfinite(norm):
        raise ValueError("Visibility normalization failed; check z-grid and ionization history.")
    visibility = visibility / norm

    z_star = float(trapezoid(z[::-1] * visibility[::-1], z[::-1]))
    z_var = float(trapezoid((z[::-1] - z_star) ** 2 * visibility[::-1], z[::-1]))
    sigma_z = float(np.sqrt(max(z_var, 0.0)))

    delta_t = sigma_z / ((1.0 + z_star) * H_z(z_star, cosmology))
    thickness_physical_mpc = float(c * delta_t / MPC_METERS)
    thickness_comoving_mpc = float(thickness_physical_mpc * (1.0 + z_star))

    return ThicknessResult(
        z=z,
        x_e=x_e,
        tau=tau,
        visibility=visibility,
        z_star=z_star,
        sigma_z=sigma_z,
        thickness_physical_mpc=thickness_physical_mpc,
        thickness_comoving_mpc=thickness_comoving_mpc,
    )
