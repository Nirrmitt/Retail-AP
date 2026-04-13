from fastapi import APIRouter, Depends, HTTPException
import asyncpg
from src.api.services.db import get_db
from src.api.models.schemas import RevenueKPI

router = APIRouter()

@router.get("/revenue", response_model=RevenueKPI)
async def get_revenue_kpi(pool: asyncpg.Pool = Depends(get_db)):
    query = """
    WITH recent AS (
        SELECT t.transaction_id, ti.line_total
        FROM transactions t
        JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
        WHERE t.status = 'completed'
          AND t.transaction_date >= CURRENT_DATE - INTERVAL '30 days'
    )
    SELECT 
        COALESCE(SUM(line_total), 0)::FLOAT AS total_revenue,
        COUNT(DISTINCT transaction_id)::INT AS order_count,
        COALESCE(AVG(line_total), 0)::FLOAT AS avg_order_value
    FROM recent;
    """
    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow(query)
            return RevenueKPI(
                total_revenue=row["total_revenue"],
                order_count=row["order_count"],
                avg_order_value=row["avg_order_value"]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
