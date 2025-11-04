from flask import Flask, render_template, request, redirect, url_for
from threading import Thread
from pyo import *
import time

# Flask app
app = Flask(__name__)

# Globals for UI state
counter = 0
volume = 0.5  # Pyo uses 0.0–1.0 scale for volume
pitch_semitones = 0  # Pitch shift in semitones

# === Pyo setup ===
print("Available devices:")
pa_list_devices()

INPUT_DEVICE = 1    # Set to your mic device index
OUTPUT_DEVICE = 1   # Set to your DigiAMP+ output device index

# Initialize Pyo server
s = Server(sr=44100, buffersize=512, nchnls=1, audio='portaudio')
s.setInputDevice(INPUT_DEVICE)
s.setOutputDevice(OUTPUT_DEVICE)

try:
    s.boot()
except Exception as e:
    print("Failed to boot server. Check device indices.")
    raise

# Set up mic input and pitch shifter
mic = Input(chnl=0)
pitch = Harmonizer(mic, transpo=pitch_semitones, feedback=0.0, mul=volume)
pitch.out()

# Flask routes
@app.route('/')
def index():
    return render_template('index.html', count=counter, volume=int(volume*100), pitch=pitch_semitones)

@app.route('/increment', methods=['POST'])
def increment():
    global counter
    counter += 1
    print("Current counter number =", counter)
    return redirect(url_for('index'))

@app.route('/set_volume', methods=['POST'])
def set_volume():
    global volume
    try:
        new_volume = float(request.form.get('volume', 50)) / 100.0  # scale to 0.0–1.0
        volume = max(0.0, min(new_volume, 1.0))
        pitch.setMul(volume)
        print(f"Volume set to {volume*100:.0f}%")
    except Exception as e:
        print("Failed to set volume:", e)
    return redirect(url_for('index'))

@app.route('/set_pitch', methods=['POST'])
def set_pitch():
    global pitch_semitones
    try:
        pitch_semitones = float(request.form.get('pitch', 0))
        pitch.setTranspo(pitch_semitones)
        print(f"Pitch shift set to {pitch_semitones} semitones")
    except Exception as e:
        print("Failed to set pitch:", e)
    return redirect(url_for('index'))

# Background thread to run Pyo server
def audio_thread():
    print("Starting Pyo audio server...")
    s.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping audio.")
        s.stop()

if __name__ == '__main__':
    # Start audio in background thread
    t = Thread(target=audio_thread)
    t.daemon = True
    t.start()

    # Start Flask app
    app.run(host='0.0.0.0', port=5000)
