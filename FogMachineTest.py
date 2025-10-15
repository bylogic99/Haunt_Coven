"""Simple standalone fog machine DMX test.

Run this module directly to pulse the fog machine for a few seconds.
"""

import time

from DMXController import DMXController

# DMX configuration used by the main application.
FOG_CHANNEL = 1
FOG_ON_VALUE = 255
FOG_OFF_VALUE = 0
FOG_PULSE_SECONDS = 3


def main():
    controller = DMXController()
    print("DMX fog test starting.")

    try:
        print(f"Setting fog channel {FOG_CHANNEL} to {FOG_ON_VALUE}.")
        controller.set_channel(FOG_CHANNEL, FOG_ON_VALUE)
        time.sleep(FOG_PULSE_SECONDS)
    finally:
        print(f"Setting fog channel {FOG_CHANNEL} to {FOG_OFF_VALUE}.")
        controller.set_channel(FOG_CHANNEL, FOG_OFF_VALUE)
        controller.stop()

    print("Fog test complete.")


if __name__ == "__main__":
    main()

