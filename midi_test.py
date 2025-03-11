import mido

# Find and select the Roland MIDI device
MIDI_DEVICE_NAME = "UM-ONE:UM-ONE MIDI 1 20:0"  # Change to "TD-17 MIDI 1" if detected under that name

available_ports = mido.get_input_names()
if MIDI_DEVICE_NAME not in available_ports:
    print(f"Error: {MIDI_DEVICE_NAME} not found! Available devices: {available_ports}")
    exit(1)

midi_input = mido.open_input(MIDI_DEVICE_NAME)

print(f"🎵 Listening for MIDI hits on {MIDI_DEVICE_NAME}...")

# Listen for MIDI messages
for msg in midi_input:
    if msg.type == "note_on":
        print(f"🥁 Drum Hit! Note: {msg.note}, Velocity: {msg.velocity}")
