from pyo import *
import time
import threading

# Print devices
print("Available devices:")
pa_list_devices()

# Device indices
INPUT_DEVICE = 1
OUTPUT_DEVICE = 0

# Create and configure server
s = Server(sr=44100, buffersize=512, nchnls=1, audio='portaudio')
s.setInputDevice(INPUT_DEVICE)
s.setOutputDevice(OUTPUT_DEVICE)

try:
    s.boot()
except Exception as e:
    print("Failed to boot server. Check device indices.")
    raise

s.start()

# Mic input and pitch shifting
try:
    mic = Input(chnl=0)
    pitch = Harmonizer(mic, transpo=0, feedback=.7)
    pitch.out()
except Exception as e:
    print("Error setting up audio objects.")
    s.stop()
    raise

# Function to listen for pitch commands in another thread
def pitch_control():
    print("\nPitch control ready. Type a number (e.g. 4, -3) and press ENTER to change pitch in semitones.")
    print("Type 'q' to quit.")
    while True:
        cmd = input("Transpo: ").strip()
        if cmd.lower() == 'q':
            print("Exiting pitch control...")
            break
        try:
            new_transpo = int(cmd)
            pitch.setTranspo(new_transpo)
            print(f"Pitch shifted to {new_transpo:+d} semitone(s).")
        except ValueError:
            print("Invalid input. Enter an integer or 'q' to quit.")

# Start pitch control thread
control_thread = threading.Thread(target=pitch_control)
control_thread.daemon = True
control_thread.start()

# Main loop
print("System live. Adjust pitch using the terminal.")
try:
    while control_thread.is_alive():
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopping audio.")
    s.stop()
