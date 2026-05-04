#!/usr/bin/env python3
"""
Generate B-AHP_mixture.pdf, B-AHP_word.pdf, C-AHP_mixture.pdf, C-AHP_word.pdf,
W-AHP_mixture.pdf, W-AHP_word.pdf using the same logic as analyse_ahp.ipynb
(cells ~8, 13, 15: ahp_belief / ahp_weight / ahp_classique + plot_elbow_).

Dependencies: pandas, numpy, scikit-learn, plotly, kaleido (for fig.write_image).

Usage (from this directory):
  python generate_mixture_figures.py
  python generate_mixture_figures.py --survey data/survey_42.csv
"""

from __future__ import annotations

import argparse
import math
import runpy
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.mixture import GaussianMixture

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
DATA = ROOT / "data"
OUTPUT = ROOT / "output"
IMG = OUTPUT / "images"


def load_survey_functions():
    belief_ns = runpy.run_path(str(SRC / "function_ahp_belief_2.py"))
    geo_ns = runpy.run_path(str(SRC / "function_ahp_geometric_2.py"))
    cls_ns = runpy.run_path(str(SRC / "function_ahp_classique_2.py"))
    return belief_ns["ahp_belief"], geo_ns["ahp_weight"], cls_ns["ahp_classique"]


def plot_elbow_mixture_word(
    scores: list[float],
    name: str,
    color,
    n_components: int,
    resultat_word: list,
    key_index: list,
    out_dir: Path,
    export_word: bool = True,
) -> None:
    """Histogram + GMM mixture curves, then stacked bars of scenario-attribute tokens (word)."""
    data = scores
    data_array = np.array(data).reshape(-1, 1)
    gmm = GaussianMixture(n_components=n_components)
    gmm.fit(data_array)

    fig = go.Figure()
    bins = [i / 1000 for i in range(0, 1000)]
    data_sumo_ttc = np.histogram(data, bins=bins)[0]
    fig.add_trace(
        go.Scatter(
            y=data_sumo_ttc / sum(data_sumo_ttc),
            x=bins,
            name="$\\Omega^{%s}_{\\mathcal{S}_f}$" % name,
            marker_color=color,
        )
    )
    for i in range(n_components):
        x = np.linspace(0, 1, 1001)
        mu = gmm.means_[i][0]
        sig = math.sqrt(gmm.covariances_[i][0][0])
        test_y = np.exp(-((x - mu) ** 2) / (2 * sig**2)) / (np.sqrt(2 * np.pi))
        fig.add_trace(
            go.Scatter(
                y=gmm.weights_[i] * test_y / sum(test_y),
                x=x,
                name="mixture %s" % (i + 1),
                marker_color=px.colors.qualitative.T10[i + 2],
            )
        )

    labels = gmm.predict(data_array)
    fig.update_xaxes(title_text="Score")
    fig.update_yaxes(
        title_text=r"$\Large \textrm{Frequency  of } \,\,\, \Omega_{\mathcal{S}_f}$"
    )
    fig.update_traces(
        textfont_size=25, marker=dict(line=dict(color="#000000", width=1))
    )
    fig.update_layout(width=820, height=500)
    fig.update_layout(
        font=dict(
            family="Times New Romans",
            size=18,
            color=px.colors.qualitative.Dark24[-2],
        )
    )
    fig.update_yaxes(
        showgrid=True,
        showline=True,
        gridcolor="rgb(200,200,200)",
        gridwidth=2,
        zerolinecolor="#969696",
        zerolinewidth=2,
        linecolor="rgb(253, 253, 253)",
        linewidth=2,
        color="rgb(55,126,184)",
    )
    fig.update_xaxes(
        showgrid=True,
        showline=True,
        gridcolor="rgb(200,200,200)",
        gridwidth=2,
        zerolinecolor="#969696",
        zerolinewidth=2,
        linecolor="rgb(253, 253, 253)",
        linewidth=2,
    )
    fig.update_layout(plot_bgcolor="rgb(253, 253, 253)", title_x=0.5)
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="middle",
            y=-0.35,
            xanchor="center",
            x=0.5,
            title_font_family="Times New Roman",
        )
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.write_image(str(out_dir / ("%s_mixture.pdf" % name)))

    fig = go.Figure()
    pandas_with_label = pd.DataFrame(
        data={"ahp_weight": data, "lables": labels, "word": resultat_word}
    )
    data_2 = pandas_with_label.groupby("lables")["word"].apply(list)
    word_freq_df_all: list[pd.DataFrame] = []
    for word_list_data in data_2:
        word_counter: Counter = Counter()
        for words_list in word_list_data:
            for word in words_list:
                word_counter[word] += 1
        word_freq_df = pd.DataFrame.from_dict(
            word_counter, orient="index", columns=["Frequency"]
        )
        word_freq_df = word_freq_df.sort_values(by="Frequency", ascending=False)
        word_freq_df_all.append(word_freq_df)

    word_dict: dict[int, list] = {}
    for i in range(0, n_components):
        word_dict[i] = []
        for word in key_index:
            if word in list(word_freq_df_all[i].index):
                word_dict[i].append(word_freq_df_all[i].loc[word].iloc[0])
            else:
                word_dict[i].append(0)
        word_dict[i] = np.array(word_dict[i])
    for i in range(0, n_components):
        fig.add_trace(
            go.Bar(
                name="mixture %s" % (i + 1),
                y=word_dict[i] / (sum(word_dict.values())),
                x=key_index,
                marker_color=px.colors.qualitative.T10[i + 2],
            )
        )

    fig.update_layout(barmode="stack")
    fig.update_yaxes(title_text="Proportion")
    fig.update_layout(
        font=dict(
            family="Times New Romans",
            size=18,
            color=px.colors.qualitative.Dark24[-2],
        )
    )
    fig.update_yaxes(
        showgrid=True,
        showline=True,
        gridcolor="rgb(200,200,200)",
        gridwidth=2,
        zerolinecolor="#969696",
        zerolinewidth=2,
        linecolor="rgb(253, 253, 253)",
        linewidth=2,
        color="rgb(55,126,184)",
    )
    fig.update_xaxes(
        showgrid=True,
        showline=True,
        gridcolor="rgb(200,200,200)",
        gridwidth=2,
        zerolinecolor="#969696",
        zerolinewidth=2,
        linecolor="rgb(253, 253, 253)",
        linewidth=2,
        title_text="Number of distribution",
    )
    fig.update_layout(plot_bgcolor="rgb(253, 253, 253)", title_x=0.5)
    fig.update_layout(width=1000, height=550)
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="middle",
            y=1.25,
            xanchor="center",
            x=0.5,
            title_font_family="Times New Roman",
        )
    )
    if export_word:
        fig.write_image(str(out_dir / ("%s_word.pdf" % name)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--survey",
        type=Path,
        default=DATA / "survey_42.csv",
        help="Survey CSV (absolute path or path relative to figure_bundle_github/).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=IMG,
        help="Output directory for PDF files.",
    )
    args = parser.parse_args()
    survey_path = args.survey if args.survey.is_absolute() else ROOT / args.survey
    if not survey_path.is_file():
        raise SystemExit("File not found: %s" % survey_path)

    ahp_belief, ahp_weight, ahp_classique = load_survey_functions()
    survey_s = str(survey_path.resolve())

    resultat_word, resultat_final_normalised, _, _, index = ahp_belief(survey_s)
    _, resultat_final_normalised_2, _, _ = ahp_weight(survey_s)
    _, resultat_final_normalised_3, _, _ = ahp_classique(survey_s)
    key_index = [x for xs in index for x in xs]

    # Order and n_components as in analyse_ahp.ipynb (cell 15)
    plot_elbow_mixture_word(
        resultat_final_normalised_3,
        "C-AHP",
        px.colors.qualitative.Set1[2],
        5,
        resultat_word,
        key_index,
        args.out,
    )
    plot_elbow_mixture_word(
        resultat_final_normalised,
        "B-AHP",
        px.colors.qualitative.Set1[1],
        3,
        resultat_word,
        key_index,
        args.out,
    )
    plot_elbow_mixture_word(
        resultat_final_normalised_2,
        "W-AHP",
        px.colors.qualitative.Set1[0],
        4,
        resultat_word,
        key_index,
        args.out,
    )
    print("PDFs written to:", args.out.resolve())


if __name__ == "__main__":
    main()
