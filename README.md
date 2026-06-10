# Micro-Thick

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Status](https://img.shields.io/badge/Status-Research-orange.svg)]()

## Cosmic Microwave Background Thickness Simulation Framework

Micro-Thick is a cosmological simulation framework designed to study the physical thickness of the Cosmic Microwave Background (CMB) last-scattering surface.

The project models:

- Recombination history
- Ionization fraction evolution
- Optical depth
- Visibility function
- Last-scattering surface thickness
- Sound horizon evolution
- Inflationary cosmology effects
- Toy CMB angular power spectra
- Comparison between inflationary models

The code is intended for educational, research, and visualization purposes.

---

## Scientific Motivation

The Cosmic Microwave Background originates from the epoch of recombination when photons decoupled from baryonic matter approximately 380,000 years after the Big Bang.

The last-scattering surface is not infinitely thin.

Instead, recombination occurs over a finite redshift interval:

\[
\Delta z \sim 80-100
\]

which produces a measurable thickness of the CMB photosphere.

Micro-Thick investigates:

- The visibility function \(g(z)\)
- Physical thickness
- Comoving thickness
- Acoustic horizon scales
- Inflationary initial conditions

and their impact on observable CMB anisotropies.

---

### Toy CMB Spectrum

Acoustic oscillations

Silk damping

Thickness damping

Tensor contribution

---

## Inflationary Models

The framework currently supports:

### Starobinsky Inflation

### Quadratic Inflation

### Quartic Inflation

### Natural Inflation

### α-Attractor Inflation

# Project Structure

```text
Micro-Thick/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── scripts/
│   ├── run_baseline.py
│   └── run_inflation_models.py
│
├── microthick/
│   ├── __init__.py
│   ├── cosmology.py
│   ├── recombination.py
│   ├── inflation.py
│   ├── visibility.py
│   └── cmb.py
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── tests/
│   └── test_microthick.py
│
└── .github/
    └── workflows/
        └── python.yml


Installation

Clone repository

git clone https://github.com/dark1505/Micro-Thick.git

cd Micro-Thick

Install dependencies

pip install -r requirements.txt
