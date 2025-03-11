from lib.ledStrip import *
from utils.utils import *
from config.config import LED_COUNT, STRIP_GPIO_PIN, MIDI_NOTE_INDEX, LED_DRUM_INDEX
from config.pixelMap import *
from animations.hitAnimations import *

def get_led_indices_for_note(note):
    """
    Unified mapping: Use MIDI_NOTE_INDEX to convert a note to a drum type,
    then LED_DRUM_INDEX to get the corresponding LED segment.
    Returns a tuple (start, end, drum_type), or (None, None, None) if the note isn't mapped.
    """
    drum_type = MIDI_NOTE_INDEX.get(note)
    if drum_type is None:
        print(f"Warning: Unmapped MIDI note: {note}")
        return None, None, None
    if drum_type not in LED_DRUM_INDEX:
        print(f"Warning: Drum type '{drum_type}' for note {note} is not active in LED_DRUM_INDEX")
        return None, None, None
    start, end = LED_DRUM_INDEX[drum_type]
    return start, end, drum_type

def initStripValues(led_count):
    current_strip_values = {}
    for i in range(led_count):
        current_strip_values[i] = [0, 0, 0]
    return current_strip_values

def runStartupAnimation(led_strip):
    # Horizontal wipe center to sides
    map_length = len(pixel_map)
    center = map_length // 2
    for i in range(0, center):
        # Use integer indices for the pixel_map lookup
        numbers = pixel_map.get(center + i, []) + pixel_map.get(center - i, [])
        for pixel_on in numbers:
            led_strip.setPixel(pixel_on, [255, 255, 255])
        led_strip.stripShow()
        for pixel_off in range(LED_COUNT):
            led_strip.setPixel(pixel_off, [0, 0, 0])
    led_strip.stripShow()

    # Horizontal wipe sides to center
    for y in range(1, center):
        r = center - y
        numbers = pixel_map.get(center + r, []) + pixel_map.get(center - r, [])
        for pixel_on in numbers:
            led_strip.setPixel(pixel_on, [255, 255, 255])
        led_strip.stripShow()
        for pixel_off in range(LED_COUNT):
            led_strip.setPixel(pixel_off, [0, 0, 0])
        led_strip.stripShow()

    # White flash fade out
    for brightness_step in range(0, 250, 10):
        brightness_value = 250 - brightness_step
        led_strip.setSegment([brightness_value, 0, 0], 0, LED_COUNT)

def runAnimation(led_strip, animation_type):
    if animation_type == 'startup':
        runStartupAnimation(led_strip)
    # Add additional animation types as needed.
    # elif animation_type == 'rainbow':
    #     led_strip.rainbow(20, 1)

def ledStripDaemon(midi_note_queue):
    led_strip = LedStrip(LED_COUNT, STRIP_GPIO_PIN)
    current_strip_values = initStripValues(LED_COUNT)
    colours = read_json_file('config/accentColours.json')

    while True:
        try:
            midi_hit = midi_note_queue.get_nowait()
            print(f"DEBUG: Processing MIDI Note: {midi_hit['note']}")  # Debug log

            if midi_hit.get("animation"):
                runAnimation(led_strip, midi_hit["animation_type"])
                continue

            start, end, drum_type = get_led_indices_for_note(midi_hit["note"])
            if start is None:
                # Unmapped note; skip processing this hit.
                continue

            # Get the hit color from the accentColours config (fallback to white)
            hit_color = colours.get(drum_type, [255, 255, 255])

            # Modify brightness based on velocity
            multiplier = midi_hit["velocity"] * ((100 / 127)) * 0.01
            pixel_color = [
                int(hit_color[0] * multiplier),
                int(hit_color[1] * multiplier),
                int(hit_color[2] * multiplier)
            ]

            # Update the strip values for the LED segment
            for pixel in range(end - start):
                current_strip_values[pixel + start] = pixel_color

            # Update the LED strip: apply current colors and fade them
            for i in range(len(current_strip_values)):
                r, g, b = current_strip_values[i]
                # Note: color ordering may be adjusted (here we swap r and g)
                color = [g, r, b]
                led_strip.setPixel(i, color)
                current_strip_values[i] = linearFade(r, g, b)
            led_strip.stripShow()

        except Exception as e:
            # In case there is nothing in the queue or another error,
            # continue to update the LED strip with fading values.
            for i in range(len(current_strip_values)):
                r, g, b = current_strip_values[i]
                color = [g, r, b]
                led_strip.setPixel(i, color)
                current_strip_values[i] = linearFade(r, g, b)
            led_strip.stripShow()
