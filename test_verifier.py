#!/usr/bin/env python3
"""Replay exact checks normally and optimized; require corruptions to fail.

Tests verification sensitivity, not the unbounded analytic theorem.
Uses only Python's standard library. All reports go to a new output directory.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    source_path = Path(__file__).with_name("verify.py")
    source = source_path.read_text()
    mutations = {
        "incorrect_initial_scale": ("kap = Q(1, 2*3**m)", "kap = Q(1, 3**m)"),
        "missing_channel": ("for source, catalyst, destination, rate in channels:",
                            "for source, catalyst, destination, rate in channels[1:]:"),
        "incorrect_removed_flux": ("scale(mul(Y, I), 4)", "scale(mul(Y, I), 3)"),
    }
    results = []
    with tempfile.TemporaryDirectory(prefix="extinction-verifier-") as temp:
        for optimized in [False, True]:
            mode = "optimized" if optimized else "normal"
            command = [sys.executable, "-B"] + (["-O"] if optimized else [])
            receipt = args.output_dir / f"{mode}.json"
            run = subprocess.run(command + [str(source_path), "--output", str(receipt)],
                                 capture_output=True, text=True, timeout=120)
            if run.returncode:
                raise RuntimeError(run.stderr)
            report = json.loads(receipt.read_text())
            if report["python_optimization"] != int(optimized):
                raise RuntimeError("child optimization mode was not applied")
            if report["status"] != "PASS" or report["instances_checked"] != 24:
                raise RuntimeError("incomplete positive-control evidence")
            results.append({"mode": mode, "case": "unaltered", "returncode": run.returncode,
                            "receipt": receipt.name,
                            "receipt_sha256": hashlib.sha256(receipt.read_bytes()).hexdigest()})
            for name, (old, new) in mutations.items():
                if source.count(old) != 1:
                    raise RuntimeError(f"mutation target not unique: {name}")
                mutated = Path(temp) / f"{name}.py"
                mutated.write_text(source.replace(old, new))
                failed_receipt = Path(temp) / f"{name}-{mode}.json"
                run = subprocess.run(command + [str(mutated), "--output", str(failed_receipt)],
                                     capture_output=True, text=True, timeout=120)
                if run.returncode == 0 or "ValueError" not in run.stderr or failed_receipt.exists():
                    raise RuntimeError(f"negative control did not reject corruption: {name}, {mode}")
                results.append({"mode": mode, "case": name, "returncode": run.returncode,
                                "rejected_by": run.stderr.strip().splitlines()[-1]})
    report = {
        "status": "PASS", "positive_runs": 2, "negative_controls_rejected": 6,
        "verifier_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "harness_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Finite exact identities and checker sensitivity, not formal verification.",
        "results": results,
    }
    (args.output_dir / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
