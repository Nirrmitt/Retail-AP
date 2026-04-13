from pydantic import BaseModel

class RevenueKPI(BaseModel):
    total_revenue: float
    order_count: int
    avg_order_value: float

class HealthResponse(BaseModel):
    status: str
    database: str