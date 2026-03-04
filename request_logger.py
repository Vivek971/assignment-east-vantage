import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from logger import get_logger

logger = get_logger("request_logger")


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        method = request.method
        url = request.url.path
        client = request.client.host

        logger.info(f"Request started | {method} {url} | client={client}")

        try:
            response = await call_next(request)

        except Exception as e:
            logger.exception(f"Request failed | {method} {url}")
            raise e

        process_time = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"Request completed | {method} {url} | "
            f"status={response.status_code} | time={process_time}ms"
        )

        return response