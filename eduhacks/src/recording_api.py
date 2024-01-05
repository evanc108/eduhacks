from flask import Flask, render_template, request, jsonify
import sounddevice as sd
import numpy as np
import wave
import os
import threading

app = Flask(__name__, template_folder=os.path.abspath('templates'))

# Global variables to store the audio data and control recording
recording_data = None
recording_active = False
sampling_rate = 44100  # You can adjust this based on your requirements

@app.route('/')
def index():
    return render_template('frontpage_ui.html')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording_data, recording_active

    # Set recording flag to True
    recording_active = True
    recording_data = []

    # Start recording in a separate thread
    recording_thread = threading.Thread(target=start_recording_thread)
    recording_thread.start()

    return jsonify({"status": "Recording started"})

def start_recording_thread():
    global recording_data, recording_active
    with sd.InputStream(callback=callback):
        while recording_active:
            sd.sleep(100)  # Adjust the sleep duration based on your needs

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global recording_active
    recording_active = False

    global recording_data
    if recording_data:
        save_wav('recorded_audio.wav', np.concatenate(recording_data))
        recording_data = None
        return jsonify({"status": "Recording stopped and saved"})
    else:
        return jsonify({"status": "No recording data available"})

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    recording_data.append(indata.copy())

def save_wav(file_path, audio_data):
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sampling_rate)
        wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())

if __name__ == '__main__':
    app.run(debug=True, port=5001)
