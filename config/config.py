import json

MIDI_UNIT = 'UM-ONE:UM-ONE MIDI 1 20:0'
STRIP_GPIO_PIN = 18
LED_COUNT = 150

# Theme
THEME_NAME = "neon"
IDLE_ANIMATION = "moving"  # or "theater", "breathing",  "rainbow", "moving"

# Updated lists so that all intended drum hits (including rims) are processed.
PAD_NOTES = [36, 38, 40, 48, 50, 45, 47, 43, 58]
CYMBAL_NOTES = [44, 26, 22, 46, 51, 53, 59, 55, 49]

# Updated MIDI note mapping based on your new mapping:
MIDI_NOTE_INDEX = {
    36: "kick",         # Bass Drum
    44: "hihat",        # Hat Pedal
    22: "hihat",        # Hi Hat closed
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


LED_DRUM_INDEX = {
    "kick":    [0, 9, 18, 27, 36, 45, 54, 63, 72, 81, 90, 99, 108, 117, 126, 135, 138, 141, 144, 147],
    "snare":   [1, 10, 19, 28, 37, 46, 55, 64, 73, 82, 91, 100, 109, 118, 127, 136, 139, 142, 145, 148],
    "hihat":   [2, 11, 20, 29, 38, 47, 56, 65, 74, 83, 92, 101, 110, 119, 128, 137, 140, 143, 146, 149],
    "tom1":    [3, 12, 21, 30, 39, 48, 57, 66, 75, 84, 93, 102, 111, 120, 129],
    "tom2":    [4, 13, 22, 31, 40, 49, 58, 67, 76, 85, 94, 103, 112, 121, 130],
    "tom3":    [5, 14, 23, 32, 41, 50, 59, 68, 77, 86, 95, 104, 113, 122, 131],
    "ride":    [6, 15, 24, 33, 42, 51, 60, 69, 78, 87, 96, 105, 114, 123, 132],
    "crash1":  [7, 16, 25, 34, 43, 52, 61, 70, 79, 88, 97, 106, 115, 124, 133],
    "crash2":  [8, 17, 26, 35, 44, 53, 62, 71, 80, 89, 98, 107, 116, 125, 134]
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

# Example of only Kick and Snare
# LED_DRUM_INDEX = {
#     "kick": [0, 75],
#     "snare": [75, 150]
# }

COLOURS = {
    "red": {"r": 255, "g": 0, "b": 0},
    "green": {"r": 0, "g": 255, "b": 0},
    "blue": {"r": 0, "g": 0, "b": 255},
    "purple": {"r": 200, "g": 0, "b": 200},
}
