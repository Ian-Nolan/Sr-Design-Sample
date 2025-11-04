import sounddevice as sd 
import numpy as np 

print(sd.query_devices())

duration = 5  # seconds 
samplerate = 44100 

input_device = 1    # Replace with the index of your microphone (e.g., Fifine Microphone)
output_device = 1   # Replace with the index of your headphones

print("Recording...") 
audio = sd.rec(
    int(duration * samplerate),
    samplerate=samplerate,
    channels=1,
    dtype='float32',
    device=(input_device, output_device)  # specify both input and output
)
sd.wait() 

print("Playing back...") 
sd.play(audio, samplerate, device=output_device) 
sd.wait()
