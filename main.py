import time
import multiprocessing
from utils.utils import read_json_file
from utils.midiUtils import setup_custom_midi_connection
from config.config import MIDI_UNIT, PAD_NOTES, CYMBAL_NOTES
import mido

def setup_midi_connection():
    MIDI_DEVICE_NAME = "UM-ONE MIDI 1"  # Change to "TD-17 MIDI 1" if needed

    available_ports = mido.get_input_names()
    if MIDI_DEVICE_NAME not in available_ports:
        print(f"Error: {MIDI_DEVICE_NAME} not found! Available devices: {available_ports}")
        exit(1)

    print(f"✅ MIDI Device Found: {MIDI_DEVICE_NAME}")
    return mido.open_input(MIDI_DEVICE_NAME)

def listen_to_midi_notes():
    time_counter = 0
    while time_counter < 600:
        if read_json_file("active_control_file.json")["app_state"] == "start":
            break
        time.sleep(0.5)
        time_counter += 1

    midi_connection = setup_midi_connection()

    print("🎵 Listening for MIDI drum hits...")

    # Listen for MIDI messages
    for msg in midi_connection:
        if msg.type == "note_on":
            if msg.note in PAD_NOTES or msg.note in CYMBAL_NOTES:
                print(f"🥁 Drum Hit! Note: {msg.note}, Velocity: {msg.velocity}")

if __name__ == "__main__":
    listen_to_midi_notes()
