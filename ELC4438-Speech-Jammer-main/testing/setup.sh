#!/bin/sh

pip install pyalsaaudio      #als audio device
sleep 1
pip install pydub            #decode mp3 files
sleep 1
sudo apt-get install ffmpeg  #back-end decode
sleep 1
pip install numpy            #for data manipulation

