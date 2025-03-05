import mido

# List available MIDI input devices
print("Available MIDI inputs:", mido.get_input_names())

# Open the first available MIDI input
midi_input = mido.open_input(mido.get_input_names()[0])

print("Listening for MIDI drum hits...")

# Listen for MIDI messages
for msg in midi_input:
    if msg.type == 'note_on':  # Detect drum hits
        print(f"Drum Hit Detected! Note: {msg.note} Velocity: {msg.velocity}")
