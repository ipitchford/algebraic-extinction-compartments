#!/usr/bin/env python3
"""Exact, dependency-free checks of the proposed compartment construction.

This replays finite instances; the arbitrary-m theorem is proved in the paper.
Polynomials have rational coefficients in ascending powers of z.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import hashlib
import json
import argparse
import sys


def require(condition, message="exact verification failed"):
    """A check that remains active under Python's -O mode."""
    if not condition:
        raise ValueError(message)


def trim(p):
    p = list(map(Q, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(a, b):
    c = [Q(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] += x
    for i, x in enumerate(b):
        c[i] += x
    return trim(c)


def scale(a, c):
    return trim([x*c for x in a])


def mul(a, b):
    c = [Q(0)] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)


def derivative(a):
    return trim([i*a[i] for i in range(1, len(a))] or [0])


def evaluate(a, z):
    ans = Q(0)
    for c in reversed(a):
        ans = ans*z+c
    return ans


def acyclic(vertices, edges):
    vertices = set(vertices)
    edges = {(i, j) for i, j in edges if i in vertices and j in vertices}
    remaining = set(vertices)
    while remaining:
        available = {v for v in remaining
                     if not any(j == v and i in remaining for i, j in edges)}
        if not available:
            return False
        remaining -= available
    return True


def instance(m):
    kap = Q(1, 2*3**m)
    active, removed = m, m+1
    profiles = [[kap*comb(m, k)*comb(k, j) for j in range(k+1)]
                for k in range(1, m+1)]
    profiles.append([Q(0)]*m+[kap])
    total = [Q(0)]
    for p in profiles:
        total = add(total, p)
    profiles.append(add([1], scale(total, -1)))
    # Build the ODE solely from individual conversion channels, not from the
    # closed-form derivative or a supplied system right-hand side.
    channels = []
    for k in range(1, m+1):
        if (m-k) % 2:
            channels.append((k-1, active, active, Q(k)))
        else:
            channels.append((k-1, active, removed, Q(k)))
            channels.append((active, k-1, removed, Q(k)))
    rhs = [[Q(0)] for _ in profiles]
    for source, catalyst, destination, rate in channels:
        require(rate > 0 and source != destination, "invalid channel")
        flux = scale(mul(profiles[source], profiles[catalyst]), rate)
        rhs[source] = add(rhs[source], scale(flux, -1))
        rhs[destination] = add(rhs[destination], flux)
    zdot = [Q(0)]*m+[-kap, -kap]
    for p, f in zip(profiles, rhs):
        require(trim(f) == mul(derivative(p), zdot), "trajectory residual")
    require(trim(sum_polynomials(profiles)) == [Q(1)], "normalisation polynomial")
    require(trim(sum_polynomials(rhs)) == [Q(0)], "conservation polynomial")
    initial = [evaluate(p, Q(1)) for p in profiles]
    limit = [evaluate(p, Q(0)) for p in profiles]
    require(all(0 < v < 1 for v in initial) and sum(initial) == 1, "initial fractions")
    require(limit[active] == 0, "vanishing activity")
    require(all(0 < v < 1 for i, v in enumerate(limit) if i != active), "persistent fractions")
    trans = {(i, j) for i, k, j, a in channels}
    dep = {(i, k) for i, k, j, a in channels}
    require(acyclic(range(m+2), trans), "transition cycle")
    persistent = {i for i, x in enumerate(limit) if x > 0}
    protected = {i for i, j in dep if j in persistent}
    # Every dependency cycle contains a protected vertex iff removing all
    # protected vertices leaves an acyclic induced graph.
    require(acyclic(set(range(m+2))-protected, dep), "unprotected dependency cycle")
    # I = - d/dt log(1+z) is checked after multiplication by 1+z.
    require(mul(profiles[active], [1, 1]) == scale(zdot, -1), "clock integral")
    return {
        'm': m, 'states': m+2, 'kappa': str(kap),
        'exponent': str(Q(m, m-1)),
        'initial': list(map(str, initial)), 'limit': list(map(str, limit)),
        'channels': [[i, k, j, str(a)] for i, k, j, a in channels],
        'transition_edges': sorted(map(list, trans)),
        'dependency_edges': sorted(map(list, dep)),
        'protected_vertices': sorted(protected),
        'all_polynomial_residuals_zero': True,
    }


def sum_polynomials(ps):
    ans = [Q(0)]
    for p in ps:
        ans = add(ans, p)
    return ans


def phase_checks():
    checks = []
    x = y = Q(2, 9)
    for activity in [Q(1, 36), Q(1, 18), Q(1, 12)]:
        removed = 1-x-y-activity
        K = activity+x-y
        delta = x*x-4*y*K
        profiles = [[0, x], [0, 0, y], [K, -x, y]]
        profiles.append(add([1], scale(sum_polynomials(profiles), -1)))
        udot = scale(mul([0, 1], profiles[2]), -1)
        X, Y, I, R = profiles
        rhs = [scale(mul(X, I), -1), scale(mul(Y, I), -2),
               mul(add(X, scale(Y, -2)), I), scale(mul(Y, I), 4)]
        require(all(mul(derivative(p), udot) == f
                    for p, f in zip(profiles, rhs)), "phase residual")
        require(sum([x, y, activity, removed]) == 1 and removed > 0, "phase initial data")
        # The linear invariant is exact for every polynomial coefficient.
        require(add(add(profiles[2], profiles[0]), scale(profiles[1], -1)) == [K], "phase invariant")
        checks.append({'I0':str(activity), 'R0':str(removed),
                       'K':str(K), 'discriminant':str(delta),
                       'regime':('exponential extinction' if delta>0 else
                                 'critical algebraic extinction' if delta==0 else
                                 'persistent activity'),
                       'all_polynomial_residuals_zero': True})
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("verification.json"))
    args = parser.parse_args()
    examples = [instance(m) for m in range(2, 26)]
    report = {
        'status':'PASS', 'arithmetic':'fractions.Fraction; exact polynomial coefficients',
        'm_range':[2,25], 'instances_checked':len(examples),
        'checks':['channel conservation', 'exact trajectory against channel-generated ODE',
                  'strictly positive normalised initial data', 'exact limiting fractions',
                  'transition acyclicity', 'dependency-cycle persistent-successor condition',
                  'internal-clock integral identity', 'three phase regimes'],
        'small_fingerprints':examples[:3], 'phase_checks':phase_checks(),
        'scope':'Finite replay checks do not replace the arbitrary-m analytic proof or the N<=3 proof.',
        'python_optimization': sys.flags.optimize,
        'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    out=args.output
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','arithmetic','m_range','instances_checked']},indent=2))
    print('verification_sha256='+hashlib.sha256(out.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
