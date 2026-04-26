{{ config(materialized='incremental',unique_key='order_id') }}

SELECT order_id,customer_id,product_id,order_date,quantity,total_amount 
FROM {{ ref('int_orders') }}

{% if is_incremental() %} 
    {% if var('backfill_start_date', False) and var('backfill_end_date', False) %}
        WHERE order_date >= '{{ var("backfill_start_date") }}'
          AND order_date <= '{{ var("backfill_end_date") }}'
    {% else %}
        WHERE order_date > (SELECT MAX(order_date) FROM {{ this }})
    {% endif %}
{% endif %}
