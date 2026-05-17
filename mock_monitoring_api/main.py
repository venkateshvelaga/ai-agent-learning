from fastapi import FastAPI
import random
import time

app = FastAPI(title="Mock Monitoring API")


@app.get("/")
def root():
    return {
        "message": "Mock Monitoring API is running",
        "try_endpoint": "/health/checkout"
    }


@app.get("/health/{service_name}")
def get_service_health(service_name: str):
    random_number = random.random()

    if random_number < 0.35:
        return {
            "service": service_name,
            "status": "degraded",
            "availability": "99.72%",
            "latency_p95_ms": random.randint(1200, 2500),
            "error_rate_percent": round(random.uniform(4.0, 8.5), 2),
            "recent_change": "Payment validation release deployed 45 minutes ago",
            "timestamp": int(time.time())
        }

    return {
        "service": service_name,
        "status": "healthy",
        "availability": "99.99%",
        "latency_p95_ms": random.randint(120, 300),
        "error_rate_percent": round(random.uniform(0.1, 0.8), 2),
        "recent_change": "No risky deployment detected",
        "timestamp": int(time.time())
    }