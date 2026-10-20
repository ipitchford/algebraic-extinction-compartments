# Algebraic extinction in acyclic compartment models

This repository accompanies a theoretical research note. A four-compartment
conservative quadratic model disproves the exponential-decay conjecture in
Chan, Crommelin and Mandjes, arXiv:2511.02437v1, Conjecture 1.

Candidate version: **1.0.0-candidate**. Reserved archive identifier:
[10.5281/zenodo.23501636](https://doi.org/10.5281/zenodo.23501636).
Source repository: [ipitchford/algebraic-extinction-compartments](https://github.com/ipitchford/algebraic-extinction-compartments).
Identifier reservation alone does not establish archive publication or DOI resolution.

## Read first

`paper.md` contains the complete proofs and context. Its explicit example has
positive integer rates, strictly positive rational initial fractions, and
activity asymptotic to 18/t², while its integrated activity equals log 2.
The paper proves four compartments are necessary, constructs exponents
m/(m−1) for every m ≥ 2, classifies the four-state threshold, and gives a
trajectory-dependent spectral criterion with an exact aggregate logarithmic rate.

These are exact mathematical constructions. They do not establish generic
algebraic decay, empirical epidemic behaviour, or historical priority.

## Reproduce the finite checks

Python 3, standard library only:

```sh
python3 -B test_verifier.py --output-dir /tmp/extinction-replay-new
```

Use a new output directory. The harness runs `verify.py` normally and with `-O`,
checks that the child really used the requested optimization mode, and requires
wrong normalization, a missing channel and a wrong removed-state flux to fail in
both modes. Published example receipts are in `evidence/replay-20261020`.

The 24 exact cases m=2,...,25 and three phase examples check transcription and
algebra. The arbitrary-m, minimum-dimension and spectral results depend on the
analytic proofs, not enumeration. This is not proof-assistant verification.

## Figure

`figures/decay_family.pdf` and `.png` illustrate the exact scalar quadrature.
`make_figure.py` requires NumPy, SciPy and Matplotlib. It is not needed for exact
verification. Inspect its output settings before regenerating a figure.

## Files

`AI_INDEX.md` maps claims to evidence. `REVISION_NOTES.md` records scientific
changes without internal assessments. `ABSTRACT.zh-TW.md` supplies an additional
Traditional Chinese abstract; the English manuscript is the authoritative text.
`CITATION_AUDIT.md` records bounded source checking and its limits.

Prose is dedicated under CC0-1.0. Code is available under the MIT licence.
The manuscript gives the anonymous-contribution and AI-assistance disclosures.
