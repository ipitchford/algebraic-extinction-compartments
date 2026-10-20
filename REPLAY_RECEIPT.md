# Finite exact replay

Executed 20 October 2026 using Python 3.14.7:

```sh
python3 -B test_verifier.py --output-dir NEW_DIRECTORY
```

The retained summary is `evidence/replay-20261020/summary.json`. It binds the
verifier and harness hashes, normal and optimized report hashes, the child
optimization flags, and the rejected controls.

Both positive runs passed all 24 cases m=2,...,25 and three phase checks.
All six negative runs failed with explicit ValueError:
wrong initial scale, a missing channel and an incorrect removed-state flux,
each in normal and optimized mode. None wrote a passing report.

No scientific universal claim is inferred from the finite range. General
proofs are in `paper.md`. Fresh-extraction and final-archive checks belong to
the separate release packaging record and must not be inferred from this
working-copy receipt.
