import pyaudio
import webrtcvad
import speech_recognition as sr
from gtts import gTTS
import pygame
import threading

# Global variables
audio_buffer = []
recognizer = sr.Recognizer()
vad = webrtcvad.Vad()
vad.set_mode(1)  # Aggressiveness: 0 (least aggressive) to 3 (most aggressive)
listening = False

def audio_stream_callback(in_data, frame_count, time_info, status):
    global audio_buffer, listening
    if status == pyaudio.paComplete:
        listening = False
    else:
        listening = True

    if listening:
        audio_buffer.append(in_data)
    return (None, pyaudio.paContinue)

def process_audio():
    global audio_buffer, listening
    while True:
        if audio_buffer and not listening:
            audio_data = b''.join(audio_buffer)
            audio_buffer = []

            try:
                recognized_text = recognizer.recognize_google(audio_data)
                print("You said:", recognized_text)
                # Add logic to process recognized_text and generate responses
                response = "You said: " + recognized_text
                tts = gTTS(text=response)
                tts.save("response.mp3")
                pygame.mixer.music.load("response.mp3")
                pygame.mixer.music.play()
            except sr.UnknownValueError:
                pass

if __name__ == "__main__":
    pygame.mixer.init()
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=320,
                    stream_callback=audio_stream_callback)

    stream.start_stream()

    processing_thread = threading.Thread(target=process_audio)
    processing_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        listening = False
        audio_buffer.clear()
        stream.stop_stream()
        stream.close()
        p.terminate()
        processing_thread.join()
