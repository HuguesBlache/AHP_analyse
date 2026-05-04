# AHP figure bundle (GitHub)

This folder collects **runnable code**, the **AHP modules** used from `analyse_ahp.ipynb`, **CSV data**, and a copy of the **Google Sheet** notebook so you can reproduce the PDF figures listed below.

## Contents

| Item | Purpose |
|------|---------|
| `data/*.csv` | Survey exports (mainly `survey_42.csv` for mixture plots and expert charts). |
| `src/function_ahp_*_2.py` | Same files as in the parent repo (loaded with `%run` in the notebook). |
| `generate_mixture_figures.py` | Writes `B-AHP_*`, `C-AHP_*`, `W-AHP_*` as `_mixture.pdf` and `_word.pdf` (see `analyse_ahp.ipynb`, cells ~8, 13, 15). |
| `expert_plots_google_sheet.py` | Writes `expert_count.pdf` and `expert_scenario.pdf` (from `notebooks/AHP_analyse_google_sheet.ipynb`). |
| `notebooks/AHP_analyse_google_sheet.ipynb` | Copy of the original notebook. |
| `output/images/` | PDF output (created when you run the scripts). |

## Setup

```bash
cd figure_bundle_github
pip install -r requirements.txt
```

Plotly needs **Kaleido** for `fig.write_image`.

## Commands

```bash
python generate_mixture_figures.py
python expert_plots_google_sheet.py --skip-show
```

Mixture and word PDFs go to `output/images/` (override with `--out`).

## `value_weight_44.pdf`

That filename is **not** referenced anywhere in the repo as `write_image("value_weight_44.pdf")`. If you generated it locally (another notebook, manual export, or a name tied to `survey_4` / respondent count), add the script here or document the command so the bundle stays complete.

## `survey_6.csv`

`analyse_ahp.ipynb` sometimes calls `ahp_belief('survey_6.csv')`; that file is **not** in the current repo. To reproduce that branch, add your CSV under `data/` and point `--survey` or your derived notebook at it.

## Source mapping

- **Mixture + word plots**: `../analyse_ahp.ipynb` — imports + `%run function_ahp_*_2.py`, `plot_elbow_(...)` with `fig.write_image("%s_mixture.pdf"%(name))` and (uncommented in this bundle) `%s_word.pdf`.
- **Expert plots**: `../AHP_analyse_google_sheet.ipynb` — load `survey_42.csv`, `result.iloc[2:]`, “Plot expertise” blocks.

## Language (comments and docs)

Bundle entrypoints (`generate_mixture_figures.py`, `expert_plots_google_sheet.py`), this README, and `extracted_snippets/` are in **English**. The copied `src/function_ahp_*_2.py` files were partially translated (shared AHP normalization docstrings and several inline comments); deeper sections may still contain French from the original thesis code. Survey CSVs and `notebooks/AHP_analyse_google_sheet.ipynb` still contain **French questionnaire text** in cells and headers, which is expected data, not UI copy.

## Publish to GitHub

This directory is already a **git** repository with branch `main`, **MIT** `LICENSE`, and an initial commit.

1. On [github.com/new](https://github.com/new), create a **Public** repository. Do **not** add a README, `.gitignore`, or license (avoids merge conflicts).
2. Link the remote and push (replace the URL with yours):

```bash
cd figure_bundle_github
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git push -u origin main
```

If `origin` already exists, use `git remote set-url origin https://github.com/YOUR_USER/YOUR_REPO.git` instead.

Alternatively run `./scripts/link_github_remote.sh https://github.com/YOUR_USER/YOUR_REPO.git` and follow the printed instructions.

GitHub will show the **MIT** license automatically once `LICENSE` is on the default branch.
