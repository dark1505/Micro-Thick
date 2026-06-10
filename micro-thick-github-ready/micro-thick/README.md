# Micro-Thick — Cosmic Microwave Background Thickness

**Micro-Thick** is a small Python research-code project for toy simulations of the thickness of the Cosmic Microwave Background last-scattering surface. It converts two standalone scripts into a GitHub-ready, executable, testable project.

The project contains:

- a baseline CMB thickness simulation;
- an inflation-model comparison simulation;
- reusable modules for cosmological constants, recombination, visibility, sound horizon, toy spectra, and plotting;
- command-line scripts;
- automated tests;
- GitHub Actions CI.

> Scientific note: this is a pedagogical/toy model. It is useful for exploring dependencies and visualization, but it is not a replacement for precision Boltzmann solvers such as CAMB or CLASS.

## Repository organization

```text
micro-thick/
├── micro_thick/
│   ├── __init__.py
│   ├── constants.py          # physical constants and default cosmology
│   ├── recombination.py      # tanh recombination, optical depth, visibility, thickness
│   ├── spectra.py            # sound horizon, Silk damping, toy CMB spectra
│   ├── inflation.py          # Starobinsky, quadratic, quartic, natural, alpha-attractor mappings
│   └── plotting.py           # headless PNG plot generation
├── scripts/
│   ├── run_baseline.py       # executable version of the first code
│   └── run_inflation_models.py # executable version of the second code
├── tests/
│   └── test_micro_thick.py   # numerical smoke tests
├── outputs/
│   └── figures/              # generated plots are saved here
├── .github/workflows/
│   └── python-ci.yml         # GitHub Actions CI
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

```bash
git clone https://github.com/YOUR-USERNAME/micro-thick.git
cd micro-thick
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Run the baseline simulation

```bash
python scripts/run_baseline.py --output-dir outputs/figures
```

This prints the last-scattering redshift, redshift thickness, physical thickness, comoving thickness, and approximate sound horizon. It also saves:

```text
outputs/figures/baseline_micro_thick.png
```

## Run the inflation-model comparison

```bash
python scripts/run_inflation_models.py --output-dir outputs/figures
```

This compares the following toy inflationary models:

- Starobinsky;
- Quadratic;
- Quartic;
- Natural inflation;
- Alpha-attractor.

It saves figures such as:

```text
outputs/figures/visibility_models.png
outputs/figures/ionization_models.png
outputs/figures/sigma_z_bar.png
outputs/figures/comoving_thickness_bar.png
outputs/figures/toy_spectra_models.png
outputs/figures/inflation_parameters.png
outputs/micro_thick_inflation_summary.csv
```

## Run tests

```bash
python -m pip install pytest
pytest -q
```

## GitHub upload steps

```bash
git init
git add .
git commit -m "Initial Micro-Thick CMB thickness simulation"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/micro-thick.git
git push -u origin main
```

## Citation / authorship placeholder

Author: **Khalil El Bourakadi**  
Simulation name: **Micro-Thick (Cosmic Microwave Background Thickness)**

## License

MIT License.
