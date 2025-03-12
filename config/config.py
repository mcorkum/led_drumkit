import json

MIDI_UNIT = 'UM-ONE:UM-ONE MIDI 1 20:0'
STRIP_GPIO_PIN = 18
LED_COUNT = 150

# Updated lists so that all intended drum hits (including rims) are processed.
PAD_NOTES = [36, 38, 40, 48, 50, 45, 47, 43, 58]
CYMBAL_NOTES = [44, 26, 46, 51, 53, 59, 55, 49]

# Updated MIDI note mapping based on your new mapping:
MIDI_NOTE_INDEX = {
    36: "kick",         # Bass Drum
    44: "hihat",        # Hat Pedal
    26: "hihat",        # Hi Hat
    46: "hihat",        # Hi Hat Edge
    38: "snare",        # Snare
    40: "snare",        # Snare Rim
    48: "tom1",         # Tom 1 (head)
    50: "tom1",         # Tom 1 - Rim
    45: "tom2",         # Tom 2 (head)
    47: "tom2",         # Tom 2 - Rim
    43: "tom3",         # Floor Tom (head)
    58: "tom3",         # Floor Tom - Rim
    51: "ride",         # Ride (head)
    53: "ride",         # Ride Bell
    59: "crash2",       # Ride Crash / Crash 2 (separate zone)
    55: "crash1",       # Crash (dedicated)
    49: "crash1"        # Crash Bell
}

# Updated LED zone mapping for only these drums.
# Here, the LED strip is partitioned into zones that sum to 150 LEDs.
# You can adjust these ranges as needed for your physical layout.
# LED_DRUM_INDEX = {
#     "snare":   [0, 14],    # 14 LEDs for snare
#     "tom1":    [14, 24],   # 10 LEDs for Tom 1 (head & rim)
#     "tom2":    [24, 33],   # 9 LEDs for Tom 2 (head & rim)
#     "tom3":    [33, 48],   # 15 LEDs for Floor Tom (head & rim)
#     "ride":    [48, 54],   # 6 LEDs for Ride
#     "crash2":  [54, 64],   # 10 LEDs for Ride Crash / Crash 2
#     "crash1":  [64, 71],   # 7 LEDs for Crash (dedicated)
#     "hihat":   [71, 77],   # 6 LEDs for Hi Hat (Hat Pedal/Hi Hat/Edge)
#     "kick":    [77, 150]   # 73 LEDs for Bass Drum (kick)
# }

LED_DRUM_INDEX = {
    "kick": [0, 75],
    "snare": [75, 150]
}

COLOURS = {
    "red": {"r": 255, "g": 0, "b": 0},
    "green": {"r": 0, "g": 255, "b": 0},
    "blue": {"r": 0, "g": 0, "b": 255},
    "purple": {"r": 200, "g": 0, "b": 200},
}
