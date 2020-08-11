import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time-MS"] = str(
            round(process_time * 1000, 2)
        )
        return response
