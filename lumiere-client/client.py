# Dependencies
import socketio
import time
import math
import logging
from dotenv import load_dotenv
from rpi_ws281x import Color, PixelStrip, ws
from colour import hex2rgb
from config import get_config

# Config
load_dotenv()
config = get_config()
config["strip_type"] = {
  "rgb": ws.WS2811_STRIP_RGB,
  "grb": ws.WS2811_STRIP_GRB
}[config["strip_type"]] if "strip_type" in config else ws.WS2811_STRIP_RGB

# Logging
logging.basicConfig(level=config["log_level"])
logger = logging.getLogger("lumiere-client")

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
def hex2pixel(hex):
    rgb = hex2rgb(hex)
    return Color(math.ceil(rgb[0] * 255), math.ceil(rgb[1] * 255), math.ceil(rgb[2] * 255))


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
    pixel_strip = PixelStrip(
        config["pixel_length"],
        config["gpio_channel"],
        # Should this be configurable
        800000,
        config["dma_channel"],
        # Should this be configurable
        False,
        config["brightness"],
        # Should this be configurable
        0,
    )

    pixel_strip.begin()

    # Connect to server
    sio.connect(config["api_domain"])
    sio.wait()


if __name__ == "__main__":
    main()
