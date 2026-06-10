"""Run Micro-Thick across several toy inflationary models."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

from micro_thick.constants import Cosmology, MPC_METERS
from micro_thick.inflation import default_inflation_models, inflation_parameters
from micro_thick.plotting import plot_model_comparisons
from micro_thick.recombination import compute_visibility, inflation_modified_recombination_history
from micro_thick.spectra import sound_horizon, toy_cmb_spectrum


def run(output_dir: Path) -> dict[str, dict]:
    cosmology = Cosmology()
    z = np.linspace(3000.0, 20.0, 8000)
    results: dict[str, dict] = {}

    for model in default_inflation_models():
        ns, r, As = inflation_parameters(model)
        x_e, delta_z_model = inflation_modified_recombination_history(z, ns, r)
        thickness = compute_visibility(z, x_e, cosmology)
        r_s_comoving = sound_horizon(z, thickness.z_star, cosmology)
        ell, Dl = toy_cmb_spectrum(ns, r_s_comoving, thickness.sigma_z, r=r, cosmology=cosmology)

        results[model.name] = {
            "ns": ns,
            "r": r,
            "As": As,
            "x_e": x_e,
            "tau": thickness.tau,
            "visibility": thickness.visibility,
            "z_star": thickness.z_star,
            "sigma_z": thickness.sigma_z,
            "thickness_physical_mpc": thickness.thickness_physical_mpc,
            "thickness_comoving_mpc": thickness.thickness_comoving_mpc,
            "r_s_mpc": r_s_comoving / MPC_METERS,
            "ell": ell,
            "Dl": Dl,
            "delta_z_model": delta_z_model,
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    plot_model_comparisons(z, results, output_dir)

    csv_path = output_dir.parent / "micro_thick_inflation_summary.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["model", "ns", "r", "z_star", "sigma_z", "physical_mpc", "comoving_mpc", "sound_horizon_mpc"])
        for model_name, res in results.items():
            writer.writerow([
                model_name,
                f"{res['ns']:.8f}",
                f"{res['r']:.8f}",
                f"{res['z_star']:.6f}",
                f"{res['sigma_z']:.6f}",
                f"{res['thickness_physical_mpc']:.8f}",
                f"{res['thickness_comoving_mpc']:.6f}",
                f"{res['r_s_mpc']:.6f}",
            ])
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Micro-Thick for several toy inflationary models.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/figures"), help="Directory for PNG output.")
    args = parser.parse_args()
    results = run(args.output_dir)

    print("\nCMB thickness simulation summary")
    print("-" * 95)
    print(f"{'Model':<18} {'n_s':>8} {'r':>8} {'z_*':>10} {'sigma_z':>10} {'phys Mpc':>12} {'com Mpc':>12} {'r_s Mpc':>12}")
    print("-" * 95)
    for model, res in results.items():
        print(
            f"{model:<18} {res['ns']:>8.4f} {res['r']:>8.4f} {res['z_star']:>10.1f} "
            f"{res['sigma_z']:>10.1f} {res['thickness_physical_mpc']:>12.4f} "
            f"{res['thickness_comoving_mpc']:>12.1f} {res['r_s_mpc']:>12.1f}"
        )
    print(f"Saved figures to: {args.output_dir}")
    print(f"Saved summary CSV to: {args.output_dir.parent / 'micro_thick_inflation_summary.csv'}")


if __name__ == "__main__":
    main()
