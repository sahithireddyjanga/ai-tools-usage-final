"""Clean the AI tools usage Excel dataset and save clean_dataset.csv."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "AI_Tools_Usage_Dashboard_Dataset.xlsx"
OUTPUT_FILE = ROOT / "clean_dataset.csv"

def main():
    df = pd.read_excel(INPUT_FILE, sheet_name="Dataset")
    df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    before = len(df)
    df = df.drop_duplicates()
    if "User_ID" in df.columns:
        df = df.drop_duplicates(subset=["User_ID"], keep="first")
    df = df.dropna(how="all")
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Rows before cleaning: {before}")
    print(f"Rows after cleaning:  {len(df)}")
    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
