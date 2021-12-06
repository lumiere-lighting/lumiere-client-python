# Dependencies
import socketio
from rpi_ws281x import Color, PixelStrip
import time


# Config
LED_COUNT = 200
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

# SocketIO client
sio = socketio.Client()


# Socket on connection
@sio.event
def connect():
    print("connection established")

    # Get lights on connection
    sio.emit("lights:get")


# Socket lights event
@sio.event
def lights(data):
    print(f"Lights {data}")


# Socket disconnect
@sio.event
def disconnect():
    print("disconnected from server")


def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def main():
    """Main program logic."""

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(
        LED_COUNT,
        LED_PIN,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        LED_CHANNEL,
    )
    strip.begin()

    colorWipe(strip, Color(255, 0, 0))

    # Connect to server
    sio.connect("http://api.lumiere.lighting")
    sio.wait()


if __name__ == "__main__":
    main()
