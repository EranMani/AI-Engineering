"""
PANDAS EXERCISES FOR AI ENGINEERING
===================================
Comprehensive practice exercises covering all pandas concepts for AI engineering.
Complete each exercise by writing code in the TODO sections.

This file corresponds to pandas_mastery.py and provides hands-on practice for:
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
print("PANDAS EXERCISES FOR AI ENGINEERING")
print("=" * 80)

# ============================================================================
# SECTION 1: CORE DATAFRAME OPERATIONS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 1: CORE DATAFRAME OPERATIONS")
print("=" * 80)

# ----------------------------------------------------------------------------
# EXERCISE 1.1: Creating and Inspecting DataFrames
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 1.1: Creating and Inspecting DataFrames")
print("=" * 80)

# Scenario: You're setting up a dataset for model performance tracking
model_data = {
    "model_name": ["GPT-4", "Claude-3", "GPT-3.5", "Llama-2", "Mistral"],
    "accuracy": [0.92, 0.91, 0.88, 0.85, 0.87],
    "latency_ms": [150, 180, 200, 250, 170],
    "tokens_per_second": [66.7, 55.6, 50.0, 40.0, 58.8]
}

# TODO: Complete the following operations:

# 1. Create a DataFrame from model_data
#    Store in: df_models
df_models = pd.DataFrame(model_data)

# 2. Display the first 2 rows
#    Use: .head(2)
print("\nFirst 2 rows:")
# TODO: Your code here
df_models.head(2)

# 3. Display the last 2 rows
#    Use: .tail(2)
print("\nLast 2 rows:")
# TODO: Your code here
df_models.tail(2)

# 4. Get the shape of the DataFrame
#    Store in: df_shape
df_shape = df_models.shape
print(f"\nShape: {df_shape}")

# 5. Get column names as a list
#    Store in: column_names
column_names = df_models.columns.tolist()
print(f"\nColumn names: {column_names}")

# 6. Get data types of all columns
#    Store in: dtypes_info
dtypes_info = df_models.dtypes
print(f"\nData types:\n{dtypes_info}")

# 7. Get a summary of the DataFrame using .info()
print("\nDataFrame info:")
# TODO: Your code here
df_models.info()

# Expected outputs:
# Shape: (5, 4)
# Column names: ['model_name', 'accuracy', 'latency_ms', 'tokens_per_second']
# Data types: model_name (object), accuracy (float64), etc.

# ----------------------------------------------------------------------------
# EXERCISE 1.2: Column Selection and Basic Indexing
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 1.2: Column Selection and Basic Indexing")
print("=" * 80)

# Scenario: Analyzing specific metrics from the model dataset
df = pd.DataFrame(model_data)

# TODO: Complete the following operations:

# 1. Select only the "model_name" column (returns Series)
#    Store in: model_names
model_names = df["model_name"]  # TODO: Your code here
print("\nModel names:")
print(model_names)

# 2. Select "model_name" and "accuracy" columns (returns DataFrame)
#    Store in: df_name_acc
df_name_acc = df[["model_name", "accuracy"]]  # TODO: Your code here
print("\nModel names and accuracy:")
print(df_name_acc)

# 3. Select the first row using .iloc (integer position)
#    Store in: first_row
first_row = df.iloc[0]  # TODO: Your code here
print("\nFirst row:")
print(first_row)

# 4. Select rows 0 to 2 (inclusive) using .iloc
#    Store in: first_three_rows
first_three_rows = df.iloc[0:3]  # TODO: Your code here
print("\nFirst three rows:")
print(first_three_rows)

# 5. Select the value at row 0, column "accuracy" using .iloc
#    Store in: first_accuracy
first_accuracy = df["accuracy"].iloc[0]  # TODO: Your code here
print(f"\nFirst accuracy value: {first_accuracy}")

# 6. Select row with index 2 using .loc (label-based)
#    Store in: row_2
row_2 = df.loc[2]  # TODO: Your code here
print("\nRow at index 2:")
print(row_2)

# 7. Select the value at row 0, column "model_name" using .loc
#    Store in: first_model_name
first_model_name = df["model_name"].loc[0]  # TODO: Your code here
print(f"\nFirst model name: {first_model_name}")

# Expected outputs:
# First accuracy: 0.92
# First model name: GPT-4

# ----------------------------------------------------------------------------
# EXERCISE 1.3: Boolean Indexing and Filtering
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 1.3: Boolean Indexing and Filtering")
print("=" * 80)

# Scenario: Filtering models based on performance criteria
df = pd.DataFrame(model_data)  # TODO: Your code here

# TODO: Complete the following filtering operations:

# 1. Filter models with accuracy > 0.88
#    Store in: high_accuracy_models
high_accuracy_models = df[df["accuracy"] > 0.88]  # TODO: Your code here
print("\nHigh accuracy models (>0.88):")
print(high_accuracy_models)

# 2. Filter models with latency < 200ms
#    Store in: fast_models
fast_models = df[df["latency_ms"] < 200]  # TODO: Your code here
print("\nFast models (<200ms):")
print(fast_models)

# 3. Filter models with accuracy >= 0.88 AND latency < 200ms
#    Use: & operator (and), | operator (or), ~ operator (not)
#    Store in: best_models
best_models = df[(df["accuracy"] >= 0.88) & (df["latency_ms"] < 200)]  # TODO: Your code here
print("\nBest models (accuracy >= 0.88 AND latency < 200ms):")
print(best_models)

# 4. Filter models with accuracy > 0.90 OR latency < 150ms
#    Store in: excellent_models
excellent_models = df[(df["accuracy"] > 0.90) | (df["latency_ms"] < 150)]
print("\nExcellent models (accuracy > 0.90 OR latency < 150ms):")
print(excellent_models)

# 5. Filter models where model_name contains "GPT"
#    Use: .str.contains()
#    Store in: gpt_models
gpt_models = df[df["model_name"].str.contains("GPT")]
print("\nGPT models:")
print(gpt_models)

# Expected outputs:
# High accuracy: GPT-4, Claude-3
# Best models: GPT-4, Claude-3
# GPT models: GPT-4, GPT-3.5

# ----------------------------------------------------------------------------
# EXERCISE 1.4: Statistical Summary and Basic Analysis
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 1.4: Statistical Summary and Basic Analysis")
print("=" * 80)

# Scenario: Getting quick insights from model performance data
df = pd.DataFrame(model_data)

# TODO: Complete the following analysis operations:

# 1. Get statistical summary using .describe()
#    Store in: stats_summary
stats_summary = df.describe()
print("\nStatistical summary:")
print(stats_summary)

# 2. Calculate mean accuracy
#    Store in: mean_accuracy
mean_accuracy = df["accuracy"].mean()
print(f"\nMean accuracy: {mean_accuracy:.3f}")

# 3. Calculate median latency
#    Store in: median_latency
median_latency = df["latency_ms"].median()
print(f"\nMedian latency: {median_latency}ms")

# 4. Find the model with maximum accuracy
#    Hint: Use .idxmax() to get index, then .loc to get row
#    Store in: best_model
best_model_idx = df["accuracy"].idxmax()  # TODO: Your code here
best_model = df.loc[best_model_idx]  # TODO: Your code here
print("\nBest model (highest accuracy):")
print(best_model)

# 5. Find the model with minimum latency
#    Store in: fastest_model
fastest_model_idx = df["latency_ms"].idxmin()
fastest_model = df.loc[fastest_model_idx]  # TODO: Your code here
print("\nFastest model (lowest latency):")
print(fastest_model)

# 6. Calculate standard deviation of accuracy
#    Store in: accuracy_std
accuracy_std = df["accuracy"].std()
print(f"\nAccuracy standard deviation: {accuracy_std:.4f}")

# Expected outputs:
# Mean accuracy: ~0.886
# Best model: GPT-4
# Fastest model: GPT-4 (150ms)

# ============================================================================
# SECTION 2: DATA CLEANING & PREPROCESSING
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 2: DATA CLEANING & PREPROCESSING")
print("=" * 80)

# ----------------------------------------------------------------------------
# EXERCISE 2.1: Handling Missing Values
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 2.1: Handling Missing Values")
print("=" * 80)

# Scenario: Cleaning model performance data with missing values
messy_data = {
    "model_name": ["GPT-4", "Claude", None, "BERT", "T5", "Llama-2"],
    "accuracy": [0.92, None, None, 0.78, 0.88, None],
    "latency_ms": [150, 180, None, 50, None, 250],
    "cost": [0.03, 0.02, None, None, 0.015, 0.005]
}
df_messy = pd.DataFrame(messy_data)

print("Original messy DataFrame:")
print(df_messy)

# TODO: Complete the following cleaning operations:

# 1. Check for missing values using .isna()
#    Store in: missing_check
missing_check = df_messy.isna()
print("\nMissing values check:")
print(missing_check)

# 2. Count missing values per column
#    Store in: missing_counts
missing_counts = df_messy.isna().any(axis=1)
print("\nMissing values count per column:")
print(missing_counts)

# 3. Fill missing "accuracy" values with the mean accuracy
#    Store in: df_filled_mean
df_filled_mean = df_messy.copy()
df_filled_mean["accuracy"] = df_filled_mean["accuracy"].fillna(df_filled_mean["accuracy"].mean())
# TODO: Fill missing accuracy values with mean
print("\nDataFrame with accuracy filled (mean):")
print(df_filled_mean[["model_name", "accuracy"]])

# 4. Fill missing "latency_ms" values with 0
#    Store in: df_filled_zero
df_filled_zero = df_messy.copy()
df_filled_zero["latency_ms"] = df_filled_zero["latency_ms"].fillna(0)

# TODO: Fill missing latency_ms values with 0
print("\nDataFrame with latency filled (0):")
print(df_filled_zero[["model_name", "latency_ms"]])

# 5. Drop rows where "model_name" is missing
#    Store in: df_no_null_models
df_no_null_models = df_messy["model_name"].dropna().reset_index()
print("\nDataFrame without null model names:")
print(df_no_null_models)

# 6. Drop rows where ALL values are missing
#    Store in: df_no_all_nulls
df_no_all_nulls = df_messy.dropna(how="all").reset_index()
print("\nDataFrame without rows where all values are null:")
print(df_no_all_nulls)

# Expected: Cleaned DataFrames with appropriate handling of missing values

# ----------------------------------------------------------------------------
# EXERCISE 2.2: Handling Duplicates
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 2.2: Handling Duplicates")
print("=" * 80)

# Scenario: Removing duplicate entries from model performance data
duplicate_data = {
    "model_name": ["GPT-4", "Claude", "GPT-4", "BERT", "Claude", "T5"],
    "accuracy": [0.92, 0.91, 0.92, 0.78, 0.91, 0.88],
    "latency_ms": [150, 180, 150, 50, 180, 170]
}
df_dup = pd.DataFrame(duplicate_data)

print("Original DataFrame with duplicates:")
print(df_dup)

# TODO: Complete the following operations:

# 1. Check for duplicate rows using .duplicated()
#    Store in: is_duplicate
is_duplicate = df_dup.duplicated()
print("\nDuplicate rows check:")
print(is_duplicate)

# 2. Find and display duplicate rows
#    Store in: duplicate_rows
duplicate_rows = df_dup[df_dup.duplicated()]
print("\nDuplicate rows:")
print(duplicate_rows)

# 3. Remove duplicate rows (keep first occurrence)
#    Store in: df_no_duplicates
df_no_duplicates = df_dup.drop_duplicates()
print("\nDataFrame without duplicates:")
print(df_no_duplicates)

# 4. Remove duplicates based on "model_name" column only
#    Store in: df_unique_models
df_unique_models = df_dup["model_name"].drop_duplicates()
print("\nDataFrame with unique model names:")
print(df_unique_models)

# 5. Remove duplicates, keeping the last occurrence instead of first
#    Store in: df_keep_last
df_keep_last = df_dup.drop_duplicates(keep="first")
print("\nDataFrame with duplicates removed (keep last):")
print(df_keep_last)

# Expected: DataFrames with duplicates removed appropriately

# ----------------------------------------------------------------------------
# EXERCISE 2.3: Data Type Conversions
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 2.3: Data Type Conversions")
print("=" * 80)

# Scenario: Converting data types for proper analysis
type_data = {
    "model_id": ["1", "2", "3", "4", "5"],
    "accuracy": ["0.92", "0.91", "0.85", "0.78", "0.88"],
    "date_created": ["2024-01-01", "2024-01-15", "2024-02-01", "2024-02-15", "2024-03-01"],
    "is_active": ["True", "False", "True", "True", "False"]
}
df_types = None  # TODO: Your code here

print("Original DataFrame with string types:")
print(df_types)
print(f"\nData types:\n{df_types.dtypes}")

# TODO: Complete the following type conversions:

# 1. Convert "model_id" to integer
#    Store in: df_types
# TODO: Your code here

# 2. Convert "accuracy" to float
# TODO: Your code here

# 3. Convert "date_created" to datetime using pd.to_datetime()
# TODO: Your code here

# 4. Convert "is_active" to boolean
#    Hint: You may need to use .map() or .replace()
# TODO: Your code here

print("\nDataFrame after type conversions:")
print(df_types)
print(f"\nNew data types:\n{df_types.dtypes}")

# Expected: All columns with appropriate data types

# ----------------------------------------------------------------------------
# EXERCISE 2.4: String Operations
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 2.4: String Operations")
print("=" * 80)

# Scenario: Cleaning and transforming model name strings
string_data = {
    "model_name": ["GPT-4", "claude-3-opus", "GPT-3.5-turbo", "bert-base-uncased", "llama-2-7b"],
    "version": ["v1.0", "v2.1", "v1.5", "v0.9", "v1.2"]
}
df_str = None  # TODO: Your code here

print("Original DataFrame:")
print(df_str)

# TODO: Complete the following string operations:

# 1. Convert all model names to uppercase
#    Store in: df_str
# TODO: Your code here
print("\nUppercase model names:")
# TODO: Print the result

# 2. Convert all model names to lowercase
# TODO: Your code here
print("\nLowercase model names:")
# TODO: Print the result

# 3. Replace hyphens with underscores in model names
# TODO: Your code here
print("\nModel names with underscores:")
print(df_str[["model_name", "model_name_underscore"]])

# 4. Check which model names contain "GPT"
#    Store in: contains_gpt
contains_gpt = None  # TODO: Your code here
print("\nModels containing 'GPT':")
print(df_str[contains_gpt])

# 5. Extract version numbers from "version" column (e.g., "1.0" from "v1.0")
#    Use: .str.extract() with regex pattern
#    Store in: df_str
# TODO: Extract version numbers using .str.extract()
print("\nExtracted version numbers:")
print(df_str[["version", "version_number"]])

# Expected: Transformed strings with various operations

# ============================================================================
# SECTION 3: DATA TRANSFORMATION
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 3: DATA TRANSFORMATION")
print("=" * 80)

# ----------------------------------------------------------------------------
# EXERCISE 3.1: Sorting Data
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 3.1: Sorting Data")
print("=" * 80)

# Scenario: Sorting models by different performance metrics
sort_data = {
    "model_name": ["GPT-4", "Claude", "GPT-3.5", "BERT", "T5"],
    "accuracy": [0.92, 0.91, 0.88, 0.78, 0.88],
    "latency_ms": [150, 180, 200, 50, 170],
    "cost": [0.03, 0.02, 0.01, 0.005, 0.015]
}
df_sort = None  # TODO: Your code here

print("Original DataFrame:")
print(df_sort)

# TODO: Complete the following sorting operations:

# 1. Sort by accuracy in ascending order
#    Store in: df_sorted_acc_asc
df_sorted_acc_asc = None  # TODO: Your code here
print("\nSorted by accuracy (ascending):")
print(df_sorted_acc_asc)

# 2. Sort by accuracy in descending order
#    Store in: df_sorted_acc_desc
df_sorted_acc_desc = None  # TODO: Your code here
print("\nSorted by accuracy (descending):")
print(df_sorted_acc_desc)

# 3. Sort by accuracy (descending), then by latency (ascending)
#    Store in: df_sorted_multi
df_sorted_multi = None  # TODO: Your code here
print("\nSorted by accuracy (desc) then latency (asc):")
print(df_sorted_multi)

# 4. Sort by index in descending order
#    Store in: df_sorted_idx
df_sorted_idx = None  # TODO: Your code here
print("\nSorted by index (descending):")
print(df_sorted_idx)

# Expected: DataFrames sorted according to specifications

# ----------------------------------------------------------------------------
# EXERCISE 3.2: Grouping and Aggregations
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 3.2: Grouping and Aggregations")
print("=" * 80)

# Scenario: Analyzing model performance by family/category
group_data = {
    "model_family": ["GPT", "GPT", "Claude", "Claude", "BERT", "BERT", "T5", "T5"],
    "model_name": ["GPT-4", "GPT-3.5", "Claude-3", "Claude-2", "BERT-base", "BERT-large", "T5-base", "T5-large"],
    "accuracy": [0.92, 0.88, 0.91, 0.89, 0.78, 0.82, 0.85, 0.87],
    "latency_ms": [150, 200, 180, 190, 50, 60, 100, 120],
    "cost": [0.03, 0.01, 0.02, 0.018, 0.005, 0.006, 0.01, 0.012]
}
df_group = None  # TODO: Your code here

print("Original DataFrame:")
print(df_group)

# TODO: Complete the following grouping operations:

# 1. Group by "model_family" and calculate mean accuracy
#    Store in: family_avg_accuracy
family_avg_accuracy = None  # TODO: Your code here
print("\nAverage accuracy by family:")
print(family_avg_accuracy)

# 2. Group by "model_family" and calculate mean for all numeric columns
#    Store in: family_stats
family_stats = None  # TODO: Your code here
print("\nAverage stats by family:")
print(family_stats)

# 3. Group by "model_family" and calculate multiple aggregations
#    For accuracy: mean, max, min
#    For latency_ms: mean, std
#    Store in: family_agg
family_agg = None  # TODO: Your code here
print("\nMultiple aggregations by family:")
print(family_agg)

# 4. Group by "model_family" and count number of models
#    Store in: family_counts
family_counts = None  # TODO: Your code here
print("\nNumber of models per family:")
print(family_counts)

# 5. Group by "model_family" and find the model with highest accuracy in each
#    Hint: Use .apply() with a lambda function
#    Store in: best_per_family
best_per_family = None  # TODO: Your code here
print("\nBest model per family:")
print(best_per_family[["model_name", "accuracy"]])

# Expected: Various grouped statistics and aggregations

# ----------------------------------------------------------------------------
# EXERCISE 3.3: Pivoting and Reshaping
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 3.3: Pivoting and Reshaping")
print("=" * 80)

# Scenario: Reshaping model performance data for different views
pivot_data = {
    "model": ["GPT-4", "GPT-4", "Claude", "Claude", "BERT", "BERT"],
    "metric": ["accuracy", "latency", "accuracy", "latency", "accuracy", "latency"],
    "value": [0.92, 150, 0.91, 180, 0.78, 50]
}
df_pivot = None  # TODO: Your code here

print("Original DataFrame:")
print(df_pivot)

# TODO: Complete the following reshaping operations:

# 1. Pivot the DataFrame: models as rows, metrics as columns
#    Store in: df_pivoted
df_pivoted = None  # TODO: Your code here
print("\nPivoted DataFrame:")
print(df_pivoted)

# 2. Melt (unpivot) the pivoted DataFrame back to long format
#    Store in: df_melted
df_melted = None  # TODO: Your code here
print("\nMelted DataFrame:")
print(df_melted)

# 3. Create a pivot table with models and datasets
#    First, create a dataset with multiple models and datasets
dataset_data = {
    "model": ["GPT-4", "GPT-4", "Claude", "Claude", "BERT", "BERT"],
    "dataset": ["A", "B", "A", "B", "A", "B"],
    "accuracy": [0.92, 0.88, 0.91, 0.89, 0.78, 0.80]
}
df_datasets = None  # TODO: Your code here
print("\nDataset DataFrame:")
print(df_datasets)

# Create pivot table: models as rows, datasets as columns, accuracy as values
#    Store in: df_dataset_pivot
df_dataset_pivot = None  # TODO: Your code here
print("\nPivot table (models vs datasets):")
print(df_dataset_pivot)

# Expected: Reshaped DataFrames in different formats

# ============================================================================
# SECTION 4: FEATURE ENGINEERING
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 4: FEATURE ENGINEERING")
print("=" * 80)

# ----------------------------------------------------------------------------
# EXERCISE 4.1: Creating New Columns
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 4.1: Creating New Columns")
print("=" * 80)

# Scenario: Creating derived features for model analysis
feature_data = {
    "model": ["GPT-4", "Claude", "GPT-3.5", "BERT", "T5"],
    "accuracy": [0.92, 0.91, 0.88, 0.78, 0.88],
    "latency_ms": [150, 180, 200, 50, 170],
    "cost": [0.03, 0.02, 0.01, 0.005, 0.015]
}
df_features = None  # TODO: Your code here

print("Original DataFrame:")
print(df_features)

# TODO: Complete the following feature engineering tasks:

# 1. Create "cost_efficiency" column: accuracy / cost
#    Store in: df_features
# TODO: Create cost_efficiency column
print("\nDataFrame with cost_efficiency:")
# TODO: Print the result

# 2. Create "speed_score" column: 1000 / latency_ms (higher is faster)
# TODO: Your code here
print("\nDataFrame with speed_score:")
# TODO: Print the result

# 3. Create "performance_score" column: accuracy * speed_score
# TODO: Your code here
print("\nDataFrame with performance_score:")
# TODO: Print the result

# 4. Create "tier" column based on accuracy:
#    "S" if accuracy >= 0.90, "A" if >= 0.85, else "B"
#    Use: .apply() with lambda function
# TODO: Your code here
print("\nDataFrame with tier:")
print(df_features[["model", "accuracy", "tier"]])

# Expected: DataFrame with multiple new feature columns

# ----------------------------------------------------------------------------
# EXERCISE 4.2: Applying Functions
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 4.2: Applying Functions")
print("=" * 80)

# Scenario: Applying custom functions to transform data
apply_data = {
    "model": ["GPT-4", "Claude", "GPT-3.5", "BERT"],
    "accuracy": [0.92, 0.91, 0.88, 0.78],
    "latency_ms": [150, 180, 200, 50]
}
df_apply = None  # TODO: Your code here

print("Original DataFrame:")
print(df_apply)

# TODO: Complete the following function applications:

# 1. Apply a function to format accuracy as percentage string
#    Format: "92.0%"
#    Store in: df_apply
# TODO: Format accuracy as percentage
print("\nAccuracy as percentage:")
# TODO: Print the result

# 2. Apply a function to each row to calculate a composite score
#    Formula: (accuracy * 100) - (latency_ms / 10)
#    Store in: df_apply
# TODO: Define the function and apply it
print("\nComposite score:")
# TODO: Print the result

# 3. Map accuracy values to letter grades using .map()
#    Mapping: {0.92: "A+", 0.91: "A", 0.88: "B+", 0.78: "C"}
#    Store in: df_apply
# TODO: Your code here
print("\nGrade mapping:")
print(df_apply[["model", "accuracy", "grade"]])

# 4. Apply a function to each column to get summary statistics
#    Calculate mean for accuracy and latency_ms columns
#    Store in: column_means
column_means = None  # TODO: Your code here
print("\nColumn means:")
print(column_means)

# Expected: DataFrame with transformed values using various apply methods

# ----------------------------------------------------------------------------
# EXERCISE 4.3: Binning and Discretization
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 4.3: Binning and Discretization")
print("=" * 80)

# Scenario: Creating categorical features from continuous variables
bin_data = {
    "model": ["GPT-4", "Claude", "GPT-3.5", "BERT", "T5", "Llama-2"],
    "accuracy": [0.92, 0.91, 0.88, 0.78, 0.88, 0.85],
    "latency_ms": [150, 180, 200, 50, 170, 250]
}
df_bin = None  # TODO: Your code here

print("Original DataFrame:")
print(df_bin)

# TODO: Complete the following binning operations:

# 1. Bin accuracy into 3 equal-width bins: "Low", "Medium", "High"
#    Use: pd.cut()
#    Store in: df_bin
# TODO: Bin accuracy using pd.cut()
print("\nAccuracy bins (equal-width):")
# TODO: Print the result

# 2. Bin latency into 3 equal-frequency bins: "Fast", "Medium", "Slow"
#    Use: pd.qcut()
#    Store in: df_bin
# TODO: Your code here
print("\nLatency bins (equal-frequency):")
# TODO: Print the result

# 3. Create custom bins for accuracy: [0, 0.80, 0.85, 0.90, 1.0]
#    Labels: ["Poor", "Fair", "Good", "Excellent"]
#    Store in: df_bin
# TODO: Your code here
print("\nCustom accuracy categories:")
print(df_bin[["model", "accuracy", "accuracy_category"]])

# Expected: DataFrame with binned categorical features

# ----------------------------------------------------------------------------
# EXERCISE 4.4: One-Hot Encoding
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 4.4: One-Hot Encoding")
print("=" * 80)

# Scenario: Encoding categorical variables for machine learning
encode_data = {
    "model": ["GPT-4", "Claude", "GPT-3.5", "BERT", "T5"],
    "model_type": ["LLM", "LLM", "LLM", "Encoder", "Encoder"],
    "accuracy": [0.92, 0.91, 0.88, 0.78, 0.88]
}
df_encode = None  # TODO: Your code here

print("Original DataFrame:")
print(df_encode)

# TODO: Complete the following encoding operations:

# 1. One-hot encode the "model_type" column
#    Use: pd.get_dummies()
#    Store in: df_encoded
df_encoded = None  # TODO: Your code here
print("\nOne-hot encoded DataFrame:")
print(df_encoded)

# 2. One-hot encode "model_type" but keep original column
#    Use: pd.get_dummies() with drop_first=False
df_encoded_full = None  # TODO: Your code here
print("\nOne-hot encoded (keeping all):")
print(df_encoded_full)

# Expected: DataFrames with one-hot encoded categorical variables

# ============================================================================
# SECTION 5: EXPLORATORY DATA ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 5: EXPLORATORY DATA ANALYSIS")
print("=" * 80)

# ----------------------------------------------------------------------------
# EXERCISE 5.1: Statistical Analysis
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 5.1: Statistical Analysis")
print("=" * 80)

# Scenario: Comprehensive statistical analysis of model performance
eda_data = {
    "model": ["GPT-4", "Claude", "GPT-3.5", "BERT", "T5", "Llama-2", "Mistral"],
    "accuracy": [0.92, 0.91, 0.88, 0.78, 0.88, 0.85, 0.87],
    "latency_ms": [150, 180, 200, 50, 170, 250, 170],
    "cost": [0.03, 0.02, 0.01, 0.005, 0.015, 0.008, 0.012]
}
df_eda = None  # TODO: Your code here

print("Original DataFrame:")
print(df_eda)

# TODO: Complete the following statistical analyses:

# 1. Get comprehensive statistical summary using .describe()
#    Store in: stats_summary
stats_summary = None  # TODO: Your code here
print("\nStatistical summary:")
print(stats_summary)

# 2. Calculate mean, median, and std for accuracy
#    Store in: accuracy_stats
accuracy_stats = None  # TODO: Your code here
print("\nAccuracy statistics:")
print(accuracy_stats)

# 3. Calculate correlation matrix for numeric columns
#    Store in: correlation_matrix
correlation_matrix = None  # TODO: Your code here
print("\nCorrelation matrix:")
print(correlation_matrix)

# 4. Calculate correlation between accuracy and latency
#    Store in: acc_lat_corr
acc_lat_corr = None  # TODO: Your code here
print(f"\nAccuracy-Latency correlation: {acc_lat_corr:.4f}")

# 5. Find models with accuracy above the mean
#    Store in: above_mean_models
mean_accuracy = None  # TODO: Your code here
above_mean_models = None  # TODO: Your code here
print("\nModels with accuracy above mean:")
print(above_mean_models[["model", "accuracy"]])

# Expected: Various statistical insights and correlations

# ----------------------------------------------------------------------------
# EXERCISE 5.2: Value Counts and Frequency Analysis
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 5.2: Value Counts and Frequency Analysis")
print("=" * 80)

# Scenario: Analyzing frequency distributions
count_data = {
    "model": ["GPT-4", "Claude", "GPT-4", "BERT", "Claude", "GPT-4", "T5", "GPT-4"],
    "status": ["active", "active", "active", "inactive", "active", "active", "inactive", "active"],
    "tier": ["S", "S", "S", "B", "S", "S", "A", "S"]
}
df_counts = None  # TODO: Your code here

print("Original DataFrame:")
print(df_counts)

# TODO: Complete the following frequency analyses:

# 1. Count occurrences of each model
#    Store in: model_counts
model_counts = None  # TODO: Your code here
print("\nModel counts:")
print(model_counts)

# 2. Count occurrences with percentages
#    Store in: model_counts_pct
model_counts_pct = None  # TODO: Your code here
print("\nModel counts (percentages):")
print(model_counts_pct)

# 3. Count occurrences sorted by index (alphabetically)
#    Store in: model_counts_sorted
model_counts_sorted = None  # TODO: Your code here
print("\nModel counts (sorted by name):")
print(model_counts_sorted)

# 4. Create cross-tabulation of model vs status
#    Store in: model_status_ct
model_status_ct = None  # TODO: Your code here
print("\nModel-Status cross-tabulation:")
print(model_status_ct)

# 5. Create cross-tabulation with percentages
#    Store in: model_status_ct_pct
model_status_ct_pct = None  # TODO: Your code here
print("\nModel-Status cross-tabulation (percentages):")
print(model_status_ct_pct)

# Expected: Various frequency distributions and cross-tabulations

# ----------------------------------------------------------------------------
# EXERCISE 5.3: Advanced Aggregations
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 5.3: Advanced Aggregations")
print("=" * 80)

# Scenario: Complex aggregations for model analysis
agg_data = {
    "model_family": ["GPT", "GPT", "Claude", "Claude", "BERT", "BERT"],
    "model": ["GPT-4", "GPT-3.5", "Claude-3", "Claude-2", "BERT-base", "BERT-large"],
    "accuracy": [0.92, 0.88, 0.91, 0.89, 0.78, 0.82],
    "latency_ms": [150, 200, 180, 190, 50, 60],
    "cost": [0.03, 0.01, 0.02, 0.018, 0.005, 0.006]
}
df_agg = None  # TODO: Your code here

print("Original DataFrame:")
print(df_agg)

# TODO: Complete the following aggregation operations:

# 1. Group by model_family and calculate mean for all numeric columns
#    Store in: family_means
family_means = None  # TODO: Your code here
print("\nMean values by family:")
print(family_means)

# 2. Group by model_family and calculate multiple statistics
#    For accuracy: mean, max, min, std
#    Store in: family_accuracy_stats
family_accuracy_stats = None  # TODO: Your code here
print("\nAccuracy statistics by family:")
print(family_accuracy_stats)

# 3. Group by model_family and calculate custom aggregations
#    Calculate range (max - min) for accuracy
#    Store in: family_accuracy_range
family_accuracy_range = None  # TODO: Your code here
print("\nAccuracy range by family:")
print(family_accuracy_range)

# 4. Calculate sum of all numeric columns
#    Store in: total_sum
total_sum = None  # TODO: Your code here
print("\nSum of numeric columns:")
print(total_sum)

# 5. Calculate multiple aggregations at once using .agg()
#    For accuracy: mean, max
#    For latency_ms: mean, min
#    For cost: sum
#    Store in: multi_agg
multi_agg = None  # TODO: Your code here
print("\nMultiple aggregations:")
print(multi_agg)

# Expected: Various aggregated statistics

# ============================================================================
# SECTION 6: ADVANCED OPERATIONS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 6: ADVANCED OPERATIONS")
print("=" * 80)

# ----------------------------------------------------------------------------
# EXERCISE 6.1: Merging DataFrames
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 6.1: Merging DataFrames")
print("=" * 80)

# Scenario: Combining data from multiple sources
df_performance = pd.DataFrame({
    "model": ["GPT-4", "Claude", "BERT", "T5"],
    "accuracy": [0.92, 0.91, 0.78, 0.88]
})

df_latency = pd.DataFrame({
    "model": ["GPT-4", "Claude", "GPT-3.5", "BERT"],
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

# TODO: Complete the following merge operations:

# 1. Inner join: Merge df_performance and df_latency on "model"
#    Store in: df_inner
df_inner = None  # TODO: Your code here
print("\nInner join (performance + latency):")
print(df_inner)

# 2. Left join: Merge df_performance and df_latency on "model"
#    Store in: df_left
df_left = None  # TODO: Your code here
print("\nLeft join (performance + latency):")
print(df_left)

# 3. Outer join: Merge df_performance and df_latency on "model"
#    Store in: df_outer
df_outer = None  # TODO: Your code here
print("\nOuter join (performance + latency):")
print(df_outer)

# 4. Merge all three DataFrames: Start with df_performance, add df_latency, then df_cost
#    Use left joins to preserve all models from df_performance
#    Store in: df_combined
df_combined = None  # TODO: Your code here
df_combined = None  # TODO: Your code here
print("\nCombined DataFrame (all three):")
print(df_combined)

# Expected: Merged DataFrames with different join types

# ----------------------------------------------------------------------------
# EXERCISE 6.2: Concatenation
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 6.2: Concatenation")
print("=" * 80)

# Scenario: Combining DataFrames vertically and horizontally
df_a = pd.DataFrame({
    "model": ["GPT-4", "Claude"],
    "accuracy": [0.92, 0.91]
})

df_b = pd.DataFrame({
    "model": ["BERT", "T5"],
    "accuracy": [0.78, 0.88]
})

df_c = pd.DataFrame({
    "latency_ms": [150, 180, 50, 170]
})

print("DataFrame A:")
print(df_a)
print("\nDataFrame B:")
print(df_b)
print("\nDataFrame C:")
print(df_c)

# TODO: Complete the following concatenation operations:

# 1. Concatenate df_a and df_b vertically
#    Use: pd.concat() with ignore_index=True
#    Store in: df_concat_vertical
df_concat_vertical = None  # TODO: Your code here
print("\nVertical concatenation (A + B):")
print(df_concat_vertical)

# 2. Concatenate df_a and df_c horizontally
#    Use: pd.concat() with axis=1
#    Store in: df_concat_horizontal
df_concat_horizontal = None  # TODO: Your code here
print("\nHorizontal concatenation (A + C):")
print(df_concat_horizontal)

# 3. Concatenate multiple DataFrames vertically
#    Create df_d with more models and concatenate all
df_d = pd.DataFrame({
    "model": ["Llama-2", "Mistral"],
    "accuracy": [0.85, 0.87]
})
df_all_models = None  # TODO: Your code here
print("\nAll models concatenated:")
print(df_all_models)

# Expected: Concatenated DataFrames in different orientations

# ----------------------------------------------------------------------------
# EXERCISE 6.3: Time Series Operations
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 6.3: Time Series Operations")
print("=" * 80)

# Scenario: Analyzing time series data for model usage
# Create time series data
dates = pd.date_range("2024-01-01", periods=10, freq="D")
ts_data = {
    "date": dates,
    "model_requests": np.random.randint(100, 1000, 10),
    "accuracy": np.random.uniform(0.85, 0.95, 10)
}
df_ts = None  # TODO: Your code here

print("Time Series DataFrame:")
print(df_ts)

# TODO: Complete the following time series operations:

# 1. Set "date" as the index
#    Store in: df_ts_indexed
df_ts_indexed = None  # TODO: Your code here
print("\nDataFrame with date as index:")
print(df_ts_indexed.head())

# 2. Resample to weekly data and calculate mean
#    Store in: df_weekly
df_weekly = None  # TODO: Your code here
print("\nWeekly resampled data (mean):")
print(df_weekly)

# 3. Reset index to get date back as a column
#    Store in: df_ts_reset
df_ts_reset = None  # TODO: Your code here
print("\nDataFrame with reset index:")
print(df_ts_reset.head())

# 4. Extract date components: year, month, day_of_week
#    Use: .dt accessor
#    Store in: df_ts_reset
# TODO: Extract date components using .dt accessor
print("\nDataFrame with date components:")
print(df_ts_reset[["date", "year", "month", "day_of_week"]].head())

# 5. Filter data for a specific date range
#    Filter dates between 2024-01-03 and 2024-01-07
#    Store in: df_filtered_dates
df_ts_indexed_filtered = None  # TODO: Your code here
df_filtered_dates = None  # TODO: Your code here
print("\nFiltered dates (2024-01-03 to 2024-01-07):")
print(df_filtered_dates)

# Expected: Time series operations with date indexing and resampling

# ----------------------------------------------------------------------------
# EXERCISE 6.4: Multi-Index DataFrames
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 6.4: Multi-Index DataFrames")
print("=" * 80)

# Scenario: Working with hierarchical index structures
multi_data = {
    "model": ["GPT-4", "GPT-4", "Claude", "Claude", "BERT", "BERT"],
    "dataset": ["A", "B", "A", "B", "A", "B"],
    "accuracy": [0.92, 0.88, 0.91, 0.89, 0.78, 0.80],
    "latency_ms": [150, 145, 180, 175, 50, 55]
}
df_multi = None  # TODO: Your code here

print("Original DataFrame:")
print(df_multi)

# TODO: Complete the following multi-index operations:

# 1. Create a multi-index from "model" and "dataset" columns
#    Set these as the index
#    Store in: df_multi_indexed
df_multi_indexed = None  # TODO: Your code here
print("\nMulti-index DataFrame:")
print(df_multi_indexed)

# 2. Access data by first level index (model)
#    Get all data for "GPT-4"
#    Store in: gpt4_data
gpt4_data = None  # TODO: Your code here
print("\nGPT-4 data:")
print(gpt4_data)

# 3. Access data by both levels (model and dataset)
#    Get data for ("GPT-4", "A")
#    Store in: gpt4_dataset_a
gpt4_dataset_a = None  # TODO: Your code here
print("\nGPT-4, Dataset A:")
print(gpt4_dataset_a)

# 4. Reset index to convert back to regular columns
#    Store in: df_multi_reset
df_multi_reset = None  # TODO: Your code here
print("\nReset multi-index:")
print(df_multi_reset)

# 5. Group by first level of multi-index and calculate mean
#    Store in: model_means
model_means = None  # TODO: Your code here
print("\nMean by model (first level):")
print(model_means)

# Expected: Multi-index operations with hierarchical data access

# ----------------------------------------------------------------------------
# EXERCISE 6.5: Complex Real-World Scenario
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("EXERCISE 6.5: Complex Real-World Scenario")
print("=" * 80)

# Scenario: Complete data pipeline - cleaning, transforming, and analyzing
# This exercise combines multiple concepts

raw_data = {
    "model_id": ["1", "2", "3", "4", "5", "6"],
    "model_name": ["GPT-4", "Claude", None, "BERT", "GPT-4", "T5"],
    "accuracy": ["0.92", "0.91", "0.85", None, "0.92", "0.88"],
    "latency": [150, 180, None, 50, 150, None],
    "cost": [0.03, 0.02, 0.01, None, 0.03, 0.015],
    "date": ["2024-01-01", "2024-01-15", "2024-02-01", "2024-02-15", "2024-03-01", "2024-03-15"]
}
df_complex = None  # TODO: Your code here

print("Raw messy DataFrame:")
print(df_complex)

# TODO: Complete the following comprehensive data pipeline:

# 1. Clean the data:
#    - Convert accuracy to float (handle string values)
#    - Fill missing accuracy with mean
#    - Fill missing latency with 0
#    - Drop rows where model_name is missing
#    - Remove duplicates
#    Store in: df_cleaned
df_cleaned = None  # TODO: Your code here
# TODO: Convert accuracy to float, fill missing values, drop rows, remove duplicates
print("\nCleaned DataFrame:")
print(df_cleaned)

# 2. Create new features:
#    - cost_efficiency: accuracy / cost
#    - performance_tier: "High" if accuracy >= 0.90, else "Medium"
#    - Convert date to datetime
#    Store in: df_cleaned
# TODO: Create cost_efficiency, performance_tier columns, and convert date to datetime
print("\nDataFrame with new features:")
print(df_cleaned)

# 3. Group by model_name and calculate statistics:
#    - Mean accuracy
#    - Mean latency
#    - Count of records
#    Store in: model_stats
model_stats = None  # TODO: Your code here
print("\nModel statistics:")
print(model_stats)

# 4. Find the best model (highest mean accuracy)
#    Store in: best_model_name
best_model_name = None  # TODO: Your code here
print(f"\nBest model: {best_model_name}")

# 5. Create a pivot table: model_name vs performance_tier
#    Count occurrences
#    Store in: pivot_table
pivot_table = None  # TODO: Your code here
print("\nPivot table (model vs tier):")
print(pivot_table)

# Expected: Complete data pipeline with cleaning, feature engineering, and analysis

print("\n" + "=" * 80)
print("ALL EXERCISES COMPLETE!")
print("=" * 80)
print("\nCongratulations! You've practiced:")
print("✓ Core DataFrame operations")
print("✓ Data cleaning and preprocessing")
print("✓ Data transformation")
print("✓ Feature engineering")
print("✓ Exploratory data analysis")
print("✓ Advanced operations (merging, time series, multi-index)")
print("\nKeep practicing to master pandas for AI engineering!")

