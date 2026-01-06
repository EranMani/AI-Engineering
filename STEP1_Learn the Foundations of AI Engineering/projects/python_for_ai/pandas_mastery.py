"""
PANDAS MASTERY GUIDE FOR AI ENGINEERING
========================================
A comprehensive guide to mastering pandas for data analysis and manipulation
in AI engineering contexts. Includes examples and hands-on exercises.

This guide covers:
1. Core DataFrame Operations
2. Data Cleaning & Preprocessing
3. Data Transformation
4. Feature Engineering
5. Exploratory Data Analysis
6. Advanced Operations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 80)
print("PANDAS MASTERY GUIDE FOR AI ENGINEERING")
print("=" * 80)

# ============================================================================
# SECTION 1: CORE DATAFRAME OPERATIONS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 1: CORE DATAFRAME OPERATIONS")
print("=" * 80)

# ----------------------------------------------------------------------------
# EXAMPLE 1.1: Creating DataFrames from Different Sources
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 1.1: Creating DataFrames from Different Sources")
print("-" * 80)

# Method 1: From a dictionary of lists
print("\n1. Creating DataFrame from dictionary of lists:")
data_dict = {
    "model_name": ["GPT-4", "Claude", "GPT-3", "BERT"],
    "accuracy": [0.92, 0.89, 0.85, 0.78],
    "latency_ms": [150, 180, 200, 50],
    "cost_per_1k_tokens": [0.03, 0.02, 0.01, 0.005]
}
df_from_dict = pd.DataFrame(data_dict)
print(df_from_dict)

# Method 2: From a list of dictionaries
print("\n2. Creating DataFrame from list of dictionaries:")
data_list = [
    {"model_name": "GPT-4", "accuracy": 0.92, "latency_ms": 150},
    {"model_name": "Claude", "accuracy": 0.89, "latency_ms": 180},
    {"model_name": "GPT-3", "accuracy": 0.85, "latency_ms": 200},
]
df_from_list = pd.DataFrame(data_list)
print(df_from_list)

# Method 3: From CSV (commented - would read from file)
# df_from_csv = pd.read_csv("model_data.csv")

# Method 4: With custom index
print("\n3. Creating DataFrame with custom index:")
df_custom_index = pd.DataFrame(data_dict, index=["A", "B", "C", "D"])
df_custom_index_2 = pd.DataFrame(data_dict, index=["hi", "why", "should", "I"])
print(df_custom_index)
print(df_custom_index_2)

# ----------------------------------------------------------------------------
# EXAMPLE 1.2: Basic DataFrame Inspection
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 1.2: Basic DataFrame Inspection")
print("-" * 80)

df = pd.DataFrame(data_dict)
print("\n1. Display first few rows (.head()):")
print(df.head(2))

print("\n2. Display last few rows (.tail()):")
print(df.tail(2))

print("\n3. Get DataFrame shape (rows, columns):")
print(f"Shape: {df.shape}")

print("\n4. Get column names:")
print(f"Columns: {df.columns.tolist()}")

print("\n5. Get data types (.dtypes):")
print(df.dtypes)

print("\n6. Get summary info (.info()):")
df.info()

print("\n7. Get statistical summary (.describe()):")
print(df.describe())

# ----------------------------------------------------------------------------
# EXAMPLE 1.3: Indexing and Selection
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 1.3: Indexing and Selection")
print("-" * 80)

df = pd.DataFrame(data_dict)

print("\n1. Select a single column (returns Series):")
print(df["model_name"])

print("\n2. Select multiple columns (returns DataFrame):")
print(df[["model_name", "accuracy"]])

print("\n3. Select rows by index using .iloc (integer position):")
print(df.iloc[0])  # First row
print(df.iloc[0:2])  # First two rows
print(df.iloc[0, 1])  # First row, second column

print("\n4. Select rows by label using .loc (label-based):")
print(df.loc[0])  # Row with index 0
print(df.loc[0:2])  # Rows 0 to 2 (inclusive!)
print(df.loc[0, "model_name"])  # Specific cell

print("\n5. Boolean indexing (filtering):")
high_accuracy = df[df["accuracy"] > 0.85]
print("Models with accuracy > 0.85:")
print(high_accuracy)

print("\n6. Multiple conditions:")
fast_and_accurate = df[(df["accuracy"] > 0.85) & (df["latency_ms"] < 200)]
print("Fast AND accurate models:")
print(fast_and_accurate)

# ----------------------------------------------------------------------------
# EXERCISE 1: Basic DataFrame Operations
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 1: Basic DataFrame Operations")
print("=" * 80)

# Scenario: You're analyzing AI model training data
training_data = {
    "epoch": [1, 2, 3, 4, 5],
    "loss": [0.85, 0.72, 0.65, 0.58, 0.52],
    "accuracy": [0.65, 0.78, 0.82, 0.87, 0.91],
    "learning_rate": [0.001, 0.001, 0.0005, 0.0005, 0.0001]
}

# TODO: Complete the following operations:

# 1. Create a DataFrame from training_data
#    Store it in: df_training
df_training = pd.DataFrame(training_data)

# 2. Display the first 3 rows
#    Use: .head(3)
print("\nFirst 3 rows:")
print(df_training.head(3))

# 3. Get the shape of the DataFrame
#    Use: .shape
print(f"\nShape: {df_training.shape}")

# 4. Select only the "epoch" and "accuracy" columns
#    Store in: df_subset
df_subset = df_training[["epoch", "accuracy"]]

# 5. Filter rows where accuracy > 0.80
#    Store in: high_accuracy_epochs
high_accuracy_epochs = df_training[df_training["accuracy"] > 0.80]

# 6. Get the row where loss is minimum
#    Hint: Use .idxmin() to find index, then .loc to get row
min_loss_idx = df_training["loss"].idxmin()
row_min_loss = df_training.loc[min_loss_idx]

# Expected outputs:
# Shape: (5, 4)
# High accuracy epochs: epochs 3, 4, 5
# Min loss row: epoch 5 with loss 0.52

print(f"\nSubset columns: {df_subset.columns.tolist()}")
print(f"\nHigh accuracy epochs:\n{high_accuracy_epochs}")
print(f"\nRow with minimum loss:\n{row_min_loss}")

# ============================================================================
# SECTION 2: DATA CLEANING & PREPROCESSING
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 2: DATA CLEANING & PREPROCESSING")
print("=" * 80)

# ----------------------------------------------------------------------------
# EXAMPLE 2.1: Handling Missing Values
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 2.1: Handling Missing Values")
print("-" * 80)

# Create DataFrame with missing values
data_with_nulls = {
    "model_name": ["GPT-4", "Claude", None, "BERT", "T5"],
    "accuracy": [0.92, None, 0.85, 0.78, 0.88],
    "latency_ms": [150, 180, None, 50, None],
    "cost": [0.03, 0.02, 0.01, None, 0.005]
}
df_nulls = pd.DataFrame(data_with_nulls)

print("Original DataFrame with missing values:")
print(df_nulls)

print("\n1. Check for missing values (.isna() or .isnull()):")
print(df_nulls.isna())

print("\n2. Count missing values per column:")
print(df_nulls.isna().sum())

print("\n3. Check if any row has missing values:")
print(df_nulls.isna().any(axis=1))

print("\n4. Fill missing values with a constant (.fillna()):")
df_filled = df_nulls.fillna(0)
print(df_filled)

print("\n5. Fill missing values with column mean:")
df_filled_mean = df_nulls.copy()
df_filled_mean["accuracy"] = df_filled_mean["accuracy"].fillna(df_filled_mean["accuracy"].mean())
print(df_filled_mean)

print("\n6. Drop rows with any missing values (.dropna()):")
df_no_nulls = df_nulls.dropna()
print(df_no_nulls)

print("\n7. Drop rows where all values are missing:")
df_drop_all = df_nulls.dropna(how="all")
print(df_drop_all)

print("\n8. Drop columns with missing values:")
df_drop_cols = df_nulls.dropna(axis=1)
print(df_drop_cols)

# ----------------------------------------------------------------------------
# EXAMPLE 2.2: Handling Duplicates
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 2.2: Handling Duplicates")
print("-" * 80)

# Create DataFrame with duplicates
data_duplicates = {
    "model_name": ["GPT-4", "Claude", "GPT-4", "BERT", "Claude"],
    "accuracy": [0.92, 0.89, 0.92, 0.78, 0.89],
    "latency_ms": [150, 180, 150, 50, 180]
}
df_dup = pd.DataFrame(data_duplicates)

print("Original DataFrame with duplicates:")
print(df_dup)

print("\n1. Check for duplicate rows (.duplicated()):")
print(df_dup.duplicated())

print("\n2. Find duplicate rows:")
print(df_dup[df_dup.duplicated()])

print("\n3. Remove duplicate rows (.drop_duplicates()):")
df_no_dup = df_dup.drop_duplicates()
print(df_no_dup)

print("\n4. Remove duplicates based on specific columns:")
df_no_dup_cols = df_dup.drop_duplicates(subset=["model_name"])
print(df_no_dup_cols)

# ----------------------------------------------------------------------------
# EXAMPLE 2.3: Data Type Conversions
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 2.3: Data Type Conversions")
print("-" * 80)

data_types = {
    "model_id": ["1", "2", "3", "4"],
    "accuracy": ["0.92", "0.89", "0.85", "0.78"],
    "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
}
df_types = pd.DataFrame(data_types)

print("Original DataFrame with string types:")
print(df_types)
print(f"\nData types:\n{df_types.dtypes}")

print("\n1. Convert column to numeric (.astype()):")
df_types["model_id"] = df_types["model_id"].astype(int)
df_types["accuracy"] = df_types["accuracy"].astype(float)
print(df_types.dtypes)

print("\n2. Convert to datetime (pd.to_datetime()):")
df_types["date"] = pd.to_datetime(df_types["date"])
print(df_types.dtypes)

# ----------------------------------------------------------------------------
# EXAMPLE 2.4: String Operations
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 2.4: String Operations")
print("-" * 80)

data_strings = {
    "model_name": ["GPT-4", "claude-3", "GPT-3.5", "bert-base"],
    "version": ["v1.0", "v2.1", "v1.5", "v0.9"]
}
df_str = pd.DataFrame(data_strings)

print("Original DataFrame:")
print(df_str)

print("\n1. Convert to uppercase (.str.upper()):")
print(df_str["model_name"].str.upper())

print("\n2. Convert to lowercase (.str.lower()):")
print(df_str["model_name"].str.lower())

print("\n3. Replace characters (.str.replace()):")
print(df_str["model_name"].str.replace("-", "_"))

print("\n4. Check if string contains pattern (.str.contains()):")
print(df_str["model_name"].str.contains("GPT"))

print("\n5. Extract numbers (.str.extract()):")
print(df_str["version"].str.extract(r"(\d+\.\d+)"))

# ----------------------------------------------------------------------------
# EXERCISE 2: Data Cleaning
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 2: Data Cleaning")
print("=" * 80)

# Scenario: Cleaning messy AI model performance data
messy_data = {
    "model": ["GPT-4", "Claude", None, "BERT", "GPT-4", "T5"],
    "accuracy": ["0.92", "0.89", "0.85", None, "0.92", "0.88"],
    "latency": [150, 180, None, 50, 150, None],
    "status": ["active", "active", "inactive", "ACTIVE", "active", "inactive"]
}
df_messy = pd.DataFrame(messy_data)

print("Messy DataFrame:")
print(df_messy)

# TODO: Complete the following cleaning operations:

# 1. Convert "accuracy" column to float (handle string values)
#    Store in: df_cleaned
df_cleaned = df_messy.copy()
df_cleaned["accuracy"] = pd.to_numeric(df_cleaned["accuracy"], errors="coerce")

# 2. Fill missing "accuracy" values with the mean
df_cleaned["accuracy"] = df_cleaned["accuracy"].fillna(df_cleaned["accuracy"].mean())

# 3. Fill missing "latency" values with 0
df_cleaned["latency"] = df_cleaned["latency"].fillna(0)

# 4. Drop rows where "model" is missing
df_cleaned = df_cleaned.dropna(subset=["model"])

# 5. Remove duplicate rows (keep first occurrence)
df_cleaned = df_cleaned.drop_duplicates()

# 6. Normalize "status" column to lowercase
df_cleaned["status"] = df_cleaned["status"].str.lower()

# Expected: Clean DataFrame with no missing values, no duplicates, normalized status

print("\nCleaned DataFrame:")
print(df_cleaned)
print(f"\nMissing values:\n{df_cleaned.isna().sum()}")

# ============================================================================
# SECTION 3: DATA TRANSFORMATION
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 3: DATA TRANSFORMATION")
print("=" * 80)

# ----------------------------------------------------------------------------
# EXAMPLE 3.1: Sorting
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 3.1: Sorting")
print("-" * 80)

df = pd.DataFrame(data_dict)

print("Original DataFrame:")
print(df)

print("\n1. Sort by single column (.sort_values()):")
print(df.sort_values("accuracy"))

print("\n2. Sort in descending order:")
print(df.sort_values("accuracy", ascending=False))

print("\n3. Sort by multiple columns:")
print(df.sort_values(["accuracy", "latency_ms"], ascending=[False, True]))

print("\n4. Sort by index (.sort_index()):")
df_sorted_idx = df.sort_index(ascending=False)
print(df_sorted_idx)

# ----------------------------------------------------------------------------
# EXAMPLE 3.2: Grouping and Aggregations
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 3.2: Grouping and Aggregations")
print("-" * 80)

# Create data with groups
group_data = {
    "model_family": ["GPT", "GPT", "Claude", "Claude", "BERT", "BERT"],
    "model_name": ["GPT-3", "GPT-4", "Claude-2", "Claude-3", "BERT-base", "BERT-large"],
    "accuracy": [0.85, 0.92, 0.88, 0.91, 0.78, 0.82],
    "latency_ms": [200, 150, 190, 180, 50, 60]
}
df_group = pd.DataFrame(group_data)

print("Original DataFrame:")
print(df_group)

print("\n1. Group by single column (.groupby()):")
grouped = df_group.groupby("model_family")
print(f"Groups: {grouped.groups}")

print("\n2. Calculate mean for each group:")
print(grouped.mean())

print("\n3. Multiple aggregations (.agg()):")
print(grouped.agg({
    "accuracy": ["mean", "max", "min"],
    "latency_ms": ["mean", "std"]
}))

print("\n4. Custom aggregation functions:")
print(grouped.agg({
    "accuracy": lambda x: x.max() - x.min()  # Range
}))

# ----------------------------------------------------------------------------
# EXAMPLE 3.3: Pivoting and Reshaping
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 3.3: Pivoting and Reshaping")
print("-" * 80)

# Create data suitable for pivoting
pivot_data = {
    "model": ["GPT-4", "GPT-4", "Claude", "Claude", "BERT", "BERT"],
    "metric": ["accuracy", "latency", "accuracy", "latency", "accuracy", "latency"],
    "value": [0.92, 150, 0.89, 180, 0.78, 50]
}
df_pivot = pd.DataFrame(pivot_data)

print("Original DataFrame:")
print(df_pivot)

print("\n1. Pivot table (.pivot()):")
df_pivoted = df_pivot.pivot(index="model", columns="metric", values="value")
print(df_pivoted)

print("\n2. Melt (unpivot) DataFrame (.melt()):")
df_melted = df_pivoted.reset_index().melt(id_vars="model", var_name="metric", value_name="value")
print(df_melted)

# ----------------------------------------------------------------------------
# EXERCISE 3: Data Transformation
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 3: Data Transformation")
print("=" * 80)

# Scenario: Analyzing model performance across different datasets
transformation_data = {
    "model": ["GPT-4", "GPT-4", "Claude", "Claude", "GPT-3", "GPT-3"],
    "dataset": ["dataset_A", "dataset_B", "dataset_A", "dataset_B", "dataset_A", "dataset_B"],
    "accuracy": [0.92, 0.88, 0.89, 0.91, 0.85, 0.83],
    "latency_ms": [150, 145, 180, 175, 200, 195]
}
df_transform = pd.DataFrame(transformation_data)

print("Original DataFrame:")
print(df_transform)

# TODO: Complete the following transformations:

# 1. Sort by model name, then by accuracy (descending)
#    Store in: df_sorted
df_sorted = df_transform.sort_values(["model", "accuracy"], ascending=[True, False])

# 2. Group by model and calculate average accuracy and latency
#    Store in: model_avg
model_avg = df_transform.groupby("model").agg({
    "accuracy": "mean",
    "latency_ms": "mean"
})

# 3. Create a pivot table with models as rows, datasets as columns, accuracy as values
#    Store in: df_pivot_table
df_pivot_table = df_transform.pivot(index="model", columns="dataset", values="accuracy")

# 4. Find the best performing model for each dataset
#    Hint: Group by dataset, then find max accuracy
best_per_dataset = df_transform.groupby("dataset").apply(
    lambda x: x.loc[x["accuracy"].idxmax(), ["model", "accuracy"]]
)

# Expected outputs:
# Model averages: GPT-4 (0.90), Claude (0.90), GPT-3 (0.84)
# Best per dataset: dataset_A -> GPT-4, dataset_B -> Claude

print("\nSorted DataFrame:")
print(df_sorted)
print("\nModel averages:")
print(model_avg)
print("\nPivot table:")
print(df_pivot_table)
print("\nBest model per dataset:")
print(best_per_dataset)

# ============================================================================
# SECTION 4: FEATURE ENGINEERING
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 4: FEATURE ENGINEERING")
print("=" * 80)

# ----------------------------------------------------------------------------
# EXAMPLE 4.1: Creating New Columns
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 4.1: Creating New Columns")
print("-" * 80)

df = pd.DataFrame(data_dict)

print("Original DataFrame:")
print(df)

print("\n1. Create new column by calculation:")
df["cost_per_accuracy"] = df["cost_per_1k_tokens"] / df["accuracy"]
print(df)

print("\n2. Create column using .assign() (returns new DataFrame):")
df_new = df.assign(efficiency=df["accuracy"] / df["latency_ms"])
print(df_new)

print("\n3. Create column with conditional logic:")
df["performance_tier"] = df["accuracy"].apply(
    lambda x: "High" if x > 0.90 else "Medium" if x > 0.85 else "Low"
)
print(df)

# ----------------------------------------------------------------------------
# EXAMPLE 4.2: Applying Functions
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 4.2: Applying Functions")
print("-" * 80)

df = pd.DataFrame(data_dict)

print("Original DataFrame:")
print(df)

print("\n1. Apply function to each element (.apply() on Series):")
df["accuracy_percent"] = df["accuracy"].apply(lambda x: f"{x*100:.1f}%")
print(df["accuracy_percent"])

print("\n2. Apply function to each row (.apply() on DataFrame with axis=1):")
def calculate_score(row):
    return row["accuracy"] * 100 - row["latency_ms"] / 10

df["score"] = df.apply(calculate_score, axis=1)
print(df[["model_name", "score"]])

print("\n3. Apply function to each column (.apply() on DataFrame with axis=0):")
print(df[["accuracy", "latency_ms"]].apply(np.mean))

print("\n4. Map values using dictionary (.map()):")
tier_map = {0.92: "S", 0.89: "A", 0.85: "B", 0.78: "C"}
df["tier"] = df["accuracy"].map(tier_map)
print(df[["model_name", "tier"]])

# ----------------------------------------------------------------------------
# EXAMPLE 4.3: Binning and Discretization
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 4.3: Binning and Discretization")
print("-" * 80)

df = pd.DataFrame(data_dict)

print("Original DataFrame:")
print(df)

print("\n1. Create bins with pd.cut() (equal-width bins):")
df["accuracy_bin"] = pd.cut(df["accuracy"], bins=3, labels=["Low", "Medium", "High"])
print(df[["model_name", "accuracy", "accuracy_bin"]])

print("\n2. Create bins with pd.qcut() (equal-frequency bins):")
df["latency_bin"] = pd.qcut(df["latency_ms"], q=2, labels=["Fast", "Slow"])
print(df[["model_name", "latency_ms", "latency_bin"]])

# ----------------------------------------------------------------------------
# EXAMPLE 4.4: One-Hot Encoding
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 4.4: One-Hot Encoding")
print("-" * 80)

data_categorical = {
    "model_name": ["GPT-4", "Claude", "GPT-3", "BERT"],
    "category": ["LLM", "LLM", "LLM", "Encoder"]
}
df_cat = pd.DataFrame(data_categorical)

print("Original DataFrame:")
print(df_cat)

print("\n1. One-hot encode categorical column (pd.get_dummies()):")
df_encoded = pd.get_dummies(df_cat, columns=["category"], prefix="cat")
print(df_encoded)

# ----------------------------------------------------------------------------
# EXERCISE 4: Feature Engineering
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 4: Feature Engineering")
print("=" * 80)

# Scenario: Creating features for model performance analysis
feature_data = {
    "model": ["GPT-4", "Claude", "GPT-3", "BERT", "T5"],
    "accuracy": [0.92, 0.89, 0.85, 0.78, 0.88],
    "latency_ms": [150, 180, 200, 50, 170],
    "cost": [0.03, 0.02, 0.01, 0.005, 0.015],
    "model_type": ["LLM", "LLM", "LLM", "Encoder", "Encoder"]
}
df_features = pd.DataFrame(feature_data)

print("Original DataFrame:")
print(df_features)

# TODO: Complete the following feature engineering tasks:

# 1. Create a "cost_efficiency" column: accuracy / cost
#    Store in: df_features
df_features["cost_efficiency"] = df_features["accuracy"] / df_features["cost"]

# 2. Create a "speed_score" column: 1000 / latency_ms (higher is faster)
df_features["speed_score"] = 1000 / df_features["latency_ms"]

# 3. Create a "performance_tier" column based on accuracy:
#    "Excellent" if accuracy >= 0.90, "Good" if >= 0.85, else "Fair"
df_features["performance_tier"] = df_features["accuracy"].apply(
    lambda x: "Excellent" if x >= 0.90 else "Good" if x >= 0.85 else "Fair"
)

# 4. Bin latency into 3 categories: "Fast" (<100), "Medium" (100-150), "Slow" (>150)
df_features["latency_category"] = pd.cut(
    df_features["latency_ms"],
    bins=[0, 100, 150, float("inf")],
    labels=["Fast", "Medium", "Slow"]
)

# 5. One-hot encode the "model_type" column
df_features = pd.get_dummies(df_features, columns=["model_type"], prefix="type")

# Expected: DataFrame with 5 new feature columns

print("\nDataFrame with engineered features:")
print(df_features)
print(f"\nNew columns: {df_features.columns.tolist()}")

# ============================================================================
# SECTION 5: EXPLORATORY DATA ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 5: EXPLORATORY DATA ANALYSIS")
print("=" * 80)

# ----------------------------------------------------------------------------
# EXAMPLE 5.1: Statistical Summaries
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 5.1: Statistical Summaries")
print("-" * 80)

df = pd.DataFrame(data_dict)

print("Original DataFrame:")
print(df)

print("\n1. Basic statistics (.describe()):")
print(df.describe())

print("\n2. Specific statistics:")
print(f"Mean accuracy: {df['accuracy'].mean()}")
print(f"Median accuracy: {df['accuracy'].median()}")
print(f"Std deviation: {df['accuracy'].std()}")
print(f"Min accuracy: {df['accuracy'].min()}")
print(f"Max accuracy: {df['accuracy'].max()}")

print("\n3. Correlation matrix (.corr()):")
print(df[["accuracy", "latency_ms", "cost_per_1k_tokens"]].corr())

# ----------------------------------------------------------------------------
# EXAMPLE 5.2: Value Counts and Cross-Tabulations
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 5.2: Value Counts and Cross-Tabulations")
print("-" * 80)

data_counts = {
    "model": ["GPT-4", "Claude", "GPT-4", "BERT", "Claude", "GPT-4"],
    "status": ["active", "active", "active", "inactive", "active", "active"],
    "tier": ["High", "High", "High", "Low", "High", "High"]
}
df_counts = pd.DataFrame(data_counts)

print("Original DataFrame:")
print(df_counts)

print("\n1. Count occurrences (.value_counts()):")
print(df_counts["model"].value_counts())

print("\n2. Count with percentages:")
print(df_counts["model"].value_counts(normalize=True))

print("\n3. Cross-tabulation (.crosstab()):")
print(pd.crosstab(df_counts["model"], df_counts["status"]))

# ----------------------------------------------------------------------------
# EXAMPLE 5.3: Aggregations
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 5.3: Aggregations")
print("-" * 80)

df = pd.DataFrame(data_dict)

print("Original DataFrame:")
print(df)

print("\n1. Sum of numeric columns:")
print(df.select_dtypes(include=[np.number]).sum())

print("\n2. Mean of numeric columns:")
print(df.select_dtypes(include=[np.number]).mean())

print("\n3. Multiple aggregations at once:")
print(df.agg({
    "accuracy": ["mean", "max", "min"],
    "latency_ms": ["mean", "std"]
}))

# ----------------------------------------------------------------------------
# EXERCISE 5: Exploratory Data Analysis
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 5: Exploratory Data Analysis")
print("=" * 80)

# Scenario: Analyzing comprehensive model performance data
eda_data = {
    "model": ["GPT-4", "Claude", "GPT-3", "BERT", "T5", "GPT-4", "Claude"],
    "dataset": ["A", "A", "A", "A", "A", "B", "B"],
    "accuracy": [0.92, 0.89, 0.85, 0.78, 0.88, 0.88, 0.91],
    "latency_ms": [150, 180, 200, 50, 170, 145, 175],
    "cost": [0.03, 0.02, 0.01, 0.005, 0.015, 0.03, 0.02]
}
df_eda = pd.DataFrame(eda_data)

print("Original DataFrame:")
print(df_eda)

# TODO: Complete the following EDA tasks:

# 1. Calculate overall statistics for accuracy and latency
#    Store in: stats_summary
stats_summary = df_eda[["accuracy", "latency_ms"]].describe()

# 2. Count how many times each model appears
#    Store in: model_counts
model_counts = df_eda["model"].value_counts()

# 3. Calculate correlation between accuracy and latency
#    Store in: accuracy_latency_corr
accuracy_latency_corr = df_eda["accuracy"].corr(df_eda["latency_ms"])

# 4. Create a cross-tabulation of model vs dataset
#    Store in: model_dataset_ct
model_dataset_ct = pd.crosstab(df_eda["model"], df_eda["dataset"])

# 5. Calculate average accuracy per model
#    Store in: avg_accuracy_per_model
avg_accuracy_per_model = df_eda.groupby("model")["accuracy"].mean()

# Expected outputs:
# Model counts: GPT-4 (2), Claude (2), GPT-3 (1), BERT (1), T5 (1)
# Correlation: negative (higher accuracy, lower latency)
# Average accuracy: varies by model

print("\nStatistics summary:")
print(stats_summary)
print("\nModel counts:")
print(model_counts)
print(f"\nAccuracy-Latency correlation: {accuracy_latency_corr:.4f}")
print("\nModel-Dataset cross-tabulation:")
print(model_dataset_ct)
print("\nAverage accuracy per model:")
print(avg_accuracy_per_model)

# ============================================================================
# SECTION 6: ADVANCED OPERATIONS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 6: ADVANCED OPERATIONS")
print("=" * 80)

# ----------------------------------------------------------------------------
# EXAMPLE 6.1: Merging DataFrames
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 6.1: Merging DataFrames")
print("-" * 80)

# Create two DataFrames to merge
df1 = pd.DataFrame({
    "model": ["GPT-4", "Claude", "BERT"],
    "accuracy": [0.92, 0.89, 0.78]
})

df2 = pd.DataFrame({
    "model": ["GPT-4", "Claude", "T5"],
    "latency_ms": [150, 180, 170]
})

print("DataFrame 1:")
print(df1)
print("\nDataFrame 2:")
print(df2)

print("\n1. Inner join (.merge()):")
df_inner = pd.merge(df1, df2, on="model", how="inner")
print(df_inner)

print("\n2. Left join:")
df_left = pd.merge(df1, df2, on="model", how="left")
print(df_left)

print("\n3. Right join:")
df_right = pd.merge(df1, df2, on="model", how="right")
print(df_right)

print("\n4. Outer join (full):")
df_outer = pd.merge(df1, df2, on="model", how="outer")
print(df_outer)

# ----------------------------------------------------------------------------
# EXAMPLE 6.2: Concatenation
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 6.2: Concatenation")
print("-" * 80)

df_a = pd.DataFrame({
    "model": ["GPT-4", "Claude"],
    "accuracy": [0.92, 0.89]
})

df_b = pd.DataFrame({
    "model": ["BERT", "T5"],
    "accuracy": [0.78, 0.88]
})

print("DataFrame A:")
print(df_a)
print("\nDataFrame B:")
print(df_b)

print("\n1. Concatenate vertically (.concat()):")
df_concat = pd.concat([df_a, df_b], ignore_index=True)
print(df_concat)

print("\n2. Concatenate horizontally:")
df_c = pd.DataFrame({
    "latency_ms": [150, 180]
})
df_concat_h = pd.concat([df_a, df_c], axis=1)
print(df_concat_h)

# ----------------------------------------------------------------------------
# EXAMPLE 6.3: Time Series Operations
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 6.3: Time Series Operations")
print("-" * 80)

# Create time series data
dates = pd.date_range("2024-01-01", periods=10, freq="D")
ts_data = {
    "date": dates,
    "model_requests": np.random.randint(100, 1000, 10),
    "accuracy": np.random.uniform(0.85, 0.95, 10)
}
df_ts = pd.DataFrame(ts_data)
df_ts.set_index("date", inplace=True)

print("Time Series DataFrame:")
print(df_ts.head())

print("\n1. Resample to weekly data (.resample()):")
df_weekly = df_ts.resample("W").mean()
print(df_weekly)

print("\n2. Extract date components (.dt accessor):")
df_ts_reset = df_ts.reset_index()
df_ts_reset["year"] = df_ts_reset["date"].dt.year
df_ts_reset["month"] = df_ts_reset["date"].dt.month
df_ts_reset["day_of_week"] = df_ts_reset["date"].dt.day_name()
print(df_ts_reset[["date", "year", "month", "day_of_week"]].head())

# ----------------------------------------------------------------------------
# EXAMPLE 6.4: Multi-Index DataFrames
# ----------------------------------------------------------------------------
print("\n" + "-" * 80)
print("EXAMPLE 6.4: Multi-Index DataFrames")
print("-" * 80)

# Create multi-index data
arrays = [
    ["GPT-4", "GPT-4", "Claude", "Claude"],
    ["dataset_A", "dataset_B", "dataset_A", "dataset_B"]
]
multi_index = pd.MultiIndex.from_arrays(arrays, names=["model", "dataset"])

df_multi = pd.DataFrame({
    "accuracy": [0.92, 0.88, 0.89, 0.91],
    "latency_ms": [150, 145, 180, 175]
}, index=multi_index)

print("Multi-Index DataFrame:")
print(df_multi)

print("\n1. Access data by first level index:")
print(df_multi.loc["GPT-4"])

print("\n2. Access data by both levels:")
print(df_multi.loc[("GPT-4", "dataset_A")])

print("\n3. Reset index to regular columns:")
print(df_multi.reset_index())

# ----------------------------------------------------------------------------
# EXERCISE 6: Advanced Operations
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 6: Advanced Operations")
print("=" * 80)

# Scenario: Combining and analyzing data from multiple sources
df_performance = pd.DataFrame({
    "model": ["GPT-4", "Claude", "BERT", "T5"],
    "accuracy": [0.92, 0.89, 0.78, 0.88]
})

df_latency = pd.DataFrame({
    "model": ["GPT-4", "Claude", "GPT-3", "BERT"],
    "latency_ms": [150, 180, 200, 50]
})

df_cost = pd.DataFrame({
    "model": ["GPT-4", "Claude", "BERT"],
    "cost": [0.03, 0.02, 0.005]
})

print("Performance DataFrame:")
print(df_performance)
print("\nLatency DataFrame:")
print(df_latency)
print("\nCost DataFrame:")
print(df_cost)

# TODO: Complete the following advanced operations:

# 1. Merge all three DataFrames using left join on "model"
#    Start with df_performance, then merge df_latency, then df_cost
#    Store in: df_combined
df_combined = pd.merge(df_performance, df_latency, on="model", how="left")
df_combined = pd.merge(df_combined, df_cost, on="model", how="left")

# 2. Create a time series DataFrame with daily model usage
#    Dates: 2024-01-01 to 2024-01-05
#    Columns: date, requests (random between 100-500)
#    Store in: df_usage
dates = pd.date_range("2024-01-01", periods=5, freq="D")
df_usage = pd.DataFrame({
    "date": dates,
    "requests": np.random.randint(100, 500, 5)
})

# 3. Set "date" as index and resample to get total requests per week
#    Store in: df_weekly_usage
df_usage_indexed = df_usage.set_index("date")
df_weekly_usage = df_usage_indexed.resample("W").sum()

# 4. Create a multi-index DataFrame from df_combined
#    First level: model, Second level: metric (accuracy, latency_ms, cost)
#    Store in: df_multi_index
df_multi_index = df_combined.set_index("model")
df_multi_index = df_multi_index.stack().reset_index()
df_multi_index.columns = ["model", "metric", "value"]
df_multi_index = df_multi_index.set_index(["model", "metric"])

# Expected: Combined DataFrame with all metrics, time series data, multi-index structure

print("\nCombined DataFrame:")
print(df_combined)
print("\nUsage DataFrame:")
print(df_usage)
print("\nWeekly usage:")
print(df_weekly_usage)
print("\nMulti-index DataFrame:")
print(df_multi_index)

print("\n" + "=" * 80)
print("PANDAS MASTERY GUIDE COMPLETE!")
print("=" * 80)
print("\nYou've learned the most essential pandas operations for AI engineering:")
print("✓ Core DataFrame operations")
print("✓ Data cleaning and preprocessing")
print("✓ Data transformation")
print("✓ Feature engineering")
print("✓ Exploratory data analysis")
print("✓ Advanced operations (merging, time series, multi-index)")
print("\nPractice these concepts regularly to master pandas!")

