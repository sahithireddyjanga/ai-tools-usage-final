"""Generate descriptive statistics, correlations and grouped analysis."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "clean_dataset.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main():
    df = pd.read_csv(DATA_FILE)
    df.describe().T.to_csv(OUT / "descriptive_statistics.csv")
    df.corr(numeric_only=True).round(3).to_csv(OUT / "correlation_matrix.csv")

    if {"Num_AI_Tools_Used", "Productivity_Rating"}.issubset(df.columns):
        (df.groupby("Num_AI_Tools_Used")["Productivity_Rating"]
           .agg(["count", "mean", "median", "std"])
           .round(3).to_csv(OUT / "productivity_by_tool_count.csv"))

    if {"Num_AI_Tools_Used", "Satisfaction_Score"}.issubset(df.columns):
        (df.groupby("Num_AI_Tools_Used")["Satisfaction_Score"]
           .agg(["count", "mean", "median", "std"])
           .round(3).to_csv(OUT / "satisfaction_by_tool_count.csv"))

    missing = df.isna().sum().rename("missing_values").to_frame()
    missing.to_csv(OUT / "missing_values_report.csv")
    print("Analysis complete. Results saved in the outputs folder.")

if __name__ == "__main__":
    main()
