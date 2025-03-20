import time
import threading
from lib.ledStrip import *
from utils.utils import *
from config.config import LED_COUNT, STRIP_GPIO_PIN, MIDI_NOTE_INDEX, LED_DRUM_INDEX, THEME_NAME
from config.pixelMap import *
from animations.hitAnimations import *

# Global idle control variables
idle_thread = None
idle_stop = threading.Event()

def get_led_indices_for_note(note):
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

def theaterChaseRainbowCycle(led_strip, wait_ms=50, cycles=1):
    num_pixels = led_strip.strip.numPixels()
    for j in range(256 * cycles):
        if idle_stop.is_set():
            return
        for q in range(3):
            for i in range(0, num_pixels, 3):
                led_strip.strip.setPixelColor(i + q, led_strip.wheel((i + j) % 255))
            led_strip.strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, num_pixels, 3):
                led_strip.strip.setPixelColor(i + q, 0)
    led_strip.strip.show()

def idle_animation(led_strip):
    """
    Runs the theaterChaseRainbow animation continuously in short cycles
    until idle_stop is set (i.e. until a MIDI hit is detected).
    """
    while not idle_stop.is_set():
        theaterChaseRainbowCycle(led_strip, wait_ms=50, cycles=1)
        # You can insert a brief pause between cycles if desired:
        time.sleep(0.1)

def ledStripDaemon(midi_note_queue):
    global idle_thread, idle_stop
    led_strip = LedStrip(LED_COUNT, STRIP_GPIO_PIN)
    current_strip_values = initStripValues(LED_COUNT)
    colours = read_json_file(f"config/themes/{THEME_NAME}.json")
    
    last_midi_time = time.time()
    
    while True:
        try:
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
                    continue  # Skip unmapped notes
                
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
            
            # Change the idle timeout from 10 seconds to 5 seconds.
            if time.time() - last_midi_time > 5:
                if idle_thread is None or not idle_thread.is_alive():
                    idle_thread = threading.Thread(target=idle_animation, args=(led_strip,))
                    idle_thread.start()
                    # Reset last_midi_time to avoid repeated triggers
                    last_midi_time = time.time()
            
            # Update the LED strip: apply fades and refresh.
            for i in range(len(current_strip_values)):
                r, g, b = current_strip_values[i]
                color = [g, r, b]  # Adjust ordering if needed.
                led_strip.setPixel(i, color)
                current_strip_values[i] = linearFade(r, g, b)
            led_strip.stripShow()
            
        except Exception as e:
            # If there's an exception, still update the LED strip.
            for i in range(len(current_strip_values)):
                r, g, b = current_strip_values[i]
                color = [g, r, b]
                led_strip.setPixel(i, color)
                current_strip_values[i] = linearFade(r, g, b)
            led_strip.stripShow()

