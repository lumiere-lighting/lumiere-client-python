# Turn off the lights strip.  Likely useful to call this
# before stopping the client.py.

# Dependencies
import logging

from coloraide import Color
from config import get_config
from dotenv import load_dotenv
from rpi_ws281x import PixelStrip
from tenacity import after_log, retry, stop_after_attempt, wait_fixed
from utils import strip_set_colors

# Config
load_dotenv()
config = get_config()

# Logging
logging.basicConfig(level=config["log_level"])
logger = logging.getLogger("lumiere-client")
logger.info(config)

# Global strip
pixel_strip = None


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

    # Turn off the lights
    strip_set_colors(
        pixel_strip,
        [Color("black") for i in range(config["pixel_length"])],
        config["gamma_correction"],
    )
    pixel_strip.show()


if __name__ == "__main__":
    main()
