"""Student Performance & Study Habits Analysis.

Downloads the UCI Student Performance dataset, explores grades and study habits,
prints useful summary tables, and saves charts to ./outputs.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from ucimlrepo import fetch_ucirepo

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid", palette="deep")


def load_subject_data():
    """Return Mathematics and Portuguese data with the final grade included."""
    dataset = fetch_ucirepo(id=320)
    features = dataset.data.features.copy()
    targets = dataset.data.targets.copy()

    # UCI's target is G3 (final grade); features include G1 and G2.
    combined = pd.concat([features, targets], axis=1)
    if "G3" not in combined.columns:
        raise ValueError("Expected final-grade column G3 was not found.")

    # UCI supplies separate subject datasets; fetch the original CSV files from
    # the package's feature/target interface only gives one dataset, so use the
    # canonical CSV downloads when available for subject-level comparison.
    import urllib.request

    base = "https://archive.ics.uci.edu/static/public/320/"
    zip_path = OUTPUT_DIR / "student.zip"
    try:
        urllib.request.urlretrieve(base + "student.zip", zip_path)
        import zipfile

        with zipfile.ZipFile(zip_path) as zf:
            mat_name = next(n for n in zf.namelist() if n.endswith("student-mat.csv"))
            por_name = next(n for n in zf.namelist() if n.endswith("student-por.csv"))
            import io

            math_df = pd.read_csv(io.BytesIO(zf.read(mat_name)), sep=";")
            por_df = pd.read_csv(io.BytesIO(zf.read(por_name)), sep=";")
        zip_path.unlink(missing_ok=True)
        return {"Mathematics": math_df, "Portuguese": por_df}
    except Exception as exc:
        print(f"Could not retrieve both subject CSVs ({exc}). Using UCI API data for a combined overview.")
        return {"Combined UCI sample": combined}


def summarize(data):
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
    return summary


def make_charts(data):
    # 1. Average final grade by study-time category
    all_subjects = []
    for subject, df in data.items():
        temp = df[["studytime", "G3", "absences"]].copy()
        temp["Subject"] = subject
        all_subjects.append(temp)
    combined = pd.concat(all_subjects, ignore_index=True)

    study_labels = {
        1: "<2 hours",
        2: "2–5 hours",
        3: "5–10 hours",
        4: ">10 hours",
    }
    combined["Study time"] = combined["studytime"].map(study_labels)

    plt.figure(figsize=(9, 5))
    sns.barplot(data=combined, x="Study time", y="G3", hue="Subject", errorbar=None)
    plt.title("Average Final Grade by Weekly Study-Time Category")
    plt.xlabel("Weekly study time (category)")
    plt.ylabel("Average final grade (0–20)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "study_time_vs_grade.png", dpi=160)
    plt.close()

    # 2. Absences vs final grade
    plt.figure(figsize=(9, 5))
    sns.scatterplot(data=combined, x="absences", y="G3", hue="Subject", alpha=0.65)
    sns.regplot(data=combined, x="absences", y="G3", scatter=False, color="black")
    plt.title("School Absences and Final Grades")
    plt.xlabel("Number of absences")
    plt.ylabel("Final grade (0–20)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "absences_vs_grade.png", dpi=160)
    plt.close()

    # 3. Final grade distribution by subject
    plt.figure(figsize=(9, 5))
    sns.histplot(data=combined, x="G3", hue="Subject", bins=20, element="step",
                 stat="density", common_norm=False, kde=True)
    plt.title("Distribution of Final Grades by Subject")
    plt.xlabel("Final grade (0–20)")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "grade_distribution.png", dpi=160)
    plt.close()

    # 4. Correlations for useful numeric columns, per subject
    for subject, df in data.items():
        cols = [c for c in ["studytime", "absences", "failures", "G1", "G2", "G3"] if c in df.columns]
        plt.figure(figsize=(8, 6))
        sns.heatmap(df[cols].corr(numeric_only=True), annot=True, fmt=".2f",
                    cmap="vlag", center=0, vmin=-1, vmax=1)
        plt.title(f"Correlation Heatmap — {subject}")
        plt.tight_layout()
        safe_name = subject.lower().replace(" ", "_")
        plt.savefig(OUTPUT_DIR / f"correlation_{safe_name}.png", dpi=160)
        plt.close()

    print(f"\nCharts and summary saved to: {OUTPUT_DIR.resolve()}")


def print_interpretation(data):
    print("\n=== QUICK OBSERVATIONS ===")
    for subject, df in data.items():
        study_means = df.groupby("studytime", observed=True)["G3"].mean()
        corr_absences = df["absences"].corr(df["G3"])
        corr_study = df["studytime"].corr(df["G3"])
        print(f"\n{subject}:")
        print(f"- Correlation of study-time category with final grade: {corr_study:.2f}")
        print(f"- Correlation of absences with final grade: {corr_absences:.2f}")
        print("- Average final grade by study-time category:")
        for category, grade in study_means.items():
            print(f"  Category {category}: {grade:.2f}/20")
    print("\nRemember: correlations describe associations; they do not establish cause and effect.")


def main():
    print("Loading UCI Student Performance data...")
    data = load_subject_data()
    summarize(data)
    make_charts(data)
    print_interpretation(data)


if __name__ == "__main__":
    main()
