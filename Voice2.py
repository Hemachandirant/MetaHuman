import speech_recognition as sr
import pygame
from gtts import gTTS
import os
import time
import streamlit as st
import requests
from streamlit_chat import message
import os
import collections
import pyaudio
import sys
from array import array
from pocketsphinx import AudioFile
import tempfile
import openai
import config
import openai
import json
import winsound
import webrtcvad
import textwrap
from IPython.display import display, Audio
# from IPython.display import Video
# import azure.cognitiveservices.speech as speechsdk
from IPython.display import HTML
import base64






vad = webrtcvad.Vad()
vad.set_mode(2) # Aggressiveness: 0 (least aggressive) to 3 (most aggressive)



FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_DURATION_MS = 30       # supports 10, 20 and 30 (ms)
PADDING_DURATION_MS = 1500   # 1 sec jugement
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)  # chunk to read
CHUNK_BYTES = CHUNK_SIZE * 2  # 16bit = 2 bytes, PCM
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)

#--- Steve Cox
NUM_WINDOW_CHUNKS = int(240 / CHUNK_DURATION_MS)
#NUM_WINDOW_CHUNKS = int(400 / CHUNK_DURATION_MS)  # 400 ms/ 30ms  ge

NUM_WINDOW_CHUNKS_END = NUM_WINDOW_CHUNKS * 2
START_OFFSET = int(NUM_WINDOW_CHUNKS * CHUNK_DURATION_MS * 0.5 * RATE)

pa = pyaudio.PyAudio()
stream = pa.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
                 start=False,
                 # input_device_index=2,
                 frames_per_buffer=CHUNK_SIZE)



# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location):
    """Get the current weather in a given location"""

    url = f"https://open-weather13.p.rapidapi.com/city/{location}"


    headers = {
        "X-RapidAPI-Key": "27678da727mshb69f3fc5c4e5cf0p175e22jsnb10038e8caa6",
        "X-RapidAPI-Host": "open-weather13.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers)

    weather_info = response.json()

    print(weather_info)
    return json.dumps(weather_info)


# def get_current_weather(location, unit="fahrenheit"):
#     """Get the current weather in a given location"""
#     weather_info = {
#         "location": location,
#         "temperature": "72",
#         "unit": unit,
#         "forecast": ["sunny", "windy"],
#     }
#     return json.dumps(weather_info)
# def transcribe_audio():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print(robot_emoji + " Listening...")
        
#         # Call the voice_activity_detection function here
#         voice_activity_detection()
        
#         audio = recognizer.listen(source)
    
#     try:
#         input_text = recognizer.recognize_google(audio)
#         return input_text.strip()
#     except sr.UnknownValueError:
#         return ""

# def transcribe_audio_from_data(audio_data):
#     # Perform speech recognition on the provided audio data
#     recognizer = sr.Recognizer()
#     audio = sr.AudioData(audio_data, sample_rate=16000, sample_width=2)
#     try:
#         text = recognizer.recognize_google(audio)
#         return text.strip()
#     except sr.UnknownValueError:
#         return ""

# def voice_activity_detection():
#     # Initialize VAD and PyAudio stream
#     vad = webrtcvad.Vad()
#     vad.set_mode(2)  # Set VAD aggressiveness

#     pa = pyaudio.PyAudio()
#     stream = pa.open(
#         format=pyaudio.paInt16,
#         channels=1,
#         rate=16000,
#         input=True,
#         start=True,
#         frames_per_buffer=CHUNK_SIZE
#     )

#     # Initialize variables
#     audio_buffer = []
#     listening = False

#     while True:
#         # Capture an audio frame
#         audio_frame = stream.read(CHUNK_SIZE)

#         # Check if speech is detected
#         is_speech = vad.is_speech(audio_frame, sample_rate=16000)

#         if is_speech:
#             # Append the frame to the audio buffer
#             audio_buffer.append(audio_frame)
#             if not listening:
#                 print("Listening...")
#                 listening = True
#         elif listening:
#             # If speech ends, transcribe and reset
#             if audio_buffer:
#                 audio_data = b''.join(audio_buffer)
#                 audio_buffer = []

#                 # Perform speech recognition on audio_data
#                 recognized_text = transcribe_audio_from_data(audio_data)

#                 if recognized_text:
#                     return recognized_text  # Return recognized text

def listen_for_user_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening1...")

        # Adjust recognizer sensitivity to ambient noise
        recognizer.adjust_for_ambient_noise(source)

        audio_data = []
        listening = True

        while listening:
            try:
                audio = recognizer.listen(source, timeout=10)  # Adjust the timeout as needed
                audio_data.append(audio)
                print("Listening2...")

            except sr.WaitTimeoutError:
                # User has paused speaking
                listening = False

        if audio_data:
            print("Processing...")
            # Concatenate the bytes objects in the list
            full_audio = sr.AudioData(b''.join([audio.frame_data for audio in audio_data]), RATE, 2)
            user_input = recognizer.recognize_google(full_audio)
            return user_input.strip()
        else:
            return ""

        


        # At this point, 'raw_data' contains the audio data for the detected speech.
        # You can further process or save this data as needed.





# def synthesize_and_play_speech(response_text):
#     tts = gTTS(text=response_text, lang='en')
#     tts.save('response.mp3')
#     os.system('mpg321 response.mp3')
#     os.remove('response.mp3')


def synthesize_and_play_speech(response_text):
    # Convert text to speech
    tts = gTTS(text=response_text, lang='en')
    tts.save('response.mp3')

    # Initialize pygame mixer
    pygame.mixer.init()

    try:
        # Load the audio file
        pygame.mixer.music.load('response.mp3')

        # Play the audio
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    finally:
        # Clean up and remove the temporary audio file
        pygame.mixer.quit()
        os.remove('response.mp3')

def generate_response(input_text, conversation_history):
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Please respond to all input in 50 words or less."},
    ]


    messages.extend(conversation_history)
    messages.append({"role": "user", "content": input_text})
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA, Bangalore",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
        
    ] 


    # response = openai.Completion.create(
    #     engine="text-davinci-002",
    #     messages=messages,
    # )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
        )
    print(response)
    response_message = response["choices"][0]["message"]
    

    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
            location=function_args.get("location"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        
        print(messages)
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
           
        )
        second_response_text = second_response.choices[0].message['content']  # get a new response from GPT where it can see the function response
        return second_response_text

    else:
        response_text = response.choices[0].message['content']
        return response_text
    
    



