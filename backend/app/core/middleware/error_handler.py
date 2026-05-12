import logging 
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger("app")

async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    
    except Exception as exc:
        logger.error(
            "Unhandled exception",
            extra={
                "url": str(request.url),
                "method": request.method,
                "error": str(exc),
                "trace": traceback.format_exc()
            }
        )

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error",
                "detail": str(exc)
            },
        )

