# Dependencies
import logging
import random

import socketio
from animate import all_animations
from config import get_config
from dotenv import load_dotenv
from rpi_ws281x import PixelStrip
from tenacity import after_log, retry, stop_after_attempt, wait_fixed
from utils import spread_colors, strip_set_colors

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
previous_lights = None
previous_spread = None

# Global strip
pixel_strip = None


# Socket on connection
@sio.event
def connect():
    logger.info("connection established")

    # Get lights on connection
    sio.emit("lights:get")


# Socket lights event
@sio.event
def lights(lights):
    logger.info(f"Lights: {lights}")
    global pixel_strip

    # Don't update if the same lights
    global previous_lights
    global previous_spread
    if (
        previous_lights is not None
        and "id" in previous_lights
        and lights["id"] == previous_lights["id"]
    ):
        id = lights["id"]
        logger.info(f"Same lights {id}, no update.")
        return

    # Spread out
    spread = spread_colors(
        lights["colors"], config["pixel_length"], lights["id"], config["max_spread"]
    )

    # Animate if we know previous lights
    if previous_spread:
        id = lights["id"]
        random.seed(f"{id}-animation")
        animation = random.choice(all_animations)
        animation(
            previous_spread,
            spread,
            pixel_strip,
            lights["id"],
            framerate=config["frame_rate"],
            gamma_correction=config["gamma_correction"],
        )
    else:
        strip_set_colors(pixel_strip, spread, config["gamma_correction"])
        pixel_strip.show()

    # Keep track of lights
    previous_lights = lights
    previous_spread = spread


# Socket disconnect
@sio.event
def disconnect():
    logger.info("disconnected from server")


@retry(
    stop=stop_after_attempt(10),
    wait=wait_fixed(5),
    after=after_log(logger, logging.DEBUG),
)
def main():
    """Main program logic."""
    global pixel_strip

    # Create NeoPixel object with appropriate configuration.
    # TODO: Should other params be configurable
    # TODO: This is not well documented.
    # strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    pixel_strip = PixelStrip(
        config["pixel_length"],
        config["gpio_channel"],
        dma=config["dma_channel"],
        brightness=config["brightness"],
        strip_type=config["strip_type"],
        freq_hz=800000,
        invert=False,
        channel=0,
        gamma=None,
    )

    pixel_strip.begin()

    # Connect to server
    sio.connect(config["api_domain"])
    sio.wait()


if __name__ == "__main__":
    main()
