import time
import uuid
import sys
from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse

from .strips import mirror, govee, connect_strip

from .api.mirror import router as mirror_router
from .api.govee import router as govee_router

app = FastAPI(
    title="LED Strip Controller",
    description="",
    version="0.1.0",
    redoc_url=None,
)


LOG_PREFIX = "level={level} source=<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"

logger.remove()
logger.add(
    sys.stdout,
    format=f"{LOG_PREFIX} | {{message}} ",
    level="DEBUG",
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    with logger.contextualize(request_id=request_id):
        start_time = time.time()
        response = None
        try:
            response = await call_next(request)
        except Exception as ex:
            logger.error(f"Request failed: {ex}")
            logger.exception(ex)
            response = JSONResponse(
                content={"success": False, "error": str(ex)}, status_code=500
            )
        finally:
            process_time = (time.time() - start_time) * 1000
            formatted_process_time = "{0:.2f}".format(process_time)
            log_resp = {
                "response": 000,
            }
            if response:
                log_resp["response"] = response.status_code

            logger.info(
                f"client={request.client.host}:{request.client.port} method={request.method} url={request.url.path} response={log_resp['response']} completed_in={formatted_process_time}ms ",
            )
    return response


@app.middleware("http")
async def initialize_bt(request: Request, call_next):
    if "/govee" in request.url.path:
        request.state.govee_led = connect_strip("govee", "A4:C1:38:96:18:60", govee.BluetoothLED)
    elif "/mirror" in request.url.path:
        request.state.mirror_led = connect_strip("mirror", "FF:FF:18:07:F5:0B", mirror.MirrorLEDStrip)

    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return RedirectResponse("/docs")


app.include_router(mirror_router, prefix="/api/mirror", tags=["MirrorLEDStrip"])
app.include_router(govee_router, prefix="/api/govee", tags=["GoveeLEDStrip"])



