"""Create varied visualizations for the AI tools usage dataset."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "clean_dataset.csv"
CHART_DIR = ROOT / "outputs" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

def save(fig, filename):
    fig.tight_layout()
    fig.savefig(CHART_DIR / filename, dpi=160, bbox_inches="tight")
    plt.close(fig)

def main():
    df = pd.read_csv(DATA_FILE)

    # 1. Histogram: distribution of daily AI usage
    if "Daily_AI_Usage_Hours" in df:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(df["Daily_AI_Usage_Hours"].dropna(), bins=18, edgecolor="black")
        ax.set(title="Distribution of Daily AI Usage", xlabel="Hours per day", ylabel="Number of users")
        save(fig, "01_daily_usage_histogram.png")

    # 2. Bar chart: number of AI tools used
    if "Num_AI_Tools_Used" in df:
        counts = df["Num_AI_Tools_Used"].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(counts.index.astype(str), counts.values)
        ax.set(title="Users by Number of AI Tools Used", xlabel="Number of AI tools", ylabel="Number of users")
        save(fig, "02_tools_count_bar.png")

    # 3. Scatter plot: usage versus productivity
    if {"Daily_AI_Usage_Hours", "Productivity_Rating"}.issubset(df.columns):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(df["Daily_AI_Usage_Hours"], df["Productivity_Rating"], alpha=0.6)
        ax.set(title="Daily AI Usage vs Productivity", xlabel="Daily AI usage (hours)", ylabel="Productivity rating")
        save(fig, "03_usage_productivity_scatter.png")

    # 4. Box plot: productivity by number of tools
    if {"Num_AI_Tools_Used", "Productivity_Rating"}.issubset(df.columns):
        groups = [g["Productivity_Rating"].dropna().values
                  for _, g in df.groupby("Num_AI_Tools_Used")]
        labels = [str(k) for k in sorted(df["Num_AI_Tools_Used"].dropna().unique())]
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.boxplot(groups, tick_labels=labels)
        ax.set(title="Productivity Rating by Number of AI Tools", xlabel="Number of AI tools", ylabel="Productivity rating")
        save(fig, "04_productivity_boxplot.png")

    # 5. Violin plot: satisfaction by number of tools
    if {"Num_AI_Tools_Used", "Satisfaction_Score"}.issubset(df.columns):
        keys = sorted(df["Num_AI_Tools_Used"].dropna().unique())
        groups = [df.loc[df["Num_AI_Tools_Used"] == k, "Satisfaction_Score"].dropna().values for k in keys]
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.violinplot(groups, showmeans=True, showmedians=True)
        ax.set_xticks(range(1, len(keys) + 1), [str(k) for k in keys])
        ax.set(title="Satisfaction Score by Number of AI Tools", xlabel="Number of AI tools", ylabel="Satisfaction score")
        save(fig, "05_satisfaction_violin.png")

    # 6. Pie chart: age-group share
    if "Age" in df:
        bins = [0, 24, 34, 44, 100]
        labels = ["18–24", "25–34", "35–44", "45+"]
        age_group = pd.cut(df["Age"], bins=bins, labels=labels, include_lowest=True)
        counts = age_group.value_counts().reindex(labels, fill_value=0)
        fig, ax = plt.subplots(figsize=(7, 6))
        ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
        ax.set_title("Users by Age Group")
        save(fig, "06_age_group_pie.png")

    # 7. Correlation heatmap (matplotlib only)
    corr = df.select_dtypes(include="number").corr()
    if not corr.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1, aspect="auto")
        ax.set_xticks(range(len(corr.columns)), corr.columns, rotation=90)
        ax.set_yticks(range(len(corr.index)), corr.index)
        ax.set_title("Correlation Heatmap")
        fig.colorbar(im, ax=ax, label="Correlation")
        save(fig, "07_correlation_heatmap.png")

    print(f"Created {len(list(CHART_DIR.glob('*.png')))} charts in {CHART_DIR}")

if __name__ == "__main__":
    main()
