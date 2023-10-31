import webrtcvad
import wave

# Set the sample rate to 16 kHz (must match your audio)
sample_rate = 16000
vad = webrtcvad.Vad(2)  # Aggressiveness: 0 (least aggressive) to 3 (most aggressive)

# Load a sample audio file (replace with your audio file)
audio_file = "Television.wav"

# Open the audio file
wav = wave.open(audio_file, 'rb')
frame_rate = wav.getframerate()
frame_size = int(frame_rate * 0.02)  # 20 ms frame size

# Read and process audio frames
while True:
    frame = wav.readframes(frame_size)
    if not frame:
        break
    if vad.is_speech(frame, sample_rate=sample_rate):
        print("Speech detected.")
