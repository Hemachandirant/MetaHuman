import speech_recognition as sr
import pygame
from gtts import gTTS
import os
import streamlit as st
from streamlit_chat import message
import os
import tempfile
import openai
import config
import winsound
import webrtcvad
import textwrap
from IPython.display import display, Audio
# from IPython.display import Video
# import azure.cognitiveservices.speech as speechsdk
from IPython.display import HTML
import base64





robot_emoji = "�"

vad = webrtcvad.Vad()
vad.set_mode(1)  # Aggressiveness: 0 (least aggressive) to 3 (most aggressive)



import openai
import json

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(robot_emoji + " Listening...")
        audio = recognizer.listen(source)
    
    try:
        input_text = recognizer.recognize_google(audio)
        return input_text.strip()
    except sr.UnknownValueError:
        return ""

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
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ] 
    openai.api_key = "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"

    # response = openai.Completion.create(
    #     engine="text-davinci-002",
    #     messages=messages,
    # )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        )

    response_text = response.choices[0].message['content']

    return response_text

def main(stop_keyword="restart", exit_keyword="exit"):
    
    st.title("🤖 Intelligent Voice Assistant")

    conversation_history = []

    # Create a Streamlit sidebar
    st.sidebar.title("Settings")
    st.sidebar.write("Press the Start button and ask me a question. I will respond.")

    if st.sidebar.button("Start"):
        st.sidebar.write("Note:  You can start your question over by saying Restart during question input...")  # Instruction section
        st.sidebar.write("You can end the chat session by saying 'Exit'")  # Instruction section
    
        while True:
            
            st.text(" Listening...")
            winsound.Beep(800, 200)  # Play a beep sound when ready for input

            input_text = transcribe_audio()

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