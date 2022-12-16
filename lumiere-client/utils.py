import math
import random
from coloraide import Color
from rpi_ws281x import Color as PixelColor


# Coloraide color to pixel
def color_to_pixel(color, gamma_correction):
    c_dict = color.to_dict()
    return PixelColor(
        math.ceil(gamma_correct(c_dict["r"], gamma_correction) * 255),
        math.ceil(gamma_correct(c_dict["g"], gamma_correction) * 255),
        math.ceil(gamma_correct(c_dict["b"], gamma_correction) * 255),
    )


# Hex to pixel
def hex_to_pixel(hex_string, gamma_correction):
    return color_to_pixel(Color(hex_string), gamma_correction)


# Spread out colors into strip
def spread_colors(colors, pixel_length, id, max_spread):
    random.seed(f"{id}-spread")
    spread = random.randint(1, max_spread)
    full_colors = []

    # Fill in colors.  Probably a more efficient way to do this.
    spread_place = 0
    color_place = 0
    for i in range(pixel_length):
        full_colors.append(colors[color_place])

        # Spread place used to know how many times to repeat the color place
        spread_place = 0 if spread_place == spread - 1 else spread_place + 1

        # When the spread place starts, increment the color.
        if i > 0 or spread == 1:
            color_place = color_place + 1 if spread_place == 0 else color_place
            color_place = 0 if color_place >= len(colors) else color_place

    return full_colors


# Set all colors in a strip
def strip_set_colors(strip, colors, gamma_correction):
    for i in range(len(colors)):
        if isinstance(colors[i], Color):
            strip.setPixelColor(i, color_to_pixel(colors[i], gamma_correction))
        else:
            strip.setPixelColor(i, hex_to_pixel(colors[i], gamma_correction))


# Correct gamma for a value.  Value should be value between 0 and 1.
# Inspiration:
# https://github.com/adafruit/Adafruit_CircuitPython_FancyLED/blob/main/adafruit_fancyled/adafruit_fancyled.py#L372
def gamma_correct(value, gamma_correction):
    if not gamma_correction:
        return value

    return pow(value, gamma_correction)
