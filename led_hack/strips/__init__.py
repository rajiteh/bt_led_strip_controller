from loguru import logger

def connect_strip(kind, mac, klass):
    tries = 0
    led = None
    while tries < 10:
        try:
            led = klass(mac)
            logger.info(f"Connected to {kind} strip {mac}")
            break
        except Exception as e:
            logger.error(f"Retry: Could not connect to {kind} strip {mac}: {e}")
            tries = tries + 1
    
    if led is None:
        raise Exception(f"couldnt connect to {kind}")

    return led
