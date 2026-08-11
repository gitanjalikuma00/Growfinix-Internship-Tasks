import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# 1. File paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "Tour_Enquiries.csv"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# 2. Load dataset
# -----------------------------
df = pd.read_csv(DATA_FILE)

print("\n===== DATASET OVERVIEW =====")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("\nColumns:")
print(df.columns.tolist())

print("\n===== FIRST 5 RECORDS =====")
print(df.head())

# -----------------------------
# 3. Data cleaning
# -----------------------------
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Income"] = pd.to_numeric(df["Income"], errors="coerce")

df["Age"] = df["Age"].fillna(df["Age"].median())
df["Income"] = df["Income"].fillna(df["Income"].median())
df["Destination"] = df["Destination"].fillna("Unknown")

# Create age groups
df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 18, 25, 35, 45, 55, 100],
    labels=["Under 18", "18-25", "26-35", "36-45", "46-55", "56+"],
    include_lowest=True
)

# Create income brackets
df["Income_Bracket"] = pd.cut(
    df["Income"],
    bins=[0, 30000, 60000, 100000, 150000, 250000, float("inf")],
    labels=[
        "Below 30K",
        "30K-60K",
        "60K-100K",
        "100K-150K",
        "150K-250K",
        "250K+"
    ],
    include_lowest=True
)

# -----------------------------
# 4. Popular destinations
# -----------------------------
destination_counts = (
    df["Destination"]
    .value_counts()
    .head(10)
)

print("\n===== TOP 10 DESTINATIONS =====")
print(destination_counts)

# Save result
destination_counts.to_csv(
    OUTPUT_DIR / "top_destinations.csv",
    header=["Enquiries"]
)

# -----------------------------
# 5. Age group analysis
# -----------------------------
age_counts = df["Age_Group"].value_counts().sort_index()

print("\n===== AGE GROUP ANALYSIS =====")
print(age_counts)

age_counts.to_csv(
    OUTPUT_DIR / "age_group_analysis.csv",
    header=["Customers"]
)

# -----------------------------
# 6. Income bracket analysis
# -----------------------------
income_counts = df["Income_Bracket"].value_counts().sort_index()

print("\n===== INCOME BRACKET ANALYSIS =====")
print(income_counts)

income_counts.to_csv(
    OUTPUT_DIR / "income_bracket_analysis.csv",
    header=["Customers"]
)

# -----------------------------
# 7. Bar chart - Destinations
# -----------------------------
plt.figure(figsize=(10, 6))

destination_counts.plot(kind="bar")

plt.title("Top 10 Most Popular Travel Destinations")
plt.xlabel("Destination")
plt.ylabel("Number of Enquiries")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "popular_destinations.png",
    dpi=300
)

plt.close()

# -----------------------------
# 8. Bar chart - Age Groups
# -----------------------------
plt.figure(figsize=(10, 6))

age_counts.plot(kind="bar")

plt.title("Customer Enquiries by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "age_groups.png",
    dpi=300
)

plt.close()

# -----------------------------
# 9. Histogram - Age
# -----------------------------
plt.figure(figsize=(10, 6))

plt.hist(df["Age"], bins=10)

plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "age_histogram.png",
    dpi=300
)

plt.close()

# -----------------------------
# 10. Histogram - Income
# -----------------------------
plt.figure(figsize=(10, 6))

plt.hist(df["Income"], bins=10)

plt.title("Customer Income Distribution")
plt.xlabel("Income")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "income_histogram.png",
    dpi=300
)

plt.close()

# -----------------------------
# 11. Save cleaned dataset
# -----------------------------
df.to_csv(
    OUTPUT_DIR / "cleaned_tour_enquiries.csv",
    index=False
)

print("\n================================")
print("TASK 3 ANALYSIS COMPLETED")
print("================================")
print("Results saved inside the output folder.")