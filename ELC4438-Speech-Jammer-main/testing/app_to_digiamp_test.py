from flask import Flask, render_template, request, redirect, url_for
import threading
import alsaaudio
from pydub import AudioSegment
import time

app = Flask(__name__)

counter = 0
volume = 50  # Initial volume

# Detect mixers
mixer_list = alsaaudio.mixers()
print("Available mixers:", mixer_list)

if mixer_list:
    mixer_name = mixer_list[0]
    mixer = alsaaudio.Mixer(mixer_name)
    print(f"Using mixer: {mixer_name}")
else:
    raise RuntimeError("No ALSA mixers found!")

# Load audio file
audio = AudioSegment.from_file("04. Thriller.mp3", format="mp3")
pcm = alsaaudio.PCM(type=alsaaudio.PCM_PLAYBACK)
pcm.setchannels(audio.channels)
pcm.setrate(audio.frame_rate)
pcm.setformat(alsaaudio.PCM_FORMAT_S16_LE)
pcm.setperiodsize(1024)

def play_audio():
    while True:
        print("Playing MP3 through DigiAMP+")
        data = audio.raw_data
        chunk_size = 1024
        offset = 0
        while offset < len(data):
            pcm.write(data[offset:offset + chunk_size])
            offset += chunk_size
            time.sleep(0.001)
        print("Finished playback. Restarting...")

@app.route('/')
def index():
    return render_template('index.html', count=counter, volume=volume)

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
        volume = int(request.form.get('volume', 50))
        mixer.setvolume(volume)
        print(f"Volume set to {volume}%")
    except ValueError:
        volume = 50
        mixer.setvolume(volume)
    return redirect(url_for('index'))

if __name__ == '__main__':
    try:
        audio_thread = threading.Thread(target=play_audio)
        audio_thread.daemon = True
        audio_thread.start()
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print("Error:", e)
