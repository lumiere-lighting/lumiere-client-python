import math
import time
from coloraide import Color
from utils import strip_set_colors


def animate(frame_handler, length = 3, framerate = 30):
    """Basic animate function"""
    interval = 1 / framerate
    frames = math.floor(length * framerate)
    s = time.perf_counter()

    for i in range(frames):
        # Measure how long it takes to run the frame to offset the wait
        start_frame = time.perf_counter()
        frame_handler(i / frames)
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
