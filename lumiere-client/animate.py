import math
import time
import random
from coloraide import Color
# See easing functions:
# https://github.com/semitable/easing-functions/blob/master/easing_functions/__init__.py
from easing_functions import LinearInOut, CubicEaseInOut
from utils import strip_set_colors


def animate(frame_handler, length = 4, framerate = 30, easing = LinearInOut):
    """Basic animate function"""
    interval = 1 / framerate
    frames = math.floor(length * framerate)
    s = time.perf_counter()
    e = easing()

    for i in range(frames):
        # Measure how long it takes to run the frame to offset the wait
        start_frame = time.perf_counter()
        frame_handler(e(i / frames))
        end_frame = time.perf_counter()
        frame_time = end_frame - start_frame
        frame_remaining = interval - frame_time
        time.sleep(0.001 if frame_remaining <= 0.001 else frame_remaining)

    e = time.perf_counter()


def animate_to_colors(start_colors, end_colors, strip, id, length = 5, easing = CubicEaseInOut):
    # Calculate transition functions
    interpolations = []
    for i in range(len(start_colors)):
        interpolations.append(Color(start_colors[i]).interpolate(Color(end_colors[i]), space="srgb"))

    # Frame handler function
    def frame_handler(t):
        strip_set_colors(strip, [i(t) for i in interpolations])
        strip.show()

    animate(frame_handler, length = length, easing = easing)


def animate_roll_out_then_in(start_colors, end_colors, strip, id, length = 5, easing = CubicEaseInOut):
    # Sub handler to move from color to black (or vic-versa)
    def roll_color(c, t, from_black = True):
        distance = math.floor(len(c) * t)
        moved = []
        for i in range(len(c)):
            # TODO: Depending on the configuration of lights, c[i - distance] makes more
            # sense, such as if the lights are mostly linear.  Make configurable.
            if from_black:
                moved.append(c[i] if i <= distance else Color('black'))
            else:
                moved.append(Color('black') if i <= distance else c[i])

        strip_set_colors(strip, moved)
        strip.show()

    # First part
    def frame_handler_first(t):
        roll_color(start_colors, t, from_black = False)

    animate(frame_handler_first, length / 2, easing = easing)

    # Second part
    def frame_handler_first(t):
        roll_color(end_colors, t, from_black = True)

    animate(frame_handler_first, length / 2, easing = easing)


def animate_fade_out_then_in(start_colors, end_colors, strip, id, length = 5, easing = CubicEaseInOut):
    all_black = [Color('black') for i in range(len(start_colors))]

    # First part
    animate_to_colors(start_colors, all_black, strip, id, length = length / 2, easing = easing)

    # Second part
    animate_to_colors(all_black, end_colors, strip, id, length = length / 2, easing = easing)


def animate_fade_out_then_in_random(start_colors, end_colors, strip, id, length = 6, easing = CubicEaseInOut):
    random.seed(f"{id}-animate_fade_out_then_in_random")
    all_black = [Color('black') for i in range(len(start_colors))]

    # Calculate transitions for fade out
    interpolations_out = []
    start_out = []
    for i in range(len(start_colors)):
        interpolations_out.append(Color(start_colors[i]).interpolate(Color(all_black[i]), space="srgb"))
        start_out.append(random.uniform(0.1, 1))

    # Calculate transitions for fade in
    interpolations_in = []
    start_in = []
    for i in range(len(start_colors)):
        interpolations_in.append(Color(all_black[i]).interpolate(Color(end_colors[i]), space="srgb"))
        start_in.append(random.uniform(0, 0.9))

    # First half (fade out)
    def frame_handler_fade_out(t):
        strip_set_colors(strip, [
            (interpolations_out[i](proportion_time(0, start_out[i], t)) if t <= start_out[i] else all_black[i])
            for i in range(len(interpolations_out))
        ])
        strip.show()

    animate(frame_handler_fade_out, length = length / 2, easing = easing)

    # First half (fade in)
    def frame_handler_fade_in(t):
        strip_set_colors(strip, [
            (interpolations_in[i](proportion_time(start_in[i], 1, t)) if t >= start_in[i] else all_black[i])
            for i in range(len(interpolations_in))
        ])
        strip.show()

    animate(frame_handler_fade_in, length = length / 2, easing = easing)


# Consistent math to calculate for sub_animations.  For instance, to run
# a complete animation from 0.2 through 0.7 of an animation t (0 - 1).
# Returns 0 - 1 of the sub-time (i.e. 0.2 - 0.7)
def proportion_time(start, end, t):
    if t < start or t > end:
        return -1

    span = end - start
    return (t - start) / span


# All animations
all_animations = [
    animate_to_colors,
    animate_roll_out_then_in,
    # animate_fade_out_then_in,
    animate_fade_out_then_in_random
]
