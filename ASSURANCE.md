# Assurance and limits

## Written mathematics

Theorem 1 explicitly contradicts Conjecture 1 in the inspected version
arXiv:2511.02437v1. Both graph hypotheses are checked on the same positive
trajectory. Theorems 2 and 5 prove the arbitrary multiplicity construction and
minimum compartment count. Theorems 6-7 give the exact four-state phase boundary
and the trajectory-dependent spectral equivalence. Corollary 8 supplies the
aggregate logarithmic rate and is proved by two-sided comparison.

## Executable evidence

`verify.py` uses rational polynomial arithmetic and constructs the ODE from
individual channels separately from the proposed solution. The retained replay
checks m=2,...,25, normalization, limits, both graph conditions, the clock identity
and three phase examples. Its explicit guards remain active under `python -O`.
`test_verifier.py` checks the child optimization flag and requires three scientific
corruptions to fail in both modes. These are finite internal replay and checker
sensitivity, not an independent experimental reproduction.

## Review

The supplied research had already undergone AI-assisted mathematical criticism.
Some of its reviewers participated in development; that is not external
independence. This revision received a separate read-only AI examination of the
new logarithmic-rate proof and surrounding manuscript. No external human referee
acceptance or formal proof-assistant certificate is asserted.

## Limits

The examples are critically tuned. Neither genericity nor robustness under
arbitrary perturbations is proved. The exponent family varies the dimension;
fixed-dimensional bounds are not settled. The spectral test needs the actual
limiting state, not merely the two graphs. Strictly positive initial fractions
are essential. The aggregate rate is not a coordinatewise-rate classification.
Source checking is bounded and cannot certify historical priority.

The figure is floating-point evaluation of an exact scalar quadrature. It is
illustrative, while the stated asymptotics are proved analytically.
