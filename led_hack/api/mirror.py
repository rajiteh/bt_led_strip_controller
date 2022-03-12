from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/turn_on")
async def turn_on(request: Request):
    request.state.mirror_led.set_power(turn_on=True)
    return {"success": True}

@router.get("/turn_off")
async def turn_off(request: Request):
    request.state.mirror_led.set_power(turn_on=False)
    return {"success": True}

@router.get("/set_white")
async def set_white(request: Request):
    request.state.mirror_led.set_white()
    return {"success": True}

@router.get("/set_brightness")
async def set_brightness(request: Request, pct: int):
    request.state.mirror_led.set_brightness(pct)
    return {"success": True}

@router.get("/set_color")
async def set_color(request: Request, color: str):
    request.state.mirror_led.set_color(color)
    return {"success": True}

@router.get("/set_temp")
async def set_temp(request: Request, temp: int):
    request.state.mirror_led.set_temp(temp)
    return {"success": True}

@router.get("/set_color_flash")
async def set_color_flash(request: Request):
    request.state.mirror_led.set_seven_color_flash()
    return {"success": True}