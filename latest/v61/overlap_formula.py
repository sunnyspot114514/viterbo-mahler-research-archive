"""Exact two-pair cube extension formula. Fractions only for numerical inputs.

The formula permits arbitrary cap overlap. Geometric derivations and the
four-dimensional lower-bound proof are in report_zh.md. This module by itself
is not a proof of the inequality for all parameters.
"""
from fractions import Fraction as F
from math import factorial
from typing import Sequence


def _validate(q: Sequence, r: Sequence):
    q, r = tuple(map(F, q)), tuple(map(F, r))
    n = len(q)
    if n < 2 or len(r) != n:
        raise ValueError('Two vectors of the same dimension >= 2 required')
    if q[0] <= 1 or r[1] <= 1:
        raise ValueError('Strict outward coordinates q[0]>1 and r[1]>1 required')
    if any(abs(q[j]) > 1 for j in range(1, n)):
        raise ValueError('q has a second outward coordinate')
    if any(abs(r[j]) > 1 for j in range(n) if j != 1):
        raise ValueError('r has a second outward coordinate')
    return q, r


def directed_overlap(q: Sequence, r: Sequence) -> F:
    """Volume in B_1^n with q.y>=1 and r.y>=1 (both own signs positive)."""
    q, r = _validate(q, r)
    n = len(q)
    a, u, v, b = q[0], q[1], r[0], r[1]
    delta = (a - 1)*(b - 1) - (1 - u)*(1 - v)
    if delta <= 0:
        return F(0)
    det = a*b - u*v
    alpha, beta = a-u, b-v
    denominator = F(factorial(n))*alpha*beta
    for j in range(2, n):
        L = beta*q[j] + alpha*r[j]
        factor = det*det - L*L
        if factor <= 0:
            raise AssertionError('Positive overlap denominator required')
        denominator *= factor
    return F(2**(n-2))*delta**n*det**(n-3)/denominator


def volumes(q: Sequence, r: Sequence) -> dict:
    q, r = _validate(q, r)
    n = len(q)
    a, u, v, b = q[0], q[1], r[0], r[1]
    x, y = a-1, b-1
    dp = x*y - (1-u)*(1-v)
    dm = x*y - (1+u)*(1+v)
    V0 = F(2**n, n)*(n+x+y)
    bridge = F(2**(n-1), n*(n-1))*(max(dp, 0)+max(dm, 0))
    Wcube = F(2**n, factorial(n))
    singles = []
    for i, p in enumerate((q, r)):
        ai, xi = p[i], p[i]-1
        den = F(1)
        for j in range(n):
            if j != i:
                den *= ai*ai - p[j]*p[j]
        singles.append(Wcube*xi**n*ai**(n-2)/den)
    # Flip axis 1 and the second antipodal representative for the minus pair.
    qm = tuple(-q[j] if j == 1 else q[j] for j in range(n))
    rm = tuple(r[j] if j == 1 else -r[j] for j in range(n))
    op, om = directed_overlap(q, r), directed_overlap(qm, rm)
    W0 = Wcube-sum(singles)
    V, W = V0+bridge, W0+2*(op+om)
    if V <= 0 or W <= 0:
        raise AssertionError('Full-dimensional cube-containing body must have positive volumes')
    return dict(dimension=n, delta_plus=dp, delta_minus=dm,
                naive_primal=V0, primal_bridge=bridge, primal=V,
                base_polar=Wcube, single_cap_pairs=singles,
                naive_polar=W0, overlap_plus=op, overlap_minus=om,
                polar_overlap_correction=2*(op+om), polar=W,
                product=V*W)
