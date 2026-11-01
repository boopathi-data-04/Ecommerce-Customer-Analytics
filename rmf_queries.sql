-- Ecommerce Customer Analytics - SQL Queries

-- 1. Total Revenue & Orders
SELECT COUNT(DISTINCT Order_ID) as total_orders, SUM(Total_Amount) as total_revenue FROM ecommerce_data;

-- 2. Monthly Sales Trend
SELECT 
  DATE_TRUNC('month', Order_Date) as month,
  SUM(Total_Amount) as monthly_sales
FROM ecommerce_data
GROUP BY 1 ORDER BY 1;

-- 3. Top 10 Cities by Revenue
SELECT City, SUM(Total_Amount) as revenue
FROM ecommerce_data
GROUP BY City ORDER BY revenue DESC LIMIT 10;

-- 4. RFM Analysis Query
WITH rfm AS (
  SELECT 
    Customer_ID,
    CURRENT_DATE - MAX(Order_Date) as Recency,
    COUNT(Order_ID) as Frequency,
    SUM(Total_Amount) as Monetary
  FROM ecommerce_data GROUP BY Customer_ID
)
SELECT * FROM rfm;

-- 5. Customer Segmentation
SELECT 
  CASE 
    WHEN Recency < 30 AND Frequency > 5 THEN 'Champions'
    WHEN Recency < 60 THEN 'Loyal'
    WHEN Recency > 180 THEN 'At Risk'
    ELSE 'Others'
  END as segment,
  COUNT(*) FROM rfm GROUP BY 1;
