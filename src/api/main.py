from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from src.api.routes import kpi, sales  # Add sales import
from src.api.services.db import db, get_db
import asyncpg
from src.api.models.schemas import HealthResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(
    title="Retail Analytics API",
    description="Production KPI endpoints for retail dashboard",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(kpi.router, prefix="/api/v1/kpi", tags=["KPIs"])
app.include_router(sales.router, prefix="/api/v1/sales", tags=["Sales Analytics"])  # Add this

@app.get("/health", response_model=HealthResponse)
async def health_check(pool: asyncpg.Pool = Depends(get_db)):
    try:
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return HealthResponse(status="healthy", database="connected")
    except Exception:
        return HealthResponse(status="degraded", database="disconnected")