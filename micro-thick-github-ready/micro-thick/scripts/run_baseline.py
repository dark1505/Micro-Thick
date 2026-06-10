"""Run the baseline Micro-Thick CMB thickness simulation."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from micro_thick.constants import Cosmology, E_z, MPC_METERS
from micro_thick.recombination import compute_visibility, recombination_history
from micro_thick.spectra import sound_horizon, toy_cmb_spectrum
from micro_thick.plotting import plot_baseline


def run(output_dir: Path) -> dict[str, float]:
    cosmology = Cosmology()
    z = np.linspace(3000.0, 100.0, 6000)
    x_e = recombination_history(z)
    thickness = compute_visibility(z, x_e, cosmology)
    r_s_comoving = sound_horizon(z, thickness.z_star, cosmology)
    ell, Dl = toy_cmb_spectrum(cosmology.ns, r_s_comoving, cosmology=cosmology, ell_max=2500)

    output_dir.mkdir(parents=True, exist_ok=True)
    plot_baseline(
        z=z,
        x_e=x_e,
        visibility=thickness.visibility,
        z_star=thickness.z_star,
        sigma_z=thickness.sigma_z,
        E=E_z(z, cosmology),
        ell=ell,
        Dl=Dl,
        output=output_dir / "baseline_micro_thick.png",
    )

    return {
        "z_star": thickness.z_star,
        "sigma_z": thickness.sigma_z,
        "physical_mpc": thickness.thickness_physical_mpc,
        "comoving_mpc": thickness.thickness_comoving_mpc,
        "sound_horizon_mpc": r_s_comoving / MPC_METERS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the baseline Micro-Thick CMB thickness simulation.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/figures"), help="Directory for PNG output.")
    args = parser.parse_args()
    summary = run(args.output_dir)
    print("Micro-Thick baseline simulation")
    print(f"Mean last-scattering redshift: z* = {summary['z_star']:.1f}")
    print(f"CMB thickness in redshift: sigma_z = {summary['sigma_z']:.1f}")
    print(f"Physical thickness: {summary['physical_mpc']:.3f} Mpc")
    print(f"Comoving thickness: {summary['comoving_mpc']:.1f} Mpc")
    print(f"Approximate sound horizon: {summary['sound_horizon_mpc']:.1f} Mpc")
    print(f"Saved figure to: {args.output_dir / 'baseline_micro_thick.png'}")


if __name__ == "__main__":
    main()
