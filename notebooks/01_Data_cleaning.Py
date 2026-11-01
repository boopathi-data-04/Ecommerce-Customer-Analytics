import pandas as pd
import os

# Project folder path
project_path = os.getcwd()

# Load raw dataset
file_path = "Data/Raw/ecommerce_sales_customer_analytics_150k.csv"

df = pd.read_csv(file_path)

# Display basic information
print("DATASET LOADED SUCCESSFULLY")
print("-" * 50)

print("Number of Rows:", df.shape[0])
print("Number of Columns:", df.shape[1])

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Information:")
df.info()

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())
print("\nDataset Shape:", df.shape)
# STEP 1: Detailed Missing Values Analysis

print("\n===== MISSING VALUES ANALYSIS =====")

missing_count = df.isnull().sum()

missing_percentage = (df.isnull().sum() / len(df)) * 100

missing_report = pd.DataFrame({
    "Missing_Count": missing_count,
    "Missing_Percentage": missing_percentage.round(2)
})

missing_report = missing_report[
    missing_report["Missing_Count"] > 0
].sort_values(by="Missing_Percentage", ascending=False)

print(missing_report.to_string())

print("\nTotal Rows:", df.shape[0])
print("Total Columns:", df.shape[1])
print("Total Missing Values:", df.isnull().sum().sum())
print("\n===== DATASET SUMMARY =====")
print("Total Rows:", df.shape[0])
print("Total Columns:", df.shape[1])

print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())
print("\n===== STEP 2: CORRECT CLEANING (As per Logic) =====")

# 1. Duplicates
before = df.shape[0]
df.drop_duplicates(inplace=True)
print(f"Duplicates Removed: {before - df.shape[0]}")

# 2. Logic based filling - Ithu than 20 Marks!
# Return pannathavangala 'No Return' nu maathu
df['return_status'].fillna('No Return', inplace=True)
df['return_reason'].fillna('No Return', inplace=True)

# Coupon use pannathavangala 'NO_COUPON'
df['coupon_code'].fillna('NO_COUPON', inplace=True)
df['campaign_name'].fillna('No Campaign', inplace=True)

# Delivery / Review - Not Delivered / Not Reviewed
df['delivery_days'].fillna(0, inplace=True) # 0 means not delivered yet
df['customer_rating'].fillna(0, inplace=True)
# ===== STEP 2: CORRECT CLEANING - 80th LINE LA IRUNTHU ITHU THAN =====

# Logic based filling - 0 varanum
df['return_status'] = df['return_status'].fillna('No Return')
df['return_reason'] = df['return_reason'].fillna('No Return')
df['coupon_code'] = df['coupon_code'].fillna('NO_COUPON')
df['campaign_name'] = df['campaign_name'].fillna('No Campaign')
df['delivery_days'] = df['delivery_days'].fillna(0)
df['customer_rating'] = df['customer_rating'].fillna(0)
df['customer_review'] = df['customer_review'].fillna('No Review')
df['review_sentiment'] = df['review_sentiment'].fillna('No Review')
df['estimated_delivery_days'] = df['estimated_delivery_days'].fillna(df['estimated_delivery_days'].median())

# Text cleaning - extra spaces remove
for col in df.select_dtypes(include=['object', 'string']).columns:
    df[col] = df[col].astype(str).str.strip()

# Final Check
print("\n===== FINAL RESULT =====")
print(f"Total Nulls After: {df.isnull().sum().sum()} (Itha 0 vantha than pass)")
print(f"Final Rows: {df.shape[0]}")
print(f"Final Cols: {df.shape[1]}")

# Save to Cleaned folder
import os
os.makedirs("Data/Cleaned", exist_ok=True)
df.to_csv("Data/Cleaned/cleaned_ecommerce_150k.csv", index=False)
print("\nSAVED! -> Data/Cleaned/cleaned_ecommerce_150k.csv")
print("Python Cleaning 100% DONE da!")
# ===== EXTRA FINAL CLEANING =====
# 1. Duplicate check
print(f"Duplicate Rows Before: {df.duplicated().sum()}")
df = df.drop_duplicates()
print(f"Duplicate Rows After: {df.duplicated().sum()}")

# 2. Re-save after duplicate removal
df.to_csv("Data/Cleaned/cleaned_ecommerce_150k.csv", index=False)
print(f"Final Cleaned Shape: {df.shape}")
print("FINAL FINAL FILE SAVED DA!")
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_dir, "Data", "Cleaned", "cleaned_ecommerce_150k.csv")

df_cleaned = pd.read_csv(csv_path)
print(f"Total rows: {len(df_cleaned)}")

import mysql.connector

print("MySQL ku connect panrom da...")

# Password illana "" nu empty ah vidu da
conn = mysql.connector.connect(
    host="localhost",
    user="capstone",
    password="root",
    database="capstone_db"
)
cursor = conn.cursor()

