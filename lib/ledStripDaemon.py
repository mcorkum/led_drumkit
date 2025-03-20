import time
import threading
from lib.ledStrip import *
from utils.utils import *
from config.config import LED_COUNT, STRIP_GPIO_PIN, MIDI_NOTE_INDEX, LED_DRUM_INDEX, THEME_NAME, IDLE_ANIMATION
from config.pixelMap import *
from animations.hitAnimations import *

# Global idle control variables and LED update lock.
idle_thread = None
idle_stop = threading.Event()
led_lock = threading.Lock()  # Ensures only one thread updates the LED strip at a time.

def get_led_indices_for_note(note):
    """
    Converts a MIDI note to a drum type via MIDI_NOTE_INDEX,
    then looks up LED_DRUM_INDEX.
    Returns:
      - (start, end, drum_type) for contiguous mappings ([start, end]).
      - (None, mapping_list, drum_type) for non-contiguous mappings.
      - (None, None, None) if the note isn't mapped.
    """
    drum_type = MIDI_NOTE_INDEX.get(note)
    if drum_type is None:
        return None, None, None
    if drum_type not in LED_DRUM_INDEX:
        return None, None, None
    mapping = LED_DRUM_INDEX[drum_type]
    if isinstance(mapping, list) and len(mapping) == 2 and isinstance(mapping[0], int):
        return mapping[0], mapping[1], drum_type
    else:
        return None, mapping, drum_type

def initStripValues(led_count):
    current_strip_values = {}
    for i in range(led_count):
        current_strip_values[i] = [0, 0, 0]
    return current_strip_values

def runStartupAnimation(led_strip):
    """
    Runs the startup animation (horizontal wipe and fade-out).
    """
    map_length = len(pixel_map)
    center = map_length // 2
    # Wipe from center to sides.
    for i in range(0, center):
        numbers = pixel_map.get(center + i, []) + pixel_map.get(center - i, [])
        for pixel_on in numbers:
            led_strip.setPixel(pixel_on, [255, 255, 255])
        with led_lock:
            led_strip.strip.show()
        for pixel_off in range(LED_COUNT):
            led_strip.setPixel(pixel_off, [0, 0, 0])
    with led_lock:
        led_strip.strip.show()
    # Wipe from sides to center.
    for y in range(1, center):
        r = center - y
        numbers = pixel_map.get(center + r, []) + pixel_map.get(center - r, [])
        for pixel_on in numbers:
            led_strip.setPixel(pixel_on, [255, 255, 255])
        with led_lock:
            led_strip.strip.show()
        for pixel_off in range(LED_COUNT):
            led_strip.setPixel(pixel_off, [0, 0, 0])
        with led_lock:
            led_strip.strip.show()
    # White flash fade out.
    for brightness_step in range(0, 250, 10):
        brightness_value = 250 - brightness_step
        led_strip.setSegment([brightness_value, 0, 0], 0, LED_COUNT)
    with led_lock:
        led_strip.strip.show()

# Idle animation functions:

def idle_rainbow(led_strip):
    """
    Idle animation using an interruptible rainbow cycle.
    """
    while not idle_stop.is_set():
        interruptibleRainbowCycle(led_strip, wait_ms=20, iterations=1)
        time.sleep(0.05)

def idle_theaterChase(led_strip):
    """
    Idle animation using a theater chase rainbow cycle.
    """
    while not idle_stop.is_set():
        theaterChaseRainbowCycle(led_strip, wait_ms=50, cycles=1)
        time.sleep(0.1)

def idle_breathing(led_strip, theme):
    """
    Idle breathing animation that slowly fades between each color in the theme.
    Instead of fading to black, it interpolates directly from one color to the next.
    """
    # Get a list of the theme color keys.
    color_keys = list(theme.keys())
    num_keys = len(color_keys)
    # Define the number of interpolation steps and delay per step.
    steps = 200          # Increase this value for a smoother (and slower) transition.
    step_delay = 0.03    # Delay in seconds between steps.
    
    while not idle_stop.is_set():
        for i in range(num_keys):
            if idle_stop.is_set():
                break
            start_color = theme[color_keys[i]]
            next_color = theme[color_keys[(i + 1) % num_keys]]
            for step in range(steps):
                if idle_stop.is_set():
                    break
                # Compute the interpolation factor (0.0 to 1.0).
                t = step / float(steps)
                # Interpolate each RGB channel.
                interpolated = [
                    int(start_color[c] * (1 - t) + next_color[c] * t)
                    for c in range(3)
                ]
                # Set the entire strip to the interpolated color.
                led_strip.setSegment(interpolated, 0, LED_COUNT)
                with led_lock:
                    led_strip.strip.show()
                time.sleep(step_delay)


