from fastapi import APIRouter, Depends, HTTPException
import asyncpg
import uuid
from pydantic import BaseModel, Field
from typing import List
from src.api.services.db import get_db

router = APIRouter()

class TransactionPayload(BaseModel):
    customer_id: uuid.UUID
    product_ids: List[uuid.UUID]
    quantities: List[int] = Field(..., min_items=1)
    payment_method: str = "credit_card"
    status: str = "completed"

@router.post("/ingest", status_code=201)
async def ingest_transaction(payload: TransactionPayload, pool: asyncpg.Pool = Depends(get_db)):
    if len(payload.product_ids) != len(payload.quantities):
        raise HTTPException(status_code=400, detail="product_ids and quantities must match")
        
    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                # 1. Insert transaction header
                txn = await conn.fetchrow(
                    """INSERT INTO transactions (customer_id, transaction_date, status, payment_method) 
                       VALUES ($1, NOW(), $2, $3) RETURNING transaction_id""",
                    payload.customer_id, payload.status, payload.payment_method
                )
                txn_id = txn["transaction_id"]
                
                # 2. Insert line items
                for pid, qty in zip(payload.product_ids, payload.quantities):
                    price = await conn.fetchval("SELECT unit_price FROM products WHERE product_id = $1", pid)
                    if not price:
                        continue
                    await conn.execute(
                        """INSERT INTO transaction_items (transaction_id, product_id, quantity, unit_price) 
                           VALUES ($1, $2, $3, $4)""",
                        txn_id, pid, qty, price
                    )
        return {"status": "success", "transaction_id": str(txn_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")