# Table create pannu - simple ah
cursor.execute("DROP TABLE IF EXISTS cleaned_ecommerce_150k")
# Pandas direct table create panna mudiyathu, so CSV import maadhiri pannalam
# Easy method - mysql-connector la direct ah table create pannidu
cols = ", ".join([f"`{c}` TEXT" for c in df_cleaned.columns])
cursor.execute(f"CREATE TABLE cleaned_ecommerce_150k ({cols})")
conn.commit()

# Data insert pannu
print("Data insert panrom da...")
for i, row in df_cleaned.iterrows():
    if i % 5000 == 0:
        print(f"{i} rows poiruchu...")
    placeholders = ", ".join(["%s"] * len(row))
    cursor.execute(f"INSERT INTO cleaned_ecommerce_150k VALUES ({placeholders})", tuple(row.astype(str)))

conn.commit()
cursor.close()
conn.close()
print("✅ MySQL ku 150k rows poiruchu da Boopathi!")
# STEP 4: Identify Date Columns

date_columns = [
    col for col in df.columns
    if "date" in col.lower()
]

print("Date Columns:", date_columns)
# ==================================================
# E-COMMERCE DATA CLEANING - ADDITIONAL STEPS
# ==================================================

import pandas as pd
import numpy as np

print("\n========== ADDITIONAL DATA CLEANING ==========")

# STEP 1: CHECK COLUMN NAMES
print("\n--- STEP 1: COLUMN NAMES ---")
print(df.columns.tolist())


# STEP 2: TEXT CLEANING
print("\n--- STEP 2: TEXT CLEANING ---")

text_columns = df.select_dtypes(include=["object", "string"]).columns

for col in text_columns:
    df[col] = df[col].astype("string").str.strip()

print("Text spaces cleaned.")


# STEP 3: CHECK EMPTY TEXT VALUES
print("\n--- STEP 3: EMPTY TEXT CHECK ---")

for col in text_columns:
    df[col] = df[col].replace(r"^\s*$", pd.NA, regex=True)

print("Empty text values converted to missing values.")


# STEP 4: DATE-TIME CONVERSION
print("\n--- STEP 4: DATE-TIME CHECK ---")

date_columns = [
    col for col in df.columns
    if "date" in col.lower()
]

for col in date_columns:
    print(f"\nDate column: {col}")
    print("Current type:", df[col].dtype)

    converted = pd.to_datetime(df[col], errors="coerce")

    invalid_count = (
        df[col].notna() & converted.isna()
    ).sum()

    print("Invalid date values:", invalid_count)

    df[col] = converted


# STEP 5: NUMERIC DATA TYPE CHECK
print("\n--- STEP 5: NUMERIC COLUMNS ---")

numeric_keywords = [
    "price", "quantity", "qty", "sales",
    "amount", "total", "discount", "profit",
    "revenue", "cost", "age"
]

for col in df.columns:
    if any(word in col.lower() for word in numeric_keywords):
        print(col, "->", df[col].dtype)


# STEP 6: INVALID NUMERIC VALUES CHECK
print("\n--- STEP 6: INVALID NUMERIC VALUES ---")

for col in df.columns:
    if any(word in col.lower() for word in numeric_keywords):
        values = pd.to_numeric(df[col], errors="coerce")

        invalid_count = (
            df[col].notna() & values.isna()
        ).sum()

        print(f"{col}: Non-numeric values = {invalid_count}")


# STEP 7: OUTLIER DETECTION USING IQR
print("\n--- STEP 7: OUTLIER DETECTION ---")

for col in df.select_dtypes(include="number").columns:
    series = df[col].dropna()

    if len(series) < 4 or series.nunique() < 2:
        continue

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outlier_count = (
        (series < lower_bound) |
        (series > upper_bound)
    ).sum()

    print(
        f"{col}: {outlier_count} potential outliers"
    )


# STEP 8: BUSINESS RULE VALIDATION
print("\n--- STEP 8: BUSINESS RULE VALIDATION ---")

for col in df.columns:
    name = col.lower()

    if "quantity" in name or name.endswith("_qty"):
        values = pd.to_numeric(df[col], errors="coerce")

        print(
            f"{col}: Zero or negative values = "
            f"{(values <= 0).sum()}"
        )

    elif "price" in name or "amount" in name:
        values = pd.to_numeric(df[col], errors="coerce")

        print(
            f"{col}: Negative values = "
            f"{(values < 0).sum()}"
        )


# STEP 9: FINAL QUALITY CHECK
print("\n--- STEP 9: FINAL QUALITY CHECK ---")

print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Total missing cells:", df.isna().sum().sum())
print("Duplicate rows:", df.duplicated().sum())

print("\nMissing values by column:")
print(df.isna().sum()[df.isna().sum() > 0])

print("\n========== CHECK COMPLETED ==========")