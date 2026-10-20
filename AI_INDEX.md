# AI evidence index

Read [the manuscript](paper.md) before relying on a result. Version 1.1, 20 October 2026.

Start with [status](STATUS.md), [assurance boundaries](ASSURANCE.md),
[claims](CLAIMS.json), [source audit](CITATION_AUDIT.md) and
[replay instructions](README.md). The [exact verifier](verify.py) and
[negative-control harness](test_verifier.py) have a retained
[replay summary](evidence/replay-20261020/summary.json).

| Claim | Exact scope | Primary evidence | Computational coverage |
|---|---|---|---|
| Counterexample | Source Conjecture 1 under its actual graph hypotheses | Theorem 1, equations (3)-(8) | m=2 and exact phase checks |
| Exponent family | Every integer m >= 2; dimension m+2 | Theorem 2, binomial identity (17) | Rational checks only m=2,...,25 |
| No uniform extra power | Across increasing dimensions | Corollary 3 | Analytic consequence, not an exhaustive search |
| Four-state minimum | Strictly positive initial data; both graph hypotheses | Lemma 4 and Theorem 5 | Analytic case proof, not model enumeration |
| Phase boundary | The displayed fixed four-state coefficient tensor | Theorem 6 | Three rational examples only |
| Spectral equivalence | Transition DAG; nonempty vanishing set; strictly positive initial fractions; known trajectory limit | Theorem 7 | Analytic positivity/comparison proof |
| Logarithmic rate | Aggregate l1 norm; full trajectory only for negative spectral bound | Corollary 8 | Analytic two-sided comparison, separately AI-checked |

## Evidence boundaries

Formal proof-assistant verification: not performed.
External human peer review: not claimed.
Independent empirical reproduction: not applicable to this mathematical model.
Finite exact replay: completed, with normal and optimized checks plus six rejected
corruptions. Review and replay do not certify novelty.

Strict positivity matters. The spectral criterion is not a graph-only algorithm
for finding the limiting population. A zero aggregate exponential rate does not
specify each coordinate's tail. Arbitrary perturbations can remove the critical
algebraic behaviour. The classical scalar and positive-matrix tools are not
claimed as new.
