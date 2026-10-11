"""Student Performance & Study Habits Analysis.

Downloads the UCI Student Performance dataset, explores grades and study habits,
prints summary tables, and saves charts in ./outputs.
"""

from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid")


def load_subject_data():
    """Download and load the Mathematics and Portuguese CSV files."""
    url = "https://archive.ics.uci.edu/static/public/320/student.zip"
    print("Downloading dataset from the UCI Machine Learning Repository...")
    with urlopen(url, timeout=30) as response:
        archive_bytes = response.read()

    data = {}
    with ZipFile(BytesIO(archive_bytes)) as archive:
        for subject, filename in [
            ("Mathematics", "student-mat.csv"),
            ("Portuguese", "student-por.csv"),
        ]:
            with archive.open(filename) as file:
                data[subject] = pd.read_csv(file, sep=";")
    return data


def summarize(data):
    """Print and save headline metrics for each subject."""
    rows = []
    for subject, df in data.items():
        rows.append({
            "Subject": subject,
            "Students": len(df),
            "Average final grade": round(df["G3"].mean(), 2),
            "Median final grade": round(df["G3"].median(), 2),
            "Pass rate (%)": round((df["G3"] >= 10).mean() * 100, 1),
            "Average absences": round(df["absences"].mean(), 2),
        })
    summary = pd.DataFrame(rows)
    print("\n=== OVERALL SUMMARY ===")
    print(summary.to_string(index=False))
    summary.to_csv(OUTPUT_DIR / "summary_metrics.csv", index=False)


def make_charts(data):
    """Create charts that answer the project's main questions."""
    pieces = []
    for subject, df in data.items():
        piece = df[["studytime", "G3", "absences"]].copy()
        piece["Subject"] = subject
        pieces.append(piece)
    combined = pd.concat(pieces, ignore_index=True)

    study_labels = {
        1: "<2 hours",
        2: "2–5 hours",
        3: "5–10 hours",
        4: ">10 hours",
    }
    combined["Study time"] = combined["studytime"].map(study_labels)

    plt.figure(figsize=(9, 5))
    sns.barplot(
        data=combined, x="Study time", y="G3", hue="Subject",
        errorbar=None, order=["<2 hours", "2–5 hours", "5–10 hours", ">10 hours"],
    )
    plt.title("Average Final Grade by Weekly Study-Time Category")
    plt.xlabel("Weekly study time (category)")
    plt.ylabel("Average final grade (0–20)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "study_time_vs_grade.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 5))
    sns.scatterplot(data=combined, x="absences", y="G3", hue="Subject", alpha=0.6)
    plt.title("School Absences and Final Grades")
    plt.xlabel("Number of absences")
    plt.ylabel("Final grade (0–20)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "absences_vs_grade.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 5))
    sns.histplot(
        data=combined, x="G3", hue="Subject", bins=20,
        element="step", stat="density", common_norm=False,
    )
    plt.title("Distribution of Final Grades by Subject")
    plt.xlabel("Final grade (0–20)")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "grade_distribution.png", dpi=160)
    plt.close()

    for subject, df in data.items():
        columns = ["studytime", "absences", "failures", "G1", "G2", "G3"]
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            df[columns].corr(numeric_only=True), annot=True, fmt=".2f",
            cmap="vlag", center=0, vmin=-1, vmax=1,
        )
        plt.title(f"Correlation Heatmap — {subject}")
        plt.tight_layout()
        safe_subject = subject.lower().replace(" ", "_")
        plt.savefig(OUTPUT_DIR / f"correlation_{safe_subject}.png", dpi=160)
        plt.close()

    print(f"\nCharts and summary saved in: {OUTPUT_DIR.resolve()}")


def print_observations(data):
    """Print a few data-driven observations without implying causation."""
    print("\n=== QUICK OBSERVATIONS ===")
    for subject, df in data.items():
        print(f"\n{subject}:")
        print(f"- Study-time / final-grade correlation: {df['studytime'].corr(df['G3']):.2f}")
        print(f"- Absences / final-grade correlation: {df['absences'].corr(df['G3']):.2f}")
        print("- Average final grade by study-time category:")
        for category, grade in df.groupby("studytime")["G3"].mean().items():
            print(f"  Category {category}: {grade:.2f}/20")
    print("\nInterpretation: these are associations, not proof of cause and effect.")


def main():
    data = load_subject_data()
    summarize(data)
    make_charts(data)
    print_observations(data)


if __name__ == "__main__":
    main()
