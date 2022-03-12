from govee_btled import BluetoothLED
import time


# https://github.com/egold555/Govee-Reverse-Engineering/blob/master/Products/H6113.md
# https://github.com/jurassic-marc/govee-h6159-light-strip-reverse-engineer
# https://github.com/chvolkmann/govee_btled
# https://github.com/egold555/Govee-Reverse-Engineering


def connect(mac):
    return BluetoothLED(mac)

LED_STRIP_MAC = "A4:C1:38:96:18:60"
if __name__ == "__main__":

    led = None
    tries = 0
    while tries < 10:
        try:
            led = BluetoothLED(LED_STRIP_MAC)
            break
        except:
            print("retry..")
            tries = tries + 1
    if led is None:
        print("couldnt connect")
        exit(1)
    led.set_state(True)
    # time.sleep(1)
    # led.set_color('blue')
    # time.sleep(1)
    # led.set_color('#facd03')
    # time.sleep(1)
    # led.set_state(False)
    # time.sleep(1)

    # The bulb seems to have a white-mode which uses cold/warm white LEDs instead of the RGB LEDs.
    # Supply a value between -1 (warm) and 1 (cold)
    # led.set_color_white(-0.4)