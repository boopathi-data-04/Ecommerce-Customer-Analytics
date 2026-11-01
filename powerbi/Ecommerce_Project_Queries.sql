USE ecommerce_customer_analytics;

-- 1. TOTAL ROWS - 138116
SELECT COUNT(*) AS total_rows FROM cleaned_ecommerce_150k;

-- 2. SAMPLE DATA
SELECT * FROM cleaned_ecommerce_150k LIMIT 5;

-- 3. TOTAL REVENUE & AOV - WORKING
SELECT 
  SUM(gross_sales) AS total_revenue,
  AVG(gross_sales) AS avg_order_value,
  COUNT(*) AS total_orders
FROM cleaned_ecommerce_150k;

-- 4. SALES CHANNEL WISE - YOUR PHOTO SUCCESS
SELECT 
  sales_channel, 
  SUM(gross_sales) AS revenue,
  COUNT(*) AS orders
FROM cleaned_ecommerce_150k
GROUP BY sales_channel
ORDER BY revenue DESC;

-- 5. MONTHLY TREND - 60 ROWS SUCCESS IN YOUR PHOTO
SELECT 
  YEAR(order_date) AS order_year,
  MONTH(order_date) AS order_month,
  SUM(gross_sales) AS monthly_revenue
FROM cleaned_ecommerce_150k
GROUP BY order_year, order_month
ORDER BY order_year, order_month;

-- 6. TOP 10 CUSTOMERS - CUST-017251 SUCCESS
SELECT 
  customer_id,
  customer_name,
  SUM(gross_sales) AS total_spent
FROM cleaned_ecommerce_150k
GROUP BY customer_id, customer_name
ORDER BY total_spent DESC
LIMIT 10;

-- 7. TOP CUSTOMERS FULL DETAILS - WORKING
SELECT 
  customer_id,
  customer_name,
  SUM(gross_sales) AS total_value,
  COUNT(*) AS total_orders
FROM cleaned_ecommerce_150k
GROUP BY customer_id, customer_name
ORDER BY total_value DESC
LIMIT 15;

-- 8. DAILY REVENUE LAST 20 DAYS
SELECT 
  order_date,
  SUM(gross_sales) AS daily_revenue,
  COUNT(*) AS daily_orders
FROM cleaned_ecommerce_150k
GROUP BY order_date
ORDER BY order_date DESC
LIMIT 20;

-- 9. YEARLY GROWTH
SELECT 
  YEAR(order_date) AS yr,
  SUM(gross_sales) AS yearly_revenue,
  COUNT(*) AS yearly_orders
FROM cleaned_ecommerce_150k
GROUP BY yr
ORDER BY yr;

-- 10. HIGH VALUE CUSTOMERS > 5000
SELECT 
  customer_id,
  customer_name,
  SUM(gross_sales) AS total_value
FROM cleaned_ecommerce_150k
GROUP BY customer_id, customer_name
HAVING total_value > 5000
ORDER BY total_value DESC
LIMIT 20;