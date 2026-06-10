"""Toy inflationary model parameter mappings used by Micro-Thick."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InflationModel:
    name: str
    N: float = 55.0
    alpha: float = 1.0
    f: float = 5.0


def inflation_parameters(model: InflationModel) -> tuple[float, float, float]:
    """Return approximate (n_s, r, A_s) for a named inflationary model."""

    As = 2.1e-9
    name = model.name.lower()
    N = model.N

    if name == "starobinsky":
        ns = 1.0 - 2.0 / N
        r = 12.0 / N**2
    elif name == "quadratic":
        ns = 1.0 - 2.0 / N
        r = 8.0 / N
    elif name == "quartic":
        ns = 1.0 - 3.0 / N
        r = 16.0 / N
    elif name == "natural":
        ns = 1.0 - (1.5 / N) * (1.0 + 1.0 / model.f)
        r = (8.0 / N) * (model.f**2 / (model.f**2 + 1.0))
    elif name in {"alpha-attractor", "alpha_attractor"}:
        ns = 1.0 - 2.0 / N
        r = 12.0 * model.alpha / N**2
    else:
        raise ValueError(f"Unknown inflation model: {model.name}")

    return float(ns), float(r), float(As)


def default_inflation_models() -> list[InflationModel]:
    return [
        InflationModel("Starobinsky"),
        InflationModel("Quadratic"),
        InflationModel("Quartic"),
        InflationModel("Natural"),
        InflationModel("Alpha-attractor", alpha=0.5),
    ]
