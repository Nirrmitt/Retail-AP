from fastapi import APIRouter, Depends
import asyncpg
from src.api.services.db import get_db
from typing import List
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/daily-revenue")
async def get_daily_revenue(
    days: int = 30,
    pool: asyncpg.Pool = Depends(get_db)
):
    """Get daily revenue for the last N days"""
    query = """
    SELECT 
        DATE_TRUNC('day', t.transaction_date)::DATE AS date,
        COUNT(DISTINCT t.transaction_id) AS orders,
        SUM(ti.line_total) AS revenue,
        COUNT(DISTINCT t.customer_id) AS unique_customers
    FROM transactions t
    JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
    WHERE t.status = 'completed'
      AND t.transaction_date >= CURRENT_DATE - INTERVAL '%s days'
    GROUP BY DATE_TRUNC('day', t.transaction_date)
    ORDER BY date ASC;
    """ % days
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]

@router.get("/category-revenue")
async def get_category_revenue(
    pool: asyncpg.Pool = Depends(get_db)
):
    """Get revenue by product category"""
    query = """
    SELECT 
        p.category,
        COUNT(DISTINCT t.transaction_id) AS orders,
        SUM(ti.line_total) AS revenue,
        AVG(ti.line_total) AS avg_order_value
    FROM transactions t
    JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
    JOIN products p ON ti.product_id = p.product_id
    WHERE t.status = 'completed'
      AND t.transaction_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY p.category
    ORDER BY revenue DESC;
    """
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]

@router.get("/top-products")
async def get_top_products(
    limit: int = 10,
    pool: asyncpg.Pool = Depends(get_db)
):
    """Get top selling products by revenue"""
    query = """
    SELECT 
        p.name AS product_name,
        p.category,
        SUM(ti.quantity) AS units_sold,
        SUM(ti.line_total) AS revenue,
        COUNT(DISTINCT t.transaction_id) AS times_purchased
    FROM transactions t
    JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
    JOIN products p ON ti.product_id = p.product_id
    WHERE t.status = 'completed'
      AND t.transaction_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY p.product_id, p.name, p.category
    ORDER BY revenue DESC
    LIMIT %s;
    """ % limit
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]