def main(stop_keyword="restart", exit_keyword="exit"):
    
    st.title("🤖 Intelligent Voice Assistant")
    got_a_sentence = False
    conversation_history = []

    # Create a Streamlit sidebar
    st.sidebar.title("Settings")
    st.sidebar.write("Press the Start button and ask me a question. I will respond.")

    if st.sidebar.button("Start"):
        st.sidebar.write("Note:  You can start your question over by saying Restart during question input...")  # Instruction section
        st.sidebar.write("You can end the chat session by saying 'Exit'")  # Instruction section

        listening = True
        input_text = ""

        while True:
            if listening:
                st.text("Listening3...")
                winsound.Beep(800, 200)  # Play a beep sound when ready for input

                input_text = listen_for_user_input()

                if input_text:
                    print(f"User said: {input_text}")
                    listening = False

            if not input_text:
                continue

            wrapped_input = textwrap.fill(input_text, width=90)
            indented_input = "\n".join(["<div style='text-align: left;'>" + line + "</div>" for line in wrapped_input.splitlines()])

            st.markdown(f"<div style='padding: 30px;'>"
                        f"<div style='background-color: blue; padding: 10px; border-radius: 5px; color: white; text-align: left;'>"
                        f"{indented_input}</div>"
                        f"</div>",
                        unsafe_allow_html=True)

            if stop_keyword.lower() in input_text.lower():
                st.text("Restarting prompt...")
                conversation_history = []
                continue

            if exit_keyword.lower() in input_text.lower():
                st.markdown(f"<div style='background-color: white; padding: 10px; border-radius: 5px;'>"
                            f"<span style='color: black;'>Goodbye for now...</span></div>",
                            unsafe_allow_html=True)
                break

            response_text = generate_response(input_text, conversation_history)
            print(response_text)
            wrapped_response = textwrap.fill(response_text, width=70)
            indented_response = "\n".join(["<div style='text-align: left;'>" + line + "</div>" for line in wrapped_response.splitlines()])

            st.markdown(f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
                        f"{indented_response}</div>",
                        unsafe_allow_html=True)

            synthesize_and_play_speech(response_text)
            conversation_history.append({"role": "user", "content": input_text})
            conversation_history.append({"role": "assistant", "content": response_text})

if __name__ == "__main__":
    main(stop_keyword="restart", exit_keyword="exit")