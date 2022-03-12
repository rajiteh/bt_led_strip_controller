from fastapi import APIRouter, Request


router = APIRouter()

@router.get("/turn_on")
async def turn_on(request: Request):
    request.state.govee_led.set_state(True)
    return {"success": True}

@router.get("/turn_off")
async def turn_off(request: Request):
    request.state.govee_led.set_state(False)
    return {"success": True}

@router.get("/set_brightness")
async def set_brightness(request: Request, pct: int):
    if pct < 0 or pct > 100:
        return Exception("must be between 0 and 100")
    request.state.govee_led.set_brightness(pct / 100)
    return {"success": True}

@router.get("/set_color")
async def set_color(request: Request, color: str):
    request.state.govee_led.set_color(color)
    return {"success": True}

@router.get("/set_white")
async def set_temp(request: Request, value: int = 1):
    request.state.govee_led.set_color_white(value)
    return {"success": True}
