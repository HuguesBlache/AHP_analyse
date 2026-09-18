# Replication Explanatory File for Journal-Associated Data

*(Prepared for ETS-Data / JICV Data and Code Policy)*

---

## Title

Expert-weighted AHP replication package for simulation confidence

*(Alternative long title aligned with the article: Replication package for assessing microscopic traffic simulation confidence via expert-weighted AHP and belief theory)*

---

## Author(s)

| Name | Role | Affiliation |
|------|------|-------------|
| Hugues Blache | Corresponding author | University of New South Wales (UNSW), Research Centre for Integrated Transport Innovation (rCITI), Sydney, Australia |
| Pierre-Antoine Laharotte | Co-author | Université Gustave Eiffel / ENTPE, Emob-Lab, France |
| Nour-Eddin El Faouzi | Co-author | Université Gustave Eiffel / ENTPE, Emob-Lab, France |

---

## Keyword(s)

Scenario-based testing; Analytic Hierarchy Process; simulation confidence; microscopic traffic simulation; expert survey; belief theory

---

## Journal Name and Manuscript ID

- **Journal name:** Journal of Intelligent and Connected Vehicles (JICV)  
- **Manuscript ID:** JICV-2026-0031  
- **Manuscript title:** Assessing Microscopic Traffic Simulation Confidence Level Through Expert-Weighted AHP and Belief Theory: An Application to CAV Testing  

---

## Data description

### What is provided

Complete **anonymous** expert-survey data used in the article are included in this package under `data/`.

| File | Description |
|------|-------------|
| `data/survey_42.csv` | **Primary analysis file** used in the manuscript (*n* = 42 respondents after removing test rows). Google Forms export containing self-reported expertise, questionnaire-branch choice, Likert confidence ratings, and pairwise comparisons. |
| `data/survey.csv`, `survey_2.csv`, …, `survey_5.csv` | Intermediate survey exports retained for traceability; **not** required to reproduce the manuscript results. |
| `data/README.md` | Data dictionary (column roles, branch sample sizes, privacy notes). |

### Data origin and format

- **Source:** Online expert questionnaire (Google Forms) administered to researchers and practitioners in microscopic traffic simulation.  
- **Collection period:** January 2024 – September 2024.  
- **Format:** UTF-8 CSV.  
- **Language in headers:** French/English questionnaire wording as collected (data content; documentation is in English).

### Completeness

This is the **complete analysis dataset** underlying the manuscript results (not licensed third-party traffic data). No Personal Health Information or other sensitive identifiers are included. Responses are anonymous (no names, emails, or institutional IDs).

### Branch-level sample sizes (*n* = 42)

Intersection 11; Type of user 9; Exit 7; Specific Lane 6; Driver’s Vision 4; Sunny 3; Curved road 2.

These data are sufficient to regenerate the key AHP weights, scenario scores, mixture figures, and sensitivity tables reported in the article.

---

## Code description

### Computer environment

- **Language:** Python ≥ 3.9 (recommended 3.10+)  
- **OS:** macOS, Linux, or Windows  
- **Dependencies:** see `requirements.txt`  
  - pandas ≥ 1.5  
  - numpy ≥ 1.23  
  - scipy ≥ 1.10  
  - scikit-learn ≥ 1.2  
  - plotly ≥ 5.18  
  - kaleido ≥ 0.2.1 (PDF export)  
  - matplotlib ≥ 3.7  

### Setup

