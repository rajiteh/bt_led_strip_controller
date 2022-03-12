
from contextlib import contextmanager
from typing import List
from loguru import logger
import sys
import simplepyble
from colour import Color

class MirrorStrip:
    
    SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
    CHARACTER_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
    
    ADAPTER_IDENTIFIER = "hci0"

    def __init__(self, strip):
        self._connected = False
        self.strip = strip
        self.connect()

    def __del__(self):
        logger.info("Disconnecting")
        self.disconnect()

    def connect(self, force=False):
        if self._connected and not force:
            return

        logger.info("Connecting")
        self.strip.connect()
        self._connected = True

    def disconnect(self):
        self.strip.disconnect()
        self._connected = False
        
    @contextmanager
    def connected(self):
        self.connect()
        try:
            yield self
        finally:
            self.disconnect()

    
    @classmethod
    def discover_device_by_mac(klass, mac : str) -> "MirrorStrip":
        adapters = simplepyble.Adapter.get_adapters()

        if len(adapters) == 0:
            logger.error("No adapters found")
            sys.exit(1)

        adapter = [adapter for adapter in adapters if adapter.identifier() == klass.ADAPTER_IDENTIFIER].pop()
        logger.debug(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")
        peripheral=None
        attempts=0
        while True:
            try:
                scan_period =125 + (attempts * 50)
                logger.debug(f"Scanning devices for {scan_period}")
                adapter.scan_for(scan_period)
                peripherals = adapter.scan_get_results()
                peripheral = [p for p in peripherals if p.address() == mac].pop()
                break
            except Exception as e:
                attempts = attempts + 1
                if attempts > 4:
                    raise e
                logger.error(f"Discovery failure: {str(e)}")

        logger.debug(f"Selected peripheral: {peripheral.identifier()} [{peripheral.address()}]")
        return klass(peripheral)
    def _write_bytes(self, content: List['int']):
        if not self._connected:
            raise Exception("Not connected.")

        if len(content) != 9:
            raise Exception(f"Incorrect content data. Recieved: {str(content)}")
        content_bytes = b''.join([i.to_bytes(1, byteorder="big", signed=True) for i in content])
        logger.debug(f"Writing: {str(content)} ({str(content_bytes)}))")
        self.strip.write_request(self.SERVICE_UUID, self.CHARACTER_UUID, content_bytes)

    def _clamped(self, number, min=-126, max=126):
        if number > max:
            return max
        elif number < min:
            return min
        else:
            return number



    def set_power(self, turn_on : bool):
        logger.debug(f"Setting power to : {turn_on}")
        content = [126, 4, 4, 0, 0, 1, -1, 0, -17]
        if not turn_on:
            content[5] = 0
        self._write_bytes(content)    

    def set_white(self):
        logger.debug(f"Setting to white.")
        content = [126, 7,5,3, -1, -1, -1, -1, -17]  
        self._write_bytes(content) 


    def set_seven_color_flash(self):
        logger.debug("Setting seven color flash")
        content = [126, 5, 3, -107, 3, -1, -1, 0, -17]
        self._write_bytes(content)
            
    def set_brightness(self, brightness_pct):
        brightness = self._clamped(int((brightness_pct / 126) * 100), min=3)
        logger.debug(f"Setting brightness: {brightness}")
        content = [126, 4, 1, brightness, -1, -1, -1, 0, -17]
        self._write_bytes(content)

    def set_color(self, color):
        col = Color(color)
        rgb = col.red, col.green, col.blue
        r, g, b = [round(x * 126) for x in rgb]
        
        logger.debug(f"Setting RGB:({r},{g},{b})")
        content = [126, 7, 5, 3, r, g, b, 0, -17]
        self._write_bytes(content)

    def set_temp(self, warmth):
        warmth = self._clamped(warmth, min=0, max=100)
        logger.debug(f"Setting warmth to {warmth}")
        content = [126, 6, 5, 2, 100 - warmth, warmth, -1, 8, -17 ]
        self._write_bytes(content)

    def set_black_white(self, level):
        r = int(self._clamped(level, min=0, max=255) * 100 / 255)
        logger.debug(f"Setting black_white level {level}")
        content = [126, 7, 5, 3, r, r, r, r, -17]
        self._write_bytes(content)

    # TODO: Special case for white and green not sure why
    def set_color_by_id(self, i):
        if i == 5:
            # 255, 255, 0
            content = [126, 6, 5, 2, 100, 100, -1, 8, -17]
        elif i == 6:
            # 255, 255, 255
            content = [126, 6, 5, 2, -1, -1, -1, 8, -17]
        else:
            return False
        logger.debug(f"Set color by id {i}")
        self._write_bytes(content)

    # TODO: unknown behaviour
    def set_click(self, z):
        logger.debug(f"Setting click: {z}")
        content = [126, 3, 4, 0, 0, 0, -1, 0, -17]
        if z:
            content[5] = 1
        self._write_bytes(content)