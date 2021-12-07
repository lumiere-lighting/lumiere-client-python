
from os import environ
import logging


def get_config():
  """Simple function to get values from environment variables and provide defaults"""

  return {
    "api_domain": environ.get("API_DOMAIN", "https://api.lumiere.lighting"),
    "pixel_length": int(environ.get("PIXEL_LENGTH", 100)),
    "dma_channel": int(environ.get("DMA_CHANNEL", 10)),
    "gpio_channel": int(environ.get("DMA_CHANNEL", 18)),
    "brightness": int(environ.get("DMA_CHANNEL", 255)),
    "strip_type": environ.get("STRIP_TYPE", "rgb"),
    "max_spread": int(environ.get("DMA_CHANNEL", 5)),
    "log_level": int(environ.get("LOG_LEVEL", logging.WARNING))
  }