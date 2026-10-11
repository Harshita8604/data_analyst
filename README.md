# Student Performance & Study Habits Analysis

A beginner-friendly data analytics project exploring how study time, absences, and previous academic performance relate to students' final grades.

## Project questions
- How do average final grades differ across weekly study-time groups?
- Are school absences associated with final grades?
- What are the average grades and pass rates in Mathematics and Portuguese?
- How strongly are study time, absences, and prior-period grades associated with final grade?

## Dataset
This project uses the **Student Performance** dataset from the UCI Machine Learning Repository. It contains student records from two Portuguese secondary schools, with separate files for Mathematics and Portuguese.

- Dataset page: https://archive.ics.uci.edu/dataset/320/student+performance
- Citation: Cortez, P. (2008). *Student Performance* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T
- The script downloads the dataset through the `ucimlrepo` Python package when you run it.

## Tools
Python, Pandas, Matplotlib, Seaborn.

## Run the project
1. Install Python 3.10+.
2. Clone or download this repository.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run:
   ```bash
   python student_performance_analysis.py
   ```
5. The script prints summary tables and saves charts in the `outputs/` folder.

Internet access is required on the first run to retrieve the dataset.

## Key definitions
- **Final grade:** `G3`, on a 0–20 scale.
- **Pass threshold used here:** `G3 >= 10`. This is an analysis assumption for this project, not a universal grading rule.
- **Study time:** UCI's ordinal category for weekly study time (from less than 2 hours to more than 10 hours).
- Mathematics and Portuguese are analyzed separately because students may appear in both subject datasets; their records should not automatically be treated as unique individuals across subjects.

## Interpretation note
This is descriptive analysis. Relationships in this dataset do not prove that study time or absences cause a particular grade. The data comes from two schools in Portugal, so results may not generalize to every school or country.

## Project structure
```
data_analyst/
├── README.md
├── requirements.txt
├── student_performance_analysis.py
└── outputs/                 # charts are generated here
```
