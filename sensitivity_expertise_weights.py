#!/usr/bin/env python3
"""
Sensitivity analysis for expertise weights alpha_k used in W-AHP and B-AHP.

Compares alternative alpha schemes on scenario confidence scores and reports
Spearman rank correlations and top/bottom scenario overlap vs. baseline.

Usage:
  python sensitivity_expertise_weights.py
  python sensitivity_expertise_weights.py --survey path/to/survey_42.csv
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent
DEFAULT_SURVEY = (
    ROOT / "figure_bundle_github" / "AHP_analyse" / "data" / "survey_42.csv"
)

ALPHA_PATTERN = re.compile(
    r"alpha=\{'No expertise':[0-9.]+,'Beginner Level':[0-9.]+,"
    r"'Intermediate Level':[0-9.]+,\s*'Advanced Level':[0-9.]+,'Expert Level':[0-9.]+\}"
)

LEVELS = [
    "No expertise",
    "Beginner Level",
    "Intermediate Level",
    "Advanced Level",
    "Expert Level",
]

SCHEMES: dict[str, dict[str, float]] = {
  # Values reported in the manuscript (Table 2)
    "baseline_manuscript": {
        "No expertise": 0.1,
        "Beginner Level": 0.3,
        "Intermediate Level": 0.5,
        "Advanced Level": 0.7,
        "Expert Level": 1.0,
    },
    # Values currently hard-coded in function_ahp_geometric_2.py / belief_2.py
    "baseline_code": {
        "No expertise": 0.1,
        "Beginner Level": 0.3,
        "Intermediate Level": 0.5,
        "Advanced Level": 0.8,
        "Expert Level": 1.0,
    },
    "uniform": {k: 1.0 for k in LEVELS},
    "steeper": {
        "No expertise": 0.05,
        "Beginner Level": 0.2,
        "Intermediate Level": 0.5,
        "Advanced Level": 0.8,
        "Expert Level": 1.0,
    },
    "mild": {
        "No expertise": 0.2,
        "Beginner Level": 0.4,
        "Intermediate Level": 0.6,
        "Advanced Level": 0.8,
        "Expert Level": 1.0,
    },
}


def alpha_assignment(alpha_map: dict[str, float]) -> str:
    return (
        "alpha={'No expertise':%s,'Beginner Level':%s,'Intermediate Level':%s,"
        "'Advanced Level':%s,'Expert Level':%s}"
        % tuple(alpha_map[k] for k in LEVELS)
    )


def load_ahp_with_alpha(py_file: Path, alpha_map: dict[str, float], fn_name: str):
    code = py_file.read_text()
    patched, n = ALPHA_PATTERN.subn(alpha_assignment(alpha_map), code)
    if n == 0:
        raise RuntimeError(f"Could not patch alpha weights in {py_file}")
    namespace: dict = {}
    exec(compile(patched, str(py_file), "exec"), namespace)
    return namespace[fn_name]


def overlap_extremes(a: np.ndarray, b: np.ndarray, k: int = 10) -> float:
    a = np.asarray(a)
    b = np.asarray(b)
    low_a = set(np.argsort(a)[:k])
    high_a = set(np.argsort(a)[-k:])
    low_b = set(np.argsort(b)[:k])
    high_b = set(np.argsort(b)[-k:])
    return (len(low_a & low_b) + len(high_a & high_b)) / (2 * k)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--survey", type=Path, default=DEFAULT_SURVEY)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "sensitivity_expertise_weights_results.csv",
    )
    args = parser.parse_args()

    survey = str(args.survey)
    methods = {
        "W-AHP": (
            ROOT / "function_ahp_geometric_2.py",
            "ahp_weight",
        ),
        "B-AHP": (
            ROOT / "function_ahp_belief_2.py",
            "ahp_belief",
        ),
    }

    scores: dict[tuple[str, str], np.ndarray] = {}
    for method, (py_file, fn_name) in methods.items():
        for scheme, alpha_map in SCHEMES.items():
            runner = load_ahp_with_alpha(py_file, alpha_map, fn_name)
            result = runner(survey)[1]
            scores[(method, scheme)] = np.asarray(result, dtype=float)

    baseline_key = "baseline_manuscript"
    rows = []
    for method in methods:
        base = scores[(method, baseline_key)]
        for scheme in SCHEMES:
            alt = scores[(method, scheme)]
            rho = spearmanr(base, alt).statistic
            rows.append(
                {
                    "method": method,
                    "scheme": scheme,
                    "spearman_rho_vs_baseline": round(float(rho), 4),
                    "top10_bottom10_overlap": round(overlap_extremes(base, alt, 10), 3),
                    "mean_score": round(float(np.mean(alt)), 4),
                    "std_score": round(float(np.std(alt)), 4),
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(args.output, index=False)

    print(f"Survey: {survey}")
    print(f"Saved: {args.output}\n")
    print(df.to_string(index=False))
    print(
        "\nInterpretation: Spearman rho close to 1 and high overlap indicate stable "
        "scenario rankings under alternative alpha_k schemes."
    )


if __name__ == "__main__":
    main()
