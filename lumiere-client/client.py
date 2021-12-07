# Dependencies
import socketio
import time
import math
import logging
from dotenv import load_dotenv
from rpi_ws281x import Color as PixelColor, PixelStrip, ws
from coloraide import Color
from config import get_config

# Config
load_dotenv()
config = get_config()

# Logging
logging.basicConfig(level=config["log_level"])
logger = logging.getLogger("lumiere-client")
logger.info(config)

# SocketIO client
sio = socketio.Client()

# Keep track of lights set
current_lights = None

# Global strip
pixel_strip = None

# Socket on connection
@sio.event
def connect():
    print('connected')
    logger.info("connection established")

    # Get lights on connection
    sio.emit("lights:get")


# Socket lights event
@sio.event
def lights(lights):
    logger.info(f"Lights: {lights}")
    global pixel_strip

    # Don't update if the same lights
    global current_lights
    if current_lights is not None and "id" in current_lights and lights["id"] == current_lights["id"]:
        logger.info(f"Same lights {id}, no update.")
        return

    # Spread out
    spread = spread_colors(lights["colors"])

    # set colors to pixels
    for i in range(config["pixel_length"]):
        pixel_strip.setPixelColor(i, hex2pixel(spread[i]))
    
    # Render
    pixel_strip.show()

    # Keep track of lights
    current_lights = lights


# Socket disconnect
@sio.event
def disconnect():
    logger.info("disconnected from server")


# Hex to pixel
def hex2pixel(hex_string):
    c = Color(hex_string)
    c_dict = c.to_dict()
    return PixelColor(math.ceil(c_dict["r"] * 255), math.ceil(c_dict["g"] * 255), math.ceil(c_dict["b"] * 255))


# Spread out colors into strip
def spread_colors(colors):
    spread = 1
    fullColors = []

    # Fill in colors.  Probably a more efficient way to do this.
    spreadPlace = 0
    colorPlace = 0
    for i in range(config["pixel_length"]):
        fullColors.append(colors[colorPlace])

        # Spread place used to know how many times to repeat the color place
        spreadPlace = 0 if spreadPlace == spread - 1 else spreadPlace + 1
        # When the spread place starts, increment the color.
        if i > 0 or spread == 1:
            colorPlace = colorPlace + 1 if spreadPlace == 0 else colorPlace
            colorPlace = 0 if colorPlace >= len(colors) else colorPlace

    return fullColors


def main():
    """Main program logic."""
    global pixel_strip

    # Create NeoPixel object with appropriate configuration.
    # TODO: Should other params be configurable
    pixel_strip = PixelStrip(
        config["pixel_length"],
        config["gpio_channel"],
        dma=config["dma_channel"],
        brightness=config["brightness"],
        strip_type=config["strip_type"],
        freq_hz=800000,
        invert=False,
        channel=0,
        gamma=None
    )

    pixel_strip.begin()

    # Connect to server
    sio.connect(config["api_domain"])
    sio.wait()


if __name__ == "__main__":
    main()
