import os
import time
import random
import board
import busio
import adafruit_adxl34x
import pygame

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
