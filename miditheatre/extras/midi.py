import mido

def send_midi_message(model):
    """
    Sends a MIDI note_on message to all available MIDI outputs using the information
    from the given model instance.
    
    The model should have the following attributes:
      - channel: MIDI channel (0-15)
      - key: MIDI note number (0-127)
      - value: Velocity (0-127)
    """
    # Create the MIDI message
    msg = mido.Message('note_on',
                       channel=model.channel,
                       note=model.key,
                       velocity=model.value)
    
    # Get all available MIDI output names
    output_names = mido.get_output_names()
    
    # Send the message to each available MIDI output
    for output_name in output_names:
        with mido.open_output(output_name) as outport:
            outport.send(msg)