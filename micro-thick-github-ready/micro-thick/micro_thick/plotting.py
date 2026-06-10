"""Plotting helpers for Micro-Thick simulations."""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def save_figure(fig, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def plot_baseline(z, x_e, visibility, z_star, sigma_z, E, ell, Dl, output: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    axes[0, 0].plot(z, x_e)
    axes[0, 0].invert_xaxis()
    axes[0, 0].set_xlabel(r"Redshift $z$")
    axes[0, 0].set_ylabel(r"Ionization fraction $x_e(z)$")
    axes[0, 0].set_title("Approximate recombination history")
    axes[0, 0].grid(alpha=0.3)

    axes[0, 1].plot(z, visibility)
    axes[0, 1].axvline(z_star, linestyle="--", label=fr"$z_*={z_star:.0f}$")
    axes[0, 1].axvspan(z_star - sigma_z, z_star + sigma_z, alpha=0.2, label=fr"$\sigma_z={sigma_z:.0f}$")
    axes[0, 1].invert_xaxis()
    axes[0, 1].set_xlabel(r"Redshift $z$")
    axes[0, 1].set_ylabel(r"Visibility $g(z)$")
    axes[0, 1].set_title("CMB last-scattering thickness")
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)

    axes[1, 0].plot(z, E)
    axes[1, 0].invert_xaxis()
    axes[1, 0].set_xlabel(r"Redshift $z$")
    axes[1, 0].set_ylabel(r"$E(z)=H(z)/H_0$")
    axes[1, 0].set_title("Expansion function")
    axes[1, 0].grid(alpha=0.3)

    axes[1, 1].plot(ell, Dl)
    axes[1, 1].set_xlabel(r"Multipole $\ell$")
    axes[1, 1].set_ylabel(r"$D_\ell=\ell(\ell+1)C_\ell/2\pi$")
    axes[1, 1].set_title("Toy CMB temperature spectrum")
    axes[1, 1].set_xlim(2, 2500)
    axes[1, 1].grid(alpha=0.3)
    save_figure(fig, output)


def plot_model_comparisons(z, results: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for key, ylabel, title, filename in [
        ("visibility", r"Visibility function $g(z)$", "CMB last-scattering thickness for different inflationary models", "visibility_models.png"),
        ("x_e", r"Ionization fraction $x_e(z)$", "Approximate recombination histories", "ionization_models.png"),
    ]:
        fig = plt.figure(figsize=(9, 5))
        for model, res in results.items():
            plt.plot(z, res[key], label=model)
        plt.gca().invert_xaxis()
        plt.xlabel(r"Redshift $z$")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(alpha=0.3)
        plt.legend()
        save_figure(fig, output_dir / filename)

    models = list(results.keys())
    x = np.arange(len(models))
    for key, ylabel, title, filename in [
        ("sigma_z", r"CMB thickness $\sigma_z$", "CMB thickness in redshift space", "sigma_z_bar.png"),
        ("thickness_comoving_mpc", "Comoving thickness [Mpc]", "Comoving thickness of the last-scattering surface", "comoving_thickness_bar.png"),
    ]:
        fig = plt.figure(figsize=(9, 5))
        plt.bar(x, [results[m][key] for m in models])
        plt.xticks(x, models, rotation=30, ha="right")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(axis="y", alpha=0.3)
        save_figure(fig, output_dir / filename)

    fig = plt.figure(figsize=(10, 5))
    for model, res in results.items():
        plt.plot(res["ell"], res["Dl"], label=model)
    plt.xlabel(r"Multipole $\ell$")
    plt.ylabel(r"$D_\ell=\ell(\ell+1)C_\ell/2\pi\ [\mu K^2]$")
    plt.title("Toy CMB temperature spectra from inflationary initial conditions")
    plt.xlim(2, 2500)
    plt.ylim(0, 7000)
    plt.grid(alpha=0.3)
    plt.legend()
    save_figure(fig, output_dir / "toy_spectra_models.png")

    fig = plt.figure(figsize=(7, 5))
    ns_values = [results[m]["ns"] for m in models]
    r_values = [results[m]["r"] for m in models]
    plt.scatter(ns_values, r_values)
    for m, ns_val, r_val in zip(models, ns_values, r_values):
        plt.text(ns_val + 0.0005, r_val, m, fontsize=9)
    plt.xlabel(r"Scalar spectral index $n_s$")
    plt.ylabel(r"Tensor-to-scalar ratio $r$")
    plt.title("Inflationary model predictions")
    plt.grid(alpha=0.3)
    save_figure(fig, output_dir / "inflation_parameters.png")
