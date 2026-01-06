import pandas as pd

# Creating a simple dataset (Dictionary of Lists)
data = {
    "Agent_Name": ["DataBot", "ChatterBox", "GPT-Zero"],
    "Version": [1.0, 2.5, 4.0],
    "Status": ["Active", "Inactive", "Active"]
}

# Converting it into a DataFrame (A programmable Excel sheet)
df = pd.DataFrMame(data)

print("--- AI Agent Report ---")
print(df)


model_data = {
    "model_name": ["GPT-4", "Claude-3", "GPT-3.5", "Llama-2", "Mistral"],
    "accuracy": [None, 0.91, 0.88, 0.85, 0.87],
    "latency_ms": [150, 180, 200, 250, 170],
    "tokens_per_second": [66.7, 55.6, 50.0, 40.0, 58.8]
}

df = pd.DataFrame(model_data)

# two first rows
df.head(2)
# last 2 rows
df.tail(2)
# table resolution (rows, columns)
df.shape
# column names as list
df.columns.tolist()
# column data types
df.dtypes
# general health check overview of the table
df.info()
# Get column data
df["accuracy"]
# Get 2 columns datad
df[["model_name", "latency_ms"]]
# Get row according to index (position based). pull data from column as well
df.iloc[0:2, 1:3]
# Get row according to label (label based).
df.loc[2]
df["model_name"].loc[3]
# Get index of min or max value in column (number only)
index = df["latency_ms"].idxmax()
# use index to access the row data
df.loc[index]
# Boolean filtering. filter rows by a boolean Series mask
df[df["accuracy"]> 0.85]
# Filtering by combine masks (&, |, ~)
df[(df["accuracy"] > 0.8) & (df["latency_ms"] < 200)]
# Check string values using str, and apply mask to df
mask = df["model_name"].str.contains("GPT")
df[mask]
# summary test for numeric columns (mean, std..)
df.describe()
# common aggregations, used when need to fill missing values
df["accuracy"].median()
# Locate missing values 
df.isna()
# Detect rows with any missing values
df.isna().any(axis=1)
# How many None values found in each row
df.isna().sum(axis=1)
# Makes a copy of a table
df.copy()
# Filling missing values (can use any value or mean or median of a column)
df["accuracy"].fillna(df["accuracy"].median())
# Remove row with missing values
df.dropna()
# Remove a row when all values are missing
df.dropna(how="all")
# Rebuild index ordering (after dropping rows mostly)
df.reset_index()
# Detect duplicated rows
df.duplicated()
# Show which rows will be removed
df[df.duplicated()]
# Remove duplicates
df.drop_duplicates() 
df.drop_duplicates(keep="first") 
