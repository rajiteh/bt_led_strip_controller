
from govee_btled import BluetoothLED
from loguru import logger

def connect_govee(mac):
    tries = 0
    led = None
    while tries < 10:
        try:
            led = BluetoothLED(mac)
            led.__del__ == (lambda x: True)
            logger.info(f"Connected to govee strip {mac}")
            break
        except Exception as e:
            logger.error(f"Retry: Could not connect to govee strip {mac}: {e}")
            tries = tries + 1
    
    if led is None:
        raise Exception("couldnt connect to govee")

    return led
