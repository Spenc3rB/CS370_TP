from flask import Flask, render_template, request, redirect, url_for
import os
import time
import random
import board
import busio
import adafruit_adxl34x
import pygame
from threading import Thread

app = Flask(__name__)

UPLOAD_FOLDER = 'sounds'
ALLOWED_EXTENSIONS = {'mp3'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('index.html')

def play_random_audio():
    # Initialize Pygame mixer for audio
    pygame.mixer.init()

    # Function to get list of audio files from the "sounds" subdirectory
    def get_audio_files(directory):
        audio_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".mp3"):
                    audio_files.append(os.path.join(root, file))
        return audio_files

    # Directory containing audio files
    audio_directory = "sounds"

    # Get list of audio files
    audio_files = get_audio_files(audio_directory)

    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    accelerometer.enable_tap_detection(tap_count=1, duration=50, threshold=50, latency=20, window=255)

    while True:
        print("%f %f %f" % accelerometer.acceleration)
        print("Accelerometer events:", accelerometer.events)
        time.sleep(0.5)
        if accelerometer.events['tap'] == True:
            # If motion is detected, randomly select an audio file to play
            selected_audio = random.choice(audio_files)
            pygame.mixer.music.load(selected_audio)
            pygame.mixer.music.play()

        time.sleep(0.5)

if __name__ == '__main__':
    # Start the background process for playing random audio
    audio_thread = Thread(target=play_random_audio)
    audio_thread.start()

    # Start the Flask server
    app.run(host='0.0.0.0', port=6969, debug=True)