```bash
cd AHP_analyse
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Core source modules (`src/`)

| File | Method in manuscript |
|------|----------------------|
| `src/function_ahp_classique_2.py` | Classical AHP (C-AHP) |
| `src/function_ahp_geometric_2.py` | Expertise-weighted AHP (W-AHP) |
| `src/function_ahp_belief_2.py` | Belief-theory AHP (B-AHP) |

### Replication scripts (`scripts/`)

| Script | Purpose |
|--------|---------|
| `scripts/expert_plots_google_sheet.py` | Expertise distribution and branch-assignment charts |
| `scripts/generate_mixture_figures.py` | GMM mixture and “word” figures for B-/C-/W-AHP scores |
| `scripts/sensitivity_expertise_weights.py` | Sensitivity of scenario rankings to expertise weights αₖ |

All scripts are **passcode-free** and have no access restrictions.

---

## Simulation software description

**Not applicable.**  
This study does not distribute traffic-simulator project files (e.g., SUMO / VISSIM / CARLA networks). Confidence scores are derived from **expert judgments** about microscopic simulation in general, at the scenario-attribute level. Platform-specific simulation validation is outside the scope of the manuscript.

---

## Experiment design description

### Survey / questionnaire design

1. **Step 1 — Expertise and branch selection:** Respondents self-report their expertise level with microscopic traffic simulation tools and select one scenario branch (ontology subset) they feel competent to evaluate.  
2. **Step 2 — Attribute evaluation:** Within the selected branch, respondents assign confidence ratings (β) and perform pairwise comparisons of attributes (AHP judgments).  
3. **Step 3 — Higher-level comparisons:** Additional cross-attribute / scenario comparisons as described in the manuscript.

Seven branches were used: Driver’s Vision, Sunny, Type of user, Intersection, Specific Lane, Exit, Curved road.

### Experiment setups

- Online form (no laboratory physical equipment).  
- No interventional human experiment beyond voluntary survey participation.  
- Data released without personal identifiers.

---

## Others — Steps to replicate the main results

Run all commands from the package root (`AHP_analyse/`):

```bash
# 1) Expertise / branch figures
python scripts/expert_plots_google_sheet.py --skip-show

# 2) Mixture and word figures (B-/C-/W-AHP)
python scripts/generate_mixture_figures.py --survey data/survey_42.csv

# 3) Expertise-weight sensitivity table
python scripts/sensitivity_expertise_weights.py --survey data/survey_42.csv
```

| Output location | Content |
|-----------------|---------|
| `output/images/` | PDF figures |
| `output/results/sensitivity_expertise_weights_results.csv` | Sensitivity metrics (Spearman ρ, top/bottom-10 overlap) |

Additional guidance is provided in `README.md`.

---

## Research facility

University of New South Wales (UNSW), Research Centre for Integrated Transport Innovation (rCITI), Sydney, Australia  
*(Co-author affiliations: Université Gustave Eiffel / ENTPE, Emob-Lab, France)*

---

## Methods

Expert judgments are aggregated with three AHP strategies (classical, expertise-weighted, Dempster–Shafer belief discounting). Scenario confidence scores are obtained by combining attribute-level weights over an ontology-based scenario representation. Gaussian mixture models are used to describe score distributions. Full methodological details are given in the manuscript.

---

## Usage notes

- Use `data/survey_42.csv` for manuscript replication.  
- Analysis scripts skip form metadata rows where required (same pipeline as the article).  
- Empty or non-applicable cells in the Forms export may appear blank; treat them as missing (`n/a`) for unused branch columns (respondents only complete their selected branch).  
- Do not attempt to re-identify respondents.  
- License of the package code: **MIT** (`LICENSE`).  

---

## Related works

- Associated manuscript: *Assessing Microscopic Traffic Simulation Confidence Level Through Expert-Weighted AHP and Belief Theory: An Application to CAV Testing*, JICV-2026-0031 (article DOI to be added after publication).  
- GitHub mirror (optional): https://github.com/HuguesBlache/AHP_analyse  
- Related prior work: Blache et al. (2025), *Journal of Intelligent Transportation Systems* (scenario ontology / description framework).

---

## Package checklist (ETS-Data upload)

- [x] Passcode-free files  
- [x] English documentation (this file + README)  
- [x] No PHI / sensitive personal data  
- [x] Data + code + scripts + this Replication Explanatory File  
- [ ] Packaged as a **single ZIP** (max 3 GB) for ETS-Data upload  

Suggested ZIP name: `JICV-2026-0031_AHP_analyse_replication.zip`
