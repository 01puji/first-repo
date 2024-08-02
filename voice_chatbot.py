import os
import openai
import pyaudio
import threading
import queue
import wave
import requests
from pathlib import Path

api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("API key is not set. Please set the OPENAI_API_KEY environment variable.")
else:
    openai.api_key = api_key

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 10

def save_audio_file(filename, audio_data):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audio_data)

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "당신은 질문에 대답하고 건의를 제공할 준비가 되어 있는 기계 엔지니어입니다."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def text_to_speech(text):
    try:
        url = "https://api.openai.com/v1/audio/speech"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "tts-1",
            "voice": "echo",
            "input": text,
            "response_format": "wav",
        }

        response = requests.post(url, headers=headers, json=data)

        response.raise_for_status()

        return response.content
    except Exception as e:
        print(f"Error during TTS: {e}")
        return None


def play_audio(audio_data):
    try:
        temp_audio_path = "response.wav"
        with open(temp_audio_path, "wb") as f:
            f.write(audio_data)

        p = pyaudio.PyAudio()
        wf = wave.open(temp_audio_path, "rb")

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)
        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)

        data = wf.readframes(CHUNK)
        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()

        Path(temp_audio_path).unlink()

    except Exception as e:
        print(f"Error during audio playback: {e}")


def process_audio_stream(audio_queue):
    while True:
        if not audio_queue.empty():
            audio_data = b''.join([audio_queue.get() for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS))])
            save_audio_file("temp.wav", audio_data)

            try:
                with wave.open("temp.wav", "rb") as audio_file:
                    params = audio_file.getparams()
                    if params.nchannels != CHANNELS or params.sampwidth != 2 or params.framerate != RATE:
                        raise ValueError("The parameters df the audio file do not match expectations")

                with open("temp.wav", "rb") as audio_file:
                    result = openai.Audio.transcribe("whisper-1", audio_file)
                    recognized_text = result['text']
                    print("Recognized Text:", recognized_text)

                    response_text = chat_with_gpt(recognized_text)
                    print("ChatGPT Response:", response_text)

                    response_audio = text_to_speech(response_text)
                    print("Playing response...")
                    play_audio(response_audio)

            except Exception as e:
                print(f"Error during transcription or playback: {e}")

def audio_callback(in_data, frame_count, time_info, status):
    audio_queue.put(in_data)
    return (None, pyaudio.paContinue)

audio_queue = queue.Queue()
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=audio_callback)

processing_thread = threading.Thread(target=process_audio_stream, args=(audio_queue,))
processing_thread.start()

print("Recording... Press Enter to stop.")
try:
    while True:
        pass
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    audio.terminate()

print("Stopped.")

