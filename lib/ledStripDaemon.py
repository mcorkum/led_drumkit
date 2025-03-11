from lib.ledStrip import *
from utils.utils import *
from config.config import *
from config.pixelMap import *
from animations.hitAnimations import *

def getStripSegmentIndex(note):
    try:
        start = DRUMKIT_CONFIG[str(note)]["led_index"][0]
        end = DRUMKIT_CONFIG[str(note)]["led_index"][1]
        print(f"DEBUG: getStripSegmentIndex({note}) → LEDs {start} to {end}")
        return start, end
    except KeyError:
        print(f"ERROR: No LED mapping found for MIDI Note {note}")
        return None, None  # Prevents crashes

def initStripValues(led_count):
    current_strip_values = {}
    for i in range(LED_COUNT):
        current_strip_values[i] = [0, 0, 0]
    return current_strip_values

def ledStripDaemon(midi_note_queue):
    led_strip = LedStrip(LED_COUNT, STRIP_GPIO_PIN)
    current_strip_values = initStripValues(LED_COUNT)
    colours = read_json_file('config/accentColours.json')

    while True:
        try:
            midi_hit = midi_note_queue.get_nowait()
            print(f"DEBUG: Processing MIDI Note {midi_hit['note']} with velocity {midi_hit['velocity']}")

            if midi_hit["animation"]:
                runAnimation(led_strip, midi_hit["animation_type"])
                continue

            start, end = getStripSegmentIndex(midi_hit["note"])
            if start is None or end is None:
                continue  # Skip if no LED mapping

            # Get drum type and color
            drum_type = DRUMKIT_CONFIG.get(str(midi_hit["note"]), {}).get("drum_type", "unknown")
            if drum_type == "unknown":
                print(f"ERROR: No drum type found for MIDI Note {midi_hit['note']}")
                continue

            hit_color = colours.get(drum_type, {"r": 255, "g": 255, "b": 255})  # Default to white
            print(f"DEBUG: Drum Type: {drum_type}, Color: {hit_color}")

            # Modify brightness based on velocity
            multiplier = midi_hit["velocity"] * ((100 / 127)) * 0.01
            pixel_color = [int(hit_color["r"] * multiplier), int(hit_color["g"] * multiplier), int(hit_color["b"] * multiplier)]
            print(f"DEBUG: Adjusted Color for Velocity {midi_hit['velocity']}: {pixel_color}")

            # Store and apply color
            for pixel in range(start, end):
                current_strip_values[pixel] = pixel_color
                print(f"DEBUG: Setting LED {pixel} to {pixel_color}")

            led_strip.stripShow()
        except Exception as e:
            print(f"ERROR in ledStripDaemon: {e}")
