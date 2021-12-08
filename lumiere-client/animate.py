import math
import time
from coloraide import Color
from easing_functions import LinearInOut, CubicEaseInOut, BounceEaseInOut
from utils import strip_set_colors


def animate(frame_handler, length = 3, framerate = 30, easing = LinearInOut):
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


def animate_to_colors(start_colors, end_colors, strip):
    # Calculate transition functions
    interpolations = []
    for i in range(len(start_colors)):
        interpolations.append(Color(start_colors[i]).interpolate(Color(end_colors[i]), space="srgb"))

    # Frame handler function
    def frame_handler(t):
        strip_set_colors(strip, [i(t) for i in interpolations])
        strip.show()

    animate(frame_handler)


def animate_train_rolling(start_colors, end_colors, strip):
    # Sub handler to move from color to black (or vic-versa)
    def roll_color(c, t, from_black = True):
        distance = math.floor(len(c) * t)
        moved = []
        for i in range(len(c)):
            # TODO: Depending on the configuration of lights, i - distance makes more
            # sense, such as if the lights are mostly linear.  Make configurable.
            if from_black:
                moved.append(c[i] if i <= distance else Color('black'))
            else:
                moved.append(Color('black') if i <= distance else c[i - distance])

        strip_set_colors(strip, moved)
        strip.show()

    # First part
    def frame_handler_first(t):
        roll_color(start_colors, t, from_black = False)

    animate(frame_handler_first, length = 2.5, easing = BounceEaseInOut)

    # Second part
    def frame_handler_first(t):
        roll_color(end_colors, t, from_black = True)

    animate(frame_handler_first, length = 2.5, easing = BounceEaseInOut)


# Consistent math to calculate for sub_animations
def proportion_time(start, end, t):
    if t < start or t > end:
        return -1

    span = end - start
    return (t - start) / span
