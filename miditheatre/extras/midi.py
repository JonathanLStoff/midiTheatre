import rtmidi
import os
import time
import traceback
import threading
from django.conf import settings
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF
from rtmidi.midiutil import get_api_from_environment

def send_midi_message(channel:int, key:int, value:int, length:float=1.0, ports:list[str]=[])-> list[dict[str,str]]:
    """
    Sends a MIDI note_on message to all available MIDI outputs using the information
    from the given model instance.
    
    The model should have the following attributes:
      - channel: MIDI channel (0-15)
      - key: MIDI note number (0-127)
      - value: Velocity (0-127)
    """
    if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miditheatre.settings")
    error_list:list[dict[str,str]] = []
    try:
        msg_start:list[int] = [NOTE_ON + channel, key, value]
        msg_stop:list[int] = [NOTE_OFF + channel, key, value]
                        #  time=length
                        #  )
        if ports == []:
            ports:list[str] = list_output_ports()
        if settings.MIDI_PORT in ports:
            ports = [settings.MIDI_PORT]
        def send_to_port(port:str, msg_start:list[int]):
            try:
                midiout = rtmidi.MidiOut(get_api_from_environment())
                midiout.open_port(name=port)
                midiout.send_message(msg_start)
                midiout.close_port()
            except Exception as:
                error_list.append({str(port)+"_stp": traceback.format_exc()})
        def stop_midi(port:str, msg_stop:list[int]):
            try:
                midiout = rtmidi.MidiOut(get_api_from_environment())
                midiout.open_port(name=port)
                midiout.send_message(msg_stop)
                midiout.close_port()
                del midiout
            except Exception as:
                error_list.append({str(port)+"_stp": traceback.format_exc()})
            
        for port in ports:
            try:
                send_to_port(str(port), msg_start)
            except Exception as:
                error_list.append({port: f"error: {traceback.format_exc()}"})
        time.sleep(length)
        for port in ports:
            try:
                stop_midi(str(port), msg_stop)
            except Exception:
                error_list.append({port: f"error: {traceback.format_exc()}"})
    except Exception as e:
        error_list.append({'send_midi_message': traceback.format_exc()})
    return error_list


def list_available_ports(midiio=None)->list[str]:
    """List MIDI ports given or available on given MIDI I/O instance."""
    ports:list[str] = midiio.get_ports()

    if isinstance(ports, list):
        return ports
    else:
        return []

def list_output_ports(api=rtmidi.API_UNSPECIFIED)->list[str]:
    """List available MIDI output ports.

    Optionally the RtMidi API can be passed with the ``api`` argument. If not
    it will be determined via the ``get_api_from_environment`` function.

    Exceptions:

    ``rtmidi.SystemError``
        Raised when RtMidi backend initialization fails.

    """
    midiout = rtmidi.MidiOut(get_api_from_environment(api))
    print("about to check for ports")
    all_ports:list = list_available_ports(midiio=midiout)
    midiout.delete()
    return all_ports
    
if __name__ == '__main__':
    error_message = send_midi_message(1, 60, 127, 1.0)
    print(error_message)
    badness = []
    for error in error_message:
        for key, value in error.items():
            badness.append(key)
        
    print(badness)
    print("Done")