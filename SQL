WITH SalesData AS (
    SELECT 
        p.product_id,
        p.product_name,
        pc.product_class_id,
        pc.product_class_name,
        SUM(s.quantity) AS total_quantity,
        SUM(s.quantity * s.retail_price) AS sales_value
    FROM Sales_Transaction s
    JOIN Product p ON s.product_id = p.product_id
    JOIN Product_Class pc ON p.product_class_id = pc.product_class_id
    GROUP BY p.product_id, p.product_name, pc.product_class_id, pc.product_class_name
),
RankedSales AS (
    SELECT 
        product_class_id,
        product_class_name,
        product_id,
        product_name,
        total_quantity,
        sales_value,
        RANK() OVER (
            PARTITION BY product_class_id 
            ORDER BY sales_value DESC, total_quantity ASC
        ) AS rank
    FROM SalesData
)
SELECT 
    product_class_name,
    product_id,
    product_name,
    total_quantity,
    sales_value,
    rank
FROM RankedSales
WHERE rank <= 2
ORDER BY product_class_id, rank;
