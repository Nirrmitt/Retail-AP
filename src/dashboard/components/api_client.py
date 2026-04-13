import requests

class DashboardAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def get_revenue_kpi(self, days: int = 30) -> dict:
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/kpi/revenue",
                params={"days": days},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return {"total_revenue": 0, "order_count": 0, "avg_order_value": 0}

    def get_daily_revenue(self, days: int = 30) -> list:
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/sales/daily-revenue",
                params={"days": days},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return []

    def get_category_revenue(self) -> list:
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/sales/category-revenue",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return []

    def health_check(self) -> dict:
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.json()
        except:
            return {"status": "disconnected", "database": "offline"}

# Global instance
api_client = DashboardAPIClient()