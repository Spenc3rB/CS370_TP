import threading
import random
import os
import time
import busio
import board
import adafruit_adxl34x
import pygame
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'sounds'
ALLOWED_EXTENSIONS = {'mp3'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sound_files = []  # Global list to hold the available sound files
lock = threading.Lock()  # Lock to ensure thread-safe access to the list of sound files


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def update_sound_files():
    global sound_files
    while True:
        with lock:
            sound_files = [file for file in os.listdir(app.config['UPLOAD_FOLDER']) if file.endswith(".mp3")]
        time.sleep(5)  # Update the list of sound files every 5 seconds


def play_random_audio():
    pygame.mixer.init()
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    accelerometer.enable_tap_detection(tap_count=1, duration=50, threshold=50, latency=20, window=255)

    while True:
        print("%f %f %f" % accelerometer.acceleration)
        print("Accelerometer events:", accelerometer.events)
        time.sleep(0.5)
        if accelerometer.events['tap']:
            with lock:
                if sound_files:
                    selected_audio = random.choice(sound_files)
                    pygame.mixer.music.set_volume(1.0) # ensure the volume is always at 100%
                    pygame.mixer.music.load(os.path.join(app.config['UPLOAD_FOLDER'], selected_audio))
                    pygame.mixer.music.play()
        time.sleep(0.5)

@app.route('/')
def index():
    return render_template('index.html', sounds=sound_files)


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/delete/<filename>', methods=['POST'])
def delete_sound(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('index'))
    else:
        return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    sound_thread = threading.Thread(target=update_sound_files)
    sound_thread.daemon = True
    sound_thread.start()

    audio_thread = threading.Thread(target=play_random_audio)
    audio_thread.daemon = True
    audio_thread.start()

    app.run(host='0.0.0.0', port=6969, debug=True)
