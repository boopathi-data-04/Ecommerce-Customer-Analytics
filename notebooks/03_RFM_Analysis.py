# RFM Analysis - Customer Segmentation - Ecommerce Capstone
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
try:
    df = pd.read_csv("../data/processed/cleaned_ecommerce.csv")
    print("Loaded cleaned data")
except:
    df = pd.read_csv("../data/raw/ecommerce_data.csv")
    print("Loaded raw data")

df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# Snapshot date = last order date + 1 day
snapshot_date = df['Order_Date'].max() + dt.timedelta(days=1)
print(f"Snapshot Date: {snapshot_date}")

# RFM Calculation
rfm = df.groupby('Customer_ID').agg({
    'Order_Date': lambda x: (snapshot_date - x.max()).days,
    'Order_ID': 'count',
    'Total_Amount': 'sum'
})

rfm.rename(columns={'Order_Date': 'Recency', 'Order_ID': 'Frequency', 'Total_Amount': 'Monetary'}, inplace=True)

# RFM Scores 1-5
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5])

rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# Customer Segments
def rfm_segment(row):
    if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
        return 'Champions'
    elif row['R_Score'] >= 4 and row['F_Score'] >= 3:
        return 'Loyal Customers'
    elif row['R_Score'] >= 4 and row['F_Score'] <= 2:
        return 'New Customers'
    elif row['R_Score'] <= 2 and row['F_Score'] >= 3:
        return 'At Risk'
    elif row['R_Score'] <= 2 and row['F_Score'] <= 2:
        return 'Lost Customers'
    else:
        return 'Potential Loyalist'

rfm['Segment'] = rfm.apply(rfm_segment, axis=1)

# Display results
print(rfm.head(10))
print("\nSegment Count:")
print(rfm['Segment'].value_counts())

# Plot Segments
plt.figure(figsize=(10,5))
sns.countplot(data=rfm, x='Segment', order=rfm['Segment'].value_counts().index)
plt.xticks(rotation=30)
plt.title('Customer Segments - RFM Analysis')
plt.show()

# Save for PowerBI and SQL
rfm.to_csv('../data/processed/rfm_result.csv', index=True)
print("\nRFM Analysis Done! File saved to rfm_result.csv")
