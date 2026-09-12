import pandas as pd

df = pd.read_csv("spotify_artist_streaming_2020_2025.csv")

#print(df.shape)        # (rows, columns)
#print(df.columns)      # column names
#print(df.head())       # first 5 rows
#print(df.dtypes)       # data type of each column

def detect_column_types(df):
    text_cols, numeric_cols, categorical_cols = [], [], []
    for col in df.columns:
        if df[col].dtype in ('object', 'str'):
            sample = df[col].dropna().astype(str)
            avg_words = sample.str.split().str.len().mean()
            if avg_words >= 4:  # real sentences have multiple words
                text_cols.append(col)
            else:
                categorical_cols.append(col)
        elif df[col].dtype == 'bool':
            categorical_cols.append(col)
        else:
            numeric_cols.append(col)
    return text_cols, numeric_cols, categorical_cols

text_cols, numeric_cols, categorical_cols = detect_column_types(df)
#print("TEXT:", text_cols)
#print("NUMERIC:", numeric_cols)
#print("CATEGORICAL:", categorical_cols)

import matplotlib.pyplot as plt

def plot_column(df, col, col_type):
    if col_type == "categorical":
        df[col].value_counts().plot(kind="bar")
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Count")
    elif col_type == "numeric":
        df[col].plot(kind="hist", bins=30)
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

def plot_all_columns(df, numeric_cols, categorical_cols, max_charts=5):
    count = 0
    for col in numeric_cols[:3]:  # cap numeric at 3
        if count >= max_charts:
            break
        plot_column(df, col, "numeric")
        count += 1

    for col in categorical_cols:
        if count >= max_charts:
            break
        if df[col].nunique() > 20:
            print(f"Skipping '{col}' — too many unique values ({df[col].nunique()})")
            continue
        plot_column(df, col, "categorical")
        count += 1


plot_all_columns(df, numeric_cols, categorical_cols, max_charts=5)