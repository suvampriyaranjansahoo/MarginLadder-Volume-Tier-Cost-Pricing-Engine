"""Why do RFQs wait? A queueing view of the estimator team.

Model: RFQs arrive at a steady average rate and are costed by c estimators. Each RFQ is one
job of S work-hours. Erlang C gives the chance a new RFQ finds every estimator busy and the
average wait before costing starts. Allen-Cunneen scales that wait for uneven arrivals and
uneven job sizes (squared coefficients of variation, ca2 and cs2).

Limits [Judgement]: real estimators can split a job, pause it and take urgent work, so this is
a pressure gauge, not a forecast. It uses only brief inputs. Productive hours per estimator
(160 a month) and an 8-hour working day are assumptions A4 and A5.
"""
from __future__ import annotations

from math import factorial

HOURS_PER_DAY = 8.0               # Assumption A5
PRODUCTIVE_HOURS_PER_MONTH = 160  # Assumption A4


def erlang_c(servers: int, offered_load: float) -> float:
    """Probability that an arriving job must wait. Needs offered_load < servers."""
    if servers < 1:
        raise ValueError("servers must be at least 1")
    if offered_load < 0:
        raise ValueError("offered_load cannot be negative")
    if offered_load >= servers:
        raise ValueError("the queue is unstable: offered load must be below the number of servers")
    top = offered_load ** servers / factorial(servers) * servers / (servers - offered_load)
    bottom = sum(offered_load ** k / factorial(k) for k in range(servers)) + top
    return top / bottom


def mean_wait_days(arrivals_per_month: float, job_hours: float, servers: int,
                   ca2: float = 1.0, cs2: float = 1.0) -> dict[str, float]:
    """Average wait before costing starts, in working days, plus load and wait probability."""
    if arrivals_per_month <= 0 or job_hours <= 0:
        raise ValueError("arrivals and job hours must be positive")
    lam = arrivals_per_month / PRODUCTIVE_HOURS_PER_MONTH      # RFQs per productive hour, whole team
    mu = 1.0 / job_hours                                       # RFQs per hour per estimator
    a = lam / mu
    if a >= servers:
        raise ValueError("the queue is unstable: load is 100% or more")
    c_prob = erlang_c(servers, a)
    wq_mmc = c_prob / (servers * mu - lam)                     # hours
    wq = wq_mmc * (ca2 + cs2) / 2
    return {"load": a / servers, "p_wait": c_prob, "wait_hours": wq, "wait_days": wq / HOURS_PER_DAY}


def load_table(job_hours: float = 12.5, servers: int = 6, arrivals: float = 60.0,
               scales=(0.6, 0.8, 1.0, 1.1, 1.2, 1.25), cs2: float = 1.0) -> list[dict[str, float]]:
    """Wait as arrivals grow. Shows the knee: small load changes near 80% move waits a lot."""
    rows = []
    for s in scales:
        try:
            r = mean_wait_days(arrivals * s, job_hours, servers, cs2=cs2)
            rows.append({"arrival_scale": s, "arrivals_per_month": arrivals * s, **r})
        except ValueError:
            rows.append({"arrival_scale": s, "arrivals_per_month": arrivals * s,
                         "load": arrivals * s * job_hours / (servers * PRODUCTIVE_HOURS_PER_MONTH),
                         "p_wait": 1.0, "wait_hours": float("inf"), "wait_days": float("inf")})
    return rows


def littles_law(arrivals_per_month: float, cycle_days: float, working_days_per_month: float = 20.0) -> float:
    """Average RFQs in progress = arrival rate x time in system (Little's law)."""
    return arrivals_per_month / working_days_per_month * cycle_days
