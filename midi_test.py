import mido

mido.get_input_names() # Get connected midi device names

with mido.open_input('<midi_device_name>') as inport:
    for message in inport:
        print(message)