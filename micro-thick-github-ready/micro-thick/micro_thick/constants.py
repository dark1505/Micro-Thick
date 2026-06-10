"""Physical constants and default cosmological parameters for Micro-Thick."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.constants import G, c, m_p

MPC_METERS = 3.085677581e22
SIGMA_T = 6.6524587321e-29


@dataclass(frozen=True)
class Cosmology:
    """Flat LCDM-like background parameters used by the toy simulations."""

    H0_km_s_Mpc: float = 67.4
    Omega_m: float = 0.315
    Omega_b: float = 0.049
    Omega_L: float = 0.685
    Omega_r: float = 9.2e-5
    T0: float = 2.7255
    Yp: float = 0.24
    As: float = 2.1e-9
    ns: float = 0.965

    @property
    def h(self) -> float:
        return self.H0_km_s_Mpc / 100.0

    @property
    def H0(self) -> float:
        return self.H0_km_s_Mpc * 1000.0 / MPC_METERS

    @property
    def rho_c0(self) -> float:
        return 3.0 * self.H0**2 / (8.0 * np.pi * G)

    @property
    def rho_b0(self) -> float:
        return self.Omega_b * self.rho_c0


def E_z(z, cosmology: Cosmology = Cosmology()):
    """Dimensionless expansion rate E(z)=H(z)/H0."""

    z = np.asarray(z)
    return np.sqrt(
        cosmology.Omega_r * (1.0 + z) ** 4
        + cosmology.Omega_m * (1.0 + z) ** 3
        + cosmology.Omega_L
    )


def H_z(z, cosmology: Cosmology = Cosmology()):
    """Hubble rate H(z) in SI units."""

    return cosmology.H0 * E_z(z, cosmology)
