# '''

# #--- Steve Cox --- 1/10/19
# # Copyright (c) Stef van der Struijk
# # License: GNU Lesser General Public License

# # Modified code to play sound from buffer recording
# # Added code to wait till sound is finished play so no echo occurs

# # Modification of:
# # https://github.com/wiseman/py-webrtcvad (MIT Copyright (c) 2016 John Wiseman)
# # https://github.com/wangshub/python-vad (MIT Copyright (c) 2017 wangshub)

# Requirements:
# + pyaudio - `pip install pyaudio`
# + py-webrtcvad - `pip install webrtcvad`
# '''
# import webrtcvad
# import collections
# import sys
# import signal
# import pyaudio

# from array import array
# from struct import pack
# import wave
# import time


# # FORMAT: This tells the program how to understand the sound data it's going to work with. It's like telling it whether the audio is in a specific language that it can understand. In this case, it's set to paInt16, which means the audio is in a format called 16-bit PCM. Think of it as a specific language for sound.

# # CHANNELS: Audio can have different "channels" like left and right in headphones. Here, it's set to 1, which means it's only listening to one channel of audio. If it were 2, it would listen to both left and right.

# # RATE: This is how fast the program is going to listen to sound. It's like the number of pictures a camera takes per second. In this case, it's set to 16000, which is 16,000 "pictures" of sound every second.

# # CHUNK_DURATION_MS: Sound is divided into small pieces called "chunks" so the program can work with it. This setting determines how long each chunk is in milliseconds (ms). It can be set to 10, 20, or 30 ms. It's like cutting a long video into shorter clips.

# # PADDING_DURATION_MS: This is like extra time added to make sure the program doesn't stop listening too soon. It's set to 1500 ms, which is 1.5 seconds. So, even after it thinks you stopped talking, it keeps listening for a bit longer just to be sure.

# # CHUNK_SIZE: This calculates how big each chunk should be in terms of the number of "pictures" (samples) it should contain. It's based on the RATE and CHUNK_DURATION_MS. Think of it as deciding how many frames to capture in each clip.

# # CHUNK_BYTES: This tells us how much space each chunk takes up in memory. It's 16 bits (2 bytes) for each sample, and there are CHUNK_SIZE samples in each chunk. So, it's like knowing how many pages are in a book and how much space each page needs.

# # NUM_PADDING_CHUNKS: It calculates how many chunks should be used for that extra time we talked about in point 5. It's like deciding how many extra video clips you want to be absolutely sure you capture everything.


# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 16000
# CHUNK_DURATION_MS = 30       # supports 10, 20 and 30 (ms)
# PADDING_DURATION_MS = 1500   # 1 sec jugement
# CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)  # chunk to read
# CHUNK_BYTES = CHUNK_SIZE * 2  # 16bit = 2 bytes, PCM
# NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)

# #--- Steve Cox
# NUM_WINDOW_CHUNKS = int(240 / CHUNK_DURATION_MS)
# #NUM_WINDOW_CHUNKS = int(400 / CHUNK_DURATION_MS)  # 400 ms/ 30ms  ge

# NUM_WINDOW_CHUNKS_END = NUM_WINDOW_CHUNKS * 2
# START_OFFSET = int(NUM_WINDOW_CHUNKS * CHUNK_DURATION_MS * 0.5 * RATE)

# vad = webrtcvad.Vad(1)

# #------ Steve Cox
# # One time Pygame init

# import pygame
# pygame.mixer.pre_init(RATE, -16, CHANNELS, 2048) # setup mixer to avoid sound lag
# pygame.mixer.init()
# pygame.init()

# #-------------------------- 

# pa = pyaudio.PyAudio()
# stream = pa.open(format=FORMAT,
#                  channels=CHANNELS,
#                  rate=RATE,
#                  input=True,
#                  start=False,
#                  # input_device_index=2,
#                  frames_per_buffer=CHUNK_SIZE)


# got_a_sentence = False
# # normalize function helps make sure the sound we record isn't too loud or too quiet. 
# # It listens to the sound, checks how loud it is, and adjusts it to a comfortable volume level. 
# # It's like having a volume knob for our recorded sound to make sure it sounds good when we play it back.
# def normalize(snd_data):
#     "Average the volume out"
#     MAXIMUM = 32767  # 16384
#     times = float(MAXIMUM) / max(abs(i) for i in snd_data)
#     r = array('h')
#     for i in snd_data:
#         r.append(int(i * times))
#     return r


# while True:
#     ring_buffer = collections.deque(maxlen=NUM_PADDING_CHUNKS)
#     triggered = False
#     voiced_frames = []
#     ring_buffer_flags = [0] * NUM_WINDOW_CHUNKS
#     ring_buffer_index = 0

#     ring_buffer_flags_end = [0] * NUM_WINDOW_CHUNKS_END
#     ring_buffer_index_end = 0
#     buffer_in = ''
#     # WangS
#     raw_data = array('h')
#     index = 0
#     start_point = 0
#     StartTime = time.time()
#     print("* recording: ")
#     stream.start_stream()

#     while not got_a_sentence:
#         chunk = stream.read(CHUNK_SIZE)
#         # add WangS
#         raw_data.extend(array('h', chunk))
#         index += CHUNK_SIZE
#         TimeUse = time.time() - StartTime

#         active = vad.is_speech(chunk, RATE)

#         sys.stdout.write('1' if active else '_')
#         ring_buffer_flags[ring_buffer_index] = 1 if active else 0
#         ring_buffer_index += 1
#         ring_buffer_index %= NUM_WINDOW_CHUNKS

#         ring_buffer_flags_end[ring_buffer_index_end] = 1 if active else 0
#         ring_buffer_index_end += 1
#         ring_buffer_index_end %= NUM_WINDOW_CHUNKS_END

#         # start point detection
#         if not triggered:
#             ring_buffer.append(chunk)
#             num_voiced = sum(ring_buffer_flags)
#             if num_voiced > 0.8 * NUM_WINDOW_CHUNKS:
#                 sys.stdout.write(' Open ')
#                 triggered = True
#                 start_point = index - CHUNK_SIZE * 20  # start point
#                 ring_buffer.clear()
#         # end point detection
#         else:
#             ring_buffer.append(chunk)
#             num_unvoiced = NUM_WINDOW_CHUNKS_END - sum(ring_buffer_flags_end)
            
#             if num_unvoiced > 0.90 * NUM_WINDOW_CHUNKS_END or TimeUse > 10:
#                 sys.stdout.write(' Close ')
#                 triggered = False
#                 got_a_sentence = True

#         sys.stdout.flush()

#     sys.stdout.write('\n')
    
#     stream.stop_stream()
#     print("* done recording")
#     got_a_sentence = False

#     # write to file
#     raw_data.reverse()
#     for index in range(start_point):
#         raw_data.pop()
        
#     raw_data.reverse()
#     raw_data = normalize(raw_data)
    
#     #--- Steve Cox
#     #--- the wav has a header, we need to strip it off before playing
#     wav_data = raw_data[44:len(raw_data)] 
#     sound = pygame.mixer.Sound(buffer=wav_data)
#     sound.play()
#     #--- Wait for the sound to finish playing or we get an echo
#     while pygame.mixer.get_busy():
#         pass
    
#     #data = np.zeros((10, 10), dtype="uint8")
#     #zmqWave.sendPlayEvent('zzzz',data)
    

# stream.close()



import requests

def text_to_speech(text):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "3b0e6a5bc5b0796e25e26d715ec65799"
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)


text_to_speech("Hi How are you")