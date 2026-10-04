import pandas as pd

FILE = "dataset/processed/labeled_metrics.csv"

df = pd.read_csv(FILE)

print("\n=== DATASET SHAPE ===")
print(df.shape)

print("\n=== COLUMNS ===")
print(df.columns.tolist())

print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

print("\n=== DUPLICATE ROWS ===")
print(df.duplicated().sum())

print("\n=== LABEL DISTRIBUTION ===")
print(df["label"].value_counts())

print("\n=== NUMERICAL STATISTICS ===")
print(df.drop(columns=["timestamp"]).describe())

print("\n=== ANOMALY SAMPLES ===")
print(df[df["label"] == 1].to_string(index=False))
