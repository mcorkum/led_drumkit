from lib.ledStrip import *
from utils.utils import *
from config.config import LED_COUNT, STRIP_GPIO_PIN, MIDI_NOTE_INDEX, LED_DRUM_INDEX, THEME_NAME
from config.pixelMap import *
from animations.hitAnimations import *

def get_led_indices_for_note(note):
    """
    Converts a MIDI note to a drum type via MIDI_NOTE_INDEX,
    then looks up the LED mapping from LED_DRUM_INDEX.
    
    - For a contiguous mapping (a two-element list [start, end]),
      it returns (start, end, drum_type).
    - For a non-contiguous mapping (a list of LED indices),
      it returns (None, mapping_list, drum_type).
    - If the note isn’t mapped, it returns (None, None, None).
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
    # Horizontal wipe: center to sides using pixel_map
    map_length = len(pixel_map)
    center = map_length // 2
    for i in range(0, center):
        numbers = pixel_map.get(center + i, []) + pixel_map.get(center - i, [])
        for pixel_on in numbers:
            led_strip.setPixel(pixel_on, [255, 255, 255])
        led_strip.stripShow()
        for pixel_off in range(LED_COUNT):
            led_strip.setPixel(pixel_off, [0, 0, 0])
    led_strip.stripShow()

    # Horizontal wipe: sides to center
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
    # Additional animations can be added here.

def ledStripDaemon(midi_note_queue):
    led_strip = LedStrip(LED_COUNT, STRIP_GPIO_PIN)
    current_strip_values = initStripValues(LED_COUNT)
    colours = read_json_file(f"config/themes/{THEME_NAME}.json")

    while True:
        try:
            midi_hit = midi_note_queue.get_nowait()
            if midi_hit.get("animation"):
                runAnimation(led_strip, midi_hit["animation_type"])
                continue

            start, mapping, drum_type = get_led_indices_for_note(midi_hit["note"])
            if start is None and mapping is None:
                continue  # Skip unmapped notes

            # Determine the color, modifying brightness based on velocity.
            hit_color = colours.get(drum_type, [255, 255, 255])
            multiplier = midi_hit["velocity"] * ((100 / 127)) * 0.01
            pixel_color = [
                int(hit_color[0] * multiplier),
                int(hit_color[1] * multiplier),
                int(hit_color[2] * multiplier)
            ]

            if start is not None:
                # Contiguous mapping: update all LEDs in the range.
                end = mapping
                for pixel in range(end - start):
                    current_strip_values[pixel + start] = pixel_color
            else:
                # Non-contiguous mapping: update only the specified LED indices.
                for idx in mapping:
                    current_strip_values[idx] = pixel_color

            # Write out current_strip_values to the LED strip and fade them.
            for i in range(len(current_strip_values)):
                r, g, b = current_strip_values[i]
                # (Swap r and g if needed for your strip)
                color = [g, r, b]
                led_strip.setPixel(i, color)
                current_strip_values[i] = linearFade(r, g, b)
            led_strip.stripShow()

        except Exception as e:
            # On error (or if nothing is in the queue), continue updating fades.
            for i in range(len(current_strip_values)):
                r, g, b = current_strip_values[i]
                color = [g, r, b]
                led_strip.setPixel(i, color)
                current_strip_values[i] = linearFade(r, g, b)
            led_strip.stripShow()
