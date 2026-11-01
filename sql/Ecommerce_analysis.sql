-- ======================================================
-- ECOMMERCE CUSTOMER ANALYTICS - COMPLETE ANALYSIS
-- Author: Boopathi
-- ======================================================

-- 1. TOTAL CUSTOMERS, ORDERS & REVENUE OVERVIEW
SELECT 
    (SELECT COUNT(DISTINCT customer_id) FROM customers) as total_customers,
    (SELECT COUNT(*) FROM orders) as total_orders,
    (SELECT SUM(order_value) FROM orders) as total_revenue;

-- 2. MONTHLY SALES TREND ANALYSIS
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') as month,
    COUNT(*) as total_orders,
    SUM(order_value) as monthly_revenue,
    AVG(order_value) as avg_order_value
FROM orders 
GROUP BY month 
ORDER BY month;

-- 3. TOP 10 HIGH VALUE CUSTOMERS
SELECT 
    c.customer_id, 
    c.customer_name, 
    c.city,
    COUNT(o.order_id) as total_orders,
    SUM(o.order_value) as total_spent
FROM customers c 
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_spent DESC 
LIMIT 10;

-- 4. RFM SEGMENTATION (Recency, Frequency, Monetary)
SELECT 
    customer_id, 
    DATEDIFF(CURDATE(), MAX(order_date)) as recency_days, 
    COUNT(*) as frequency, 
    SUM(order_value) as monetary,
    CASE 
        WHEN DATEDIFF(CURDATE(), MAX(order_date)) < 30 AND COUNT(*) > 10 THEN 'VIP Champions'
        WHEN DATEDIFF(CURDATE(), MAX(order_date)) < 60 AND COUNT(*) > 5 THEN 'Loyal Customers'
        WHEN DATEDIFF(CURDATE(), MAX(order_date)) < 90 THEN 'Potential Loyalist'
        ELSE 'At Risk / Churned'
    END as customer_segment
FROM orders 
GROUP BY customer_id
ORDER BY monetary DESC;

-- 5. CITY WISE REVENUE ANALYSIS
SELECT 
    c.city, 
    COUNT(DISTINCT c.customer_id) as total_customers, 
    COUNT(o.order_id) as total_orders,
    SUM(o.order_value) as total_revenue
FROM customers c 
JOIN orders o ON c.customer_id = o.customer_id 
GROUP BY c.city 
ORDER BY total_revenue DESC;

-- 6. PAYMENT METHOD ANALYSIS
SELECT 
    payment_method, 
    COUNT(*) as usage_count, 
    SUM(order_value) as total_value,
    AVG(order_value) as avg_value
FROM orders 
GROUP BY payment_method
ORDER BY total_value DESC;

-- 7. CHURN ANALYSIS - ACTIVE vs CHURNED
SELECT 
    CASE 
        WHEN MAX(order_date) < DATE_SUB(CURDATE(), INTERVAL 90 DAY) THEN 'Churned'
        ELSE 'Active'
    END as customer_status, 
    COUNT(DISTINCT customer_id) as customer_count
FROM orders 
GROUP BY customer_status;

-- 8. YEARLY GROWTH RATE
SELECT 
    YEAR(order_date) as year, 
    COUNT(*) as total_orders,
    SUM(order_value) as yearly_revenue,
    LAG(SUM(order_value)) OVER (ORDER BY YEAR(order_date)) as prev_year_revenue
FROM orders 
GROUP BY year 
ORDER BY year;

-- 9. REPEAT PURCHASE RATE
SELECT 
    COUNT(DISTINCT CASE WHEN order_count > 1 THEN customer_id END) * 100.0 / COUNT(DISTINCT customer_id) as repeat_purchase_rate_percent
FROM (
    SELECT customer_id, COUNT(*) as order_count 
    FROM orders 
    GROUP BY customer_id
) as customer_orders;

-- 10. AGE GROUP WISE REVENUE ANALYSIS
SELECT 
    CASE 
        WHEN c.age < 25 THEN 'Youth ( <25 )'
        WHEN c.age < 40 THEN 'Adult (25-40)'
        WHEN c.age < 60 THEN 'Middle Age (40-60)'
        ELSE 'Senior (60+)'
    END as age_group, 
    COUNT(DISTINCT c.customer_id) as customers,
    SUM(o.order_value) as total_revenue,
    AVG(o.order_value) as avg_order_value
FROM customers c 
JOIN orders o ON c.customer_id = o.customer_id 
GROUP BY age_group 
ORDER BY total_revenue DESC;