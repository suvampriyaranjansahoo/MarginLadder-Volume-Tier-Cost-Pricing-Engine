"""Sample sizes for the pilot. Standard library only.

Question: how many RFQs do we need before a rise in the share sent within 4 working days is more than noise?
Two independent periods (before and after), two-sided 5% test, 80% power, normal approximation.
Limits: periods are not randomised, so seasonality and customer mix can fake or hide an effect.
"""
from __future__ import annotations

from math import ceil, sqrt
from statistics import NormalDist

Z = NormalDist().inv_cdf


def n_per_period(p0: float, p1: float, alpha: float = 0.05, power: float = 0.80) -> int:
    if not (0 < p0 < 1 and 0 < p1 < 1) or p0 == p1:
        raise ValueError("p0 and p1 must differ and lie strictly between 0 and 1")
    pbar = (p0 + p1) / 2
    top = Z(1 - alpha / 2) * sqrt(2 * pbar * (1 - pbar)) + Z(power) * sqrt(p0 * (1 - p0) + p1 * (1 - p1))
    return ceil(top ** 2 / (p1 - p0) ** 2)


def minimum_detectable_rate(p0: float, n: int, alpha: float = 0.05, power: float = 0.80) -> float | None:
    """Smallest p1 above p0 that n RFQs per period can detect, or None if even 99.9% cannot be."""
    lo, hi = p0 + 1e-6, 0.999
    if n_per_period(p0, hi, alpha, power) > n:
        return None
    for _ in range(60):
        mid = (lo + hi) / 2
        if n_per_period(p0, mid, alpha, power) > n:
            lo = mid
        else:
            hi = mid
    return ceil(hi * 1000) / 1000


if __name__ == "__main__":
    print("RFQs needed in each period (80% power, 5% two-sided)")
    for p0 in (0.10, 0.20, 0.30):
        print(f"  baseline {p0:.0%}: " + ", ".join(f"to {p1:.0%} = {n_per_period(p0, p1)}" for p1 in (0.35, 0.50, 0.70)))
    for n in (30, 60, 90, 180):
        print(f"  with {n} RFQs a period, from 10% the smallest detectable rate is {minimum_detectable_rate(0.10, n)}")
