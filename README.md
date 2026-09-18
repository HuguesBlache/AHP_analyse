# Replication package — JICV manuscript

**Title:** Assessing Microscopic Traffic Simulation Confidence Level Through Expert-Weighted AHP and Belief Theory: An Application to CAV Testing  
**Authors:** Hugues Blache et al.  
**Journal:** *Journal of Intelligent and Connected Vehicles* (JICV)  
**Manuscript ID:** JICV-2026-0031  

This package contains the **data**, **source code**, and **scripts** needed to reproduce the main AHP / W-AHP / B-AHP results and figures of the article.

**Primary distribution (now):** GitHub — https://github.com/HuguesBlache/AHP_analyse  
**ETS-Data:** the same package will be deposited before final publication; replace `XXXX` below once the DOI is assigned.

**ETS-Data DOI (to be filled after approval):** `https://doi.org/XXXX`  
**Associated article DOI (after publication):** `https://doi.org/10.26599/JICV.XXXX`

---

## Package structure

```text
AHP_analyse/
├── README.md                          # this file
├── LICENSE                            # MIT
├── requirements.txt
├── data/
│   ├── README.md                      # data dictionary
│   └── survey_42.csv                  # primary analysis file (n = 42)
│   └── survey*.csv                    # intermediate survey exports
├── src/
│   ├── function_ahp_classique_2.py    # classical AHP (C-AHP)
│   ├── function_ahp_geometric_2.py    # expertise-weighted AHP (W-AHP)
│   └── function_ahp_belief_2.py       # belief-theory AHP (B-AHP)
├── scripts/
│   ├── generate_mixture_figures.py    # GMM mixture + word figures
│   ├── expert_plots_google_sheet.py   # expertise / branch charts
│   └── sensitivity_expertise_weights.py
└── output/
    ├── images/                        # generated PDFs/PNGs
    └── results/                       # CSV tables (e.g. sensitivity)
```

---

## Environment

- Python ≥ 3.9 (tested with 3.10+)
- OS: macOS / Linux / Windows

```bash
cd AHP_analyse
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Reproduce main results

All commands below are run from the **repository root** (`AHP_analyse/`).

### 1. Expertise and branch distributions (Figure 9-type plots)

```bash
python scripts/expert_plots_google_sheet.py --skip-show
```

Outputs: `output/images/expert_count.pdf`, `output/images/expert_scenario.pdf`

### 2. Scenario score mixtures (B/C/W-AHP)

```bash
python scripts/generate_mixture_figures.py --survey data/survey_42.csv
```

Outputs: `output/images/{B,C,W}-AHP_mixture.pdf` and `{B,C,W}-AHP_word.pdf`

### 3. Sensitivity of expertise weights αₖ

```bash
python scripts/sensitivity_expertise_weights.py --survey data/survey_42.csv
```

Output: `output/results/sensitivity_expertise_weights_results.csv`

---

## Primary data file

| File | Role |
|------|------|
| `data/survey_42.csv` | Anonymous expert-survey responses used in the manuscript (*n* = 42 after removing test rows). |

See `data/README.md` for column description and ethics notes. Responses are anonymous; no personal identifiers are included.

---

## Citation

Please cite the article once published, and this replication package via its ETS-Data DOI.

```
Blache, H., et al. (2026). Replication package for: Assessing Microscopic Traffic
Simulation Confidence Level Through Expert-Weighted AHP and Belief Theory.
ETS-Data. https://doi.org/XXXX
```

---

## License

MIT License — see `LICENSE`.
