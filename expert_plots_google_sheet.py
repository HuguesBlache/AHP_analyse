#!/usr/bin/env python3
"""
Taken from AHP_analyse_google_sheet.ipynb: expert_count and expert_scenario charts.

Dependencies: pandas, plotly, kaleido.

Usage:
  python expert_plots_google_sheet.py
  python expert_plots_google_sheet.py --survey data/survey_42.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
IMG = ROOT / "output" / "images"


def plot_expert_count(result: pd.DataFrame, out_dir: Path, *, show: bool = True) -> None:
    # Expertise level pie chart
    expertise_columns = result.columns[1]
    fig = go.Figure()
    colors = px.colors.qualitative.D3
    fig.add_trace(
        go.Pie(
            labels=list(result[expertise_columns].value_counts().index),
            values=list(result[expertise_columns].value_counts()),
        )
    )
    fig.update_traces(
        textfont_size=20,
        marker=dict(colors=colors, line=dict(color="#000000", width=1)),
    )
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="middle",
            y=-0.20,
            x=0.19,
            title_font_family="Times New Roman",
        )
    )
    fig.update_layout(width=600, height=600)
    if show:
        fig.show()
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.write_image(str(out_dir / "expert_count.pdf"))


def plot_expert_scenario(result: pd.DataFrame, out_dir: Path, *, show: bool = True) -> None:
    # Stacked bars: expertise level × scenario branch
    expertise_columns = result.columns[2]
    pivot_table = result.pivot_table(
        index=result.columns[1], columns=expertise_columns, aggfunc="size", fill_value=0
    )
    desired_order = [
        "Intermediate Level",
        "Expert Level",
        "Advanced Level",
        "Beginner Level",
        "No expertise",
    ]
    pivot_table = pivot_table.reindex(desired_order)
    table_by_expert = []
    for i in range(0, len(pivot_table)):
        table_by_expert.append(list(pivot_table.iloc[i]))

    colors = px.colors.qualitative.D3
    fig = go.Figure()
    for i in range(0, len(table_by_expert)):
        fig.add_trace(
            go.Bar(
                x=pivot_table.columns,
                y=table_by_expert[i],
                name=desired_order[i],
                marker_color=colors[i],
            )
        )
    fig.update_layout(barmode="stack")
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="middle",
            y=-0.20,
            xanchor="center",
            x=0.5,
            title_font_family="Times New Roman",
        )
    )
    fig.update_xaxes(title_text="<b>Scenario</b>")
    fig.update_xaxes(title_text="<b>Count</b>")
    fig.update_traces(
        textfont_size=30, marker=dict(line=dict(color="#000000", width=1))
    )
    fig.update_layout(width=800, height=800)
    fig.update_layout(plot_bgcolor="rgb(245, 245, 245)")
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.write_image(str(out_dir / "expert_scenario.pdf"))
    if show:
        fig.show()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--survey",
        type=Path,
        default=DATA / "survey_42.csv",
        help="Form export CSV (same as in the notebook).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=IMG,
        help="Output directory for PDF files.",
    )
    parser.add_argument(
        "--skip-show",
        action="store_true",
        help="Do not call fig.show() (useful in CI or without a display backend).",
    )
    args = parser.parse_args()
    survey_path = args.survey if args.survey.is_absolute() else ROOT / args.survey
    result = pd.read_csv(survey_path)
    result = result.iloc[2:]

    show = not args.skip_show
    plot_expert_count(result, args.out, show=show)
    plot_expert_scenario(result, args.out, show=show)

    print("PDFs written to:", args.out.resolve())


if __name__ == "__main__":
    main()
