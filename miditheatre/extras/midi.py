from rtmidi2 import MidiIn, NOTEON, CC, splitchannel
import keyboard
def send_midi_message(channel:int, key:int, value:int, length:float=1.0):
    """
    Sends a MIDI note_on message to all available MIDI outputs using the information
    from the given model instance.
    
    The model should have the following attributes:
      - channel: MIDI channel (0-15)
      - key: MIDI note number (0-127)
      - value: Velocity (0-127)
    """
    msg = Message('note_on', channel=channel)
                      #  note=key,
                      #  velocity=value,
                      #  time=length
                      #  )
    conn = MidiConnector('/dev/serial0', timeout=5)
    available_ports = pm_list_devices()
    for port in available_ports:
      # Create the MIDI message
      s = Server()
      s.setMidiOutputDevice(99)

      # Then boot the Server.
      s.boot()

    
    
    # Get all available MIDI output names
    output_names = get_output_names()
    MultiPort(output_names)
    # Send the message to each available MIDI output
    for output_name in output_names:
        with mido.open_output(output_name) as outport:
            outport.send(msg)