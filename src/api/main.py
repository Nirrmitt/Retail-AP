from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from src.api.routes import kpi, sales, ingest  # ✅ Import all routers here
from src.api.services.db import db, get_db
import asyncpg
from src.api.models.schemas import HealthResponse

# 1️⃣ Define lifespan (runs on startup/shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

# 2️⃣ Initialize FastAPI app
app = FastAPI(
    title="Retail Analytics API",
    description="Production KPI endpoints for retail dashboard",
    version="1.0.0",
    lifespan=lifespan
)

# 3️⃣ Register routers (AFTER app is defined)
app.include_router(kpi.router, prefix="/api/v1/kpi", tags=["KPIs"])
app.include_router(sales.router, prefix="/api/v1/sales", tags=["Sales Analytics"])
app.include_router(ingest.router, prefix="/api/v1/data", tags=["Data Ingestion"])  # ✅ Now safe

# 4️⃣ Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check(pool: asyncpg.Pool = Depends(get_db)):
    try:
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return HealthResponse(status="healthy", database="connected")
    except Exception:
        return HealthResponse(status="degraded", database="disconnected")