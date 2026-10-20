# Revision notes: version 1.1

The supplied version already contained the completed corrections to its earlier
review: accurate source assumptions, corrected references, close stability
comparisons, finite-time positivity, compartment-count clarification and figure
qualification. Those corrections are retained.

This revision adds:

- An introductory explanation of why an integrable tail need not justify an
  exponential stopping estimate, and a short guide through the proof.
- Corollary 8: the aggregate vanishing population has logarithmic rate equal to
  the transverse spectral bound. The full trajectory has that rate when the
  bound is negative. A complete proof is included, with a separate AI proof check.
- Explicit verifier guards that remain active in optimized Python, and a replay
  harness that rejects three deliberate corruptions in both execution modes.
- Availability, ethics, anonymous contribution, funding/conflict and AI-assistance
  declarations.

Theorems 1-7 are unchanged. The new corollary is a direct consequence of the
comparison method; it is not presented as a new general theory. The finite checks
do not establish the unbounded analytic results or historical novelty. No external
human peer review or proof-assistant verification is claimed.

Near-critical bottleneck calculations were considered but not added as a claimed
advance: their scalar mechanism is standard. General dimension-dependent tail
classification and robustness of higher-multiplicity constructions remain open.
