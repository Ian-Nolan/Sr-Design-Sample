import alsaaudio
from pydub import AudioSegment

fileName = input("Enter audio file name: ")
#fileName = "04. Thriller.mp3"
audio = AudioSegment.from_file(fileName, format = "mp3")

#play back setup
pcm = alsaaudio.PCM(type=alsaaudio.PCM_PLAYBACK)
pcm.setchannels(audio.channels)
pcm.setrate(audio.frame_rate)
pcm.setformat(alsaaudio.PCM_FORMAT_S16_LE)
pcm.setperiodsize(1024)

print(f"Playing {fileName} through DigiAMP+")

data = audio.raw_data
#smaller for real time
chunk_size = 1024 # what is the sweets spot for speed and latency
offset = 0

while offset < len(data):
    pcm.write(data[offset:offset + chunk_size])
    offset += chunk_size

print("Finished playback.")