def interruptibleRainbowCycle(led_strip, wait_ms=20, iterations=1):
    """
    Runs a portion of a rainbow cycle (similar to strandtest) for a fixed number
    of iterations, checking idle_stop between iterations.
    """
    num_pixels = led_strip.strip.numPixels()
    for j in range(256 * iterations):
        if idle_stop.is_set():
            return
        for i in range(num_pixels):
            led_strip.strip.setPixelColor(i, led_strip.wheel((int(i * 256 / num_pixels) + j) & 255))
        with led_lock:
            led_strip.strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChaseRainbowCycle(led_strip, wait_ms=50, cycles=1):
    """
    Runs a portion of the theater chase rainbow animation for a fixed number of cycles.
    Checks idle_stop between iterations.
    """
    num_pixels = led_strip.strip.numPixels()
    for j in range(256 * cycles):
        if idle_stop.is_set():
            return
        for q in range(3):
            for i in range(0, num_pixels, 3):
                led_strip.strip.setPixelColor(i + q, led_strip.wheel((i + j) % 255))
            with led_lock:
                led_strip.strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, num_pixels, 3):
                led_strip.strip.setPixelColor(i + q, 0)
    with led_lock:
        led_strip.strip.show()

def idle_animation(led_strip):
    """
    Selects the idle animation based on the configuration.
    For the breathing mode, it passes the current theme colors.
    """
    theme = read_json_file(f"config/themes/{THEME_NAME}.json")
    if IDLE_ANIMATION == "rainbow":
        idle_rainbow(led_strip)
    elif IDLE_ANIMATION == "theater":
        idle_theaterChase(led_strip)
    elif IDLE_ANIMATION == "breathing":
        idle_breathing(led_strip, theme)
    else:
        idle_rainbow(led_strip)

def runAnimation(led_strip, animation_type):
    if animation_type == 'startup':
        runStartupAnimation(led_strip)
    # Additional non-idle animations can be added here.

def cleanup(led_strip):
    """
    Turns off all LEDs.
    """
    for i in range(LED_COUNT):
        led_strip.setPixel(i, [0, 0, 0])
    with led_lock:
        led_strip.strip.show()

def ledStripDaemon(midi_note_queue):
    global idle_thread, idle_stop
    led_strip = LedStrip(LED_COUNT, STRIP_GPIO_PIN)
    current_strip_values = initStripValues(LED_COUNT)
    colours = read_json_file(f"config/themes/{THEME_NAME}.json")
    
    # Run the startup animation once.
    runStartupAnimation(led_strip)
    last_midi_time = time.time()
    
    try:
        while True:
            if not midi_note_queue.empty():
                midi_hit = midi_note_queue.get_nowait()
                # If idle animation is running, stop it.
                if idle_thread is not None and idle_thread.is_alive():
                    idle_stop.set()
                    idle_thread.join()
                    idle_thread = None
                    idle_stop.clear()
                last_midi_time = time.time()
                
                if midi_hit.get("animation"):
                    runAnimation(led_strip, midi_hit["animation_type"])
                    continue
                
                start, mapping, drum_type = get_led_indices_for_note(midi_hit["note"])
                if start is None and mapping is None:
                    continue  # Skip unmapped notes.
                
                hit_color = colours.get(drum_type, [255, 255, 255])
                multiplier = midi_hit["velocity"] * ((100 / 127)) * 0.01
                pixel_color = [
                    int(hit_color[0] * multiplier),
                    int(hit_color[1] * multiplier),
                    int(hit_color[2] * multiplier)
                ]
                
                if start is not None:
                    end = mapping
                    for pixel in range(end - start):
                        current_strip_values[pixel + start] = pixel_color
                else:
                    for idx in mapping:
                        current_strip_values[idx] = pixel_color
            
            # Trigger idle animation after 5 seconds of inactivity.
            if time.time() - last_midi_time > 5:
                if idle_thread is None or not idle_thread.is_alive():
                    idle_thread = threading.Thread(target=idle_animation, args=(led_strip,))
                    idle_thread.start()
                    last_midi_time = time.time()  # Reset timer.
            
            # If idle animation is NOT running, update LED strip normally.
            if idle_thread is None or not idle_thread.is_alive():
                for i in range(len(current_strip_values)):
                    r, g, b = current_strip_values[i]
                    color = [g, r, b]  # Adjust ordering if needed.
                    led_strip.setPixel(i, color)
                    current_strip_values[i] = linearFade(r, g, b)
                with led_lock:
                    led_strip.strip.show()
            
            # Throttle main loop.
            time.sleep(0.03)
            
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Cleaning up...")
        if idle_thread is not None and idle_thread.is_alive():
            idle_stop.set()
            idle_thread.join()
        cleanup(led_strip)
    except Exception as e:
        print("Exception occurred:", e)
        cleanup(led_strip)
