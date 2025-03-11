import json

MIDI_UNIT = 'UM-ONE:UM-ONE MIDI 1 20:0'

DRUMKIT_NAME = 'config/roland_td17_config.json' #TODO

with open(DRUMKIT_NAME) as json_file:
    DRUMKIT_CONFIG = json.load(json_file)

STRIP_GPIO_PIN = 18

LED_COUNT = 150

PAD_NOTES = [36, 38,48,45,43,27,40,50]

CYMBAL_NOTES = [49,55,52,57,51,53,59,26,22,44]

KICK_NOTE = 36

SNARE_NOTE = 38

ACCENT_NOTE_1 = 47

ACCENT_NOTE_2 = 58

MIDI_NOTE_INDEX = {
    36 : "kick",
    38 : "snare",
    40 : "snare",
    48 : "tom1",
    50 : "tom1",
    45 : "tom2",
    47 : "tom2",
    43 : "tom3",
    58 : "tom3",
    27 : "tom4",
    49 : "crash1",
    55 : "crash1",
    52 : "crash2",
    57 : "crash2",
    51 : "ride",
    53 : "ride",
    59 : "ride",
    26 : "hihat",
    22 : "hihat",
    44 : "hihat"
}

LED_DRUM_INDEX = {
    "kick": [74, 149],     # 76 LEDs
    "snare": [0, 13],      # 14 LEDs
    "tom1": [13, 22],      # 10 LEDs
    "tom2": [22, 30],      # 9 LEDs
    "tom3": [30, 38],      # 9 LEDs
    "tom4": [38, 51],      # 14 LEDs
    "ride": [51, 57],      # 7 LEDs
    "crash2": [57, 62],    # 6 LEDs
    "crash1": [62, 68],    # 7 LEDs
    "hihat": [68, 73]      # 6 LEDs
}

COLOURS = {
    "red": {
        "r": 255,
        "g": 0,
        "b": 0
    },
    "green": {
        "r": 0,
        "g": 255,
        "b": 0
    },
    "blue": {
        "r": 0,
        "g": 0,
        "b": 255
    },
    "purple": {
        "r": 200,
        "g": 0,
        "b": 200
    },
    "orange": {
        "r": 200,
        "g": 0,
        "b": 200
    },
    "yellow": {
        "r": 200,
        "g": 0,
        "b": 200
    },
    "cyan": {
        "r": 200,
        "g": 0,
        "b": 200
    }
}
