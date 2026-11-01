# Ecommerce Customer Analytics - EDA Analysis
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data
file_path = "../data/raw/ecommerce_data.csv"
# Try processed if available
try:
    df = pd.read_csv("../data/processed/cleaned_ecommerce.csv")
except:
    df = pd.read_csv(file_path)

print(f"Dataset Shape: {df.shape}")
print(df.head())
print(df.info())

# Clean Date
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['Month'] = df['Order_Date'].dt.to_period('M')

# 1. Monthly Sales Trend
monthly_sales = df.groupby('Month')['Total_Amount'].sum()
plt.figure(figsize=(12,6))
monthly_sales.plot(kind='line', marker='o')
plt.title('Monthly Sales Trend')
plt.ylabel('Total Sales')
plt.grid(True)
plt.show()

# 2. Top 10 Cities by Revenue
city_revenue = df.groupby('City')['Total_Amount'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=city_revenue.values, y=city_revenue.index)
plt.title('Top 10 Cities by Revenue')
plt.show()

# 3. Age Distribution
plt.figure(figsize=(8,5))
sns.histplot(df['Age'], kde=True, bins=20)
plt.title('Customer Age Distribution')
plt.show()

# 4. Payment Method
payment_counts = df['Payment_Method'].value_counts()
plt.figure(figsize=(6,6))
plt.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%')
plt.title('Payment Method Share')
plt.show()

print("EDA Completed Successfully!")
