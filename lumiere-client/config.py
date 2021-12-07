
from os import environ
from rpi_ws281x import ws
import logging


def get_config():
  """Simple function to get values from environment variables and provide defaults"""

  # Convert strip type
  strip_type_options = {
    "rgb": ws.WS2811_STRIP_RGB,
    "rbg": ws.WS2811_STRIP_RBG,
    "grb": ws.WS2811_STRIP_GRB,
    "gbr": ws.WS2811_STRIP_GBR,
    "brg": ws.WS2811_STRIP_BRG,
    "bgr": ws.WS2811_STRIP_BGR
  }
  strip_type = environ.get("STRIP_TYPE", "rgb")
  strip_type = strip_type_options[strip_type] if strip_type in strip_type_options else ws.WS2811_STRIP_RGB

  return {
    "api_domain": environ.get("API_DOMAIN", "https://api.lumiere.lighting"),
    "pixel_length": int(environ.get("PIXEL_LENGTH", 100)),
    "dma_channel": int(environ.get("DMA_CHANNEL", 10)),
    "gpio_channel": int(environ.get("GPIO_CHANNEL", 18)),
    "brightness": int(environ.get("BRIGHTNESS", 255)),
    "strip_type": strip_type,
    "max_spread": int(environ.get("MAX_SPREAD", 5)),
    "log_level": int(environ.get("LOG_LEVEL", logging.WARNING))
  }