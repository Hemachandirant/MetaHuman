import speech_recognition as sr
import pygame
from gtts import gTTS
import os
import streamlit as st
import requests
from streamlit_chat import message
import os
import tempfile
import openai
import config
import winsound
import webrtcvad
import textwrap
from IPython.display import display, Audio
from pydub import AudioSegment
from pydub.playback import play

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


# send Email API
def send_email(to_email, subject):
    # Define the URL
    url = "https://gray-repulsive-duck.cyclic.app/sendEmail"

    # Define the headers
    headers = {
        "Content-Type": "application/json",
    }

    # Define the request body with the provided values
    payload = {
        "to": to_email,
        "subject": subject,
        "text": "Successfully Sent",
    }

    # Convert the payload to JSON
    json_payload = json.dumps(payload)

    # Send the POST request
    response = requests.post(url, headers=headers, data=json_payload)

    # Check the response status code
    if response.status_code == 200:
        return "Email sent successfully!"
    else:
        return f"Failed to send email. Status code: {response.status_code}"
        print(response.text)





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


def text_to_speech(text):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream"

    headers = {
        "xi-api-key": "3b0e6a5bc5b0796e25e26d715ec65799",
    }

    data = {"text": text, "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}}

    response = requests.post(url, json=data, headers=headers)

    output_filename = "reply.mp3"
    with open(output_filename, "wb") as output:
        output.write(response.content)

    # Initialize pygame mixer
    pygame.mixer.init()

    try:
        # Load the audio file
        pygame.mixer.music.load(output_filename)

        # Play the audio
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    finally:
        # Clean up and remove the temporary audio file
        pygame.mixer.quit()
        os.remove(output_filename)


def synthesize_and_play_speech(response_text):
    # Convert text to speech
    tts = gTTS(text=response_text, lang="en")
    tts.save("response.mp3")

    # Initialize pygame mixer
    pygame.mixer.init()

    try:
        # Load the audio file
        pygame.mixer.music.load("response.mp3")

        # Play the audio
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    finally:
        # Clean up and remove the temporary audio file
        pygame.mixer.quit()
        os.remove("response.mp3")


def generate_response(input_text, conversation_history):
    intial_prompt = (
        "Think Like your a trusted AI IT Support Assistant\n."
        "Imagine this: you're a tech professional or a business owner, and you've run into a snag. That's where I come in. I'll guide you step by step to troubleshoot, fix, and optimize your technology.\n\n"
        "Just provide me with some key details:\n"
        "1. What's the issue you're facing? Describe it in your own words.\n"
        "2. Which operating system and browser are you using?\n"
        "3. When did the issue start? Any recent changes?\n"
        "4. What steps have you taken so far to resolve it?\n"
        "5. If you've seen any error messages, please share what they say.\n\n"
        "Once I have these details, I'll tap into my knowledge base and provide you with actionable solutions. Let's get started and turn your tech troubles into triumphs!\n\n"
         "And add the Filler Words Um, Er, Uh, Hmm in between the 2 sentences that makes the conversation more like a human conversation and use simple words for better understanding\n\n"
        "Please respond to all input in 50 words or less."
    )
    messages = [
        {
            "role": "system",
            "content": intial_prompt,
        },
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
        {
            "name": "send_email",
            "description": "Send mail to the given email and subject",
            "parameters": {
                "type": "object",
                "properties": {
                    "to_email": {
                        "type": "string",
                        "description": "The email or gmail,  e.g. balaji@gmail.com, abhijeet@wipro.com",
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject of the email or gmail, e.g. Can you fix meet today, What is the status of the task",
                    },
                },
                "required": ["to_email", "subject"],
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
            "send_email": send_email,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])

        if function_name == "get_current_weather":
            location = function_args.get("location")
            function_response = function_to_call(location=location)
        elif function_name == "send_email":
            to_email = function_args.get("to_email")
            subject = function_args.get("subject")
            function_response = function_to_call(to_email=to_email, subject=subject)
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
        second_response_text = second_response.choices[0].message[
            "content"
        ]  # get a new response from GPT where it can see the function response
        return second_response_text

    else:
        response_text = response.choices[0].message["content"]
        return response_text


def main(stop_keyword="restart", exit_keyword="exit"):
    st.title("🤖 Intelligent Voice Assistant")

    conversation_history = []

    # Create a Streamlit sidebar
    st.sidebar.title("Settings")
    st.sidebar.write("Press the Start button and ask me a question. I will respond.")

    if st.sidebar.button("Start"):
        st.sidebar.write(
            "Note:  You can start your question over by saying Restart during question input..."
        )  # Instruction section
        st.sidebar.write(
            "You can end the chat session by saying 'Exit'"
        )  # Instruction section

        while True:
            st.text(" Listening...")
            winsound.Beep(800, 200)  # Play a beep sound when ready for input

            input_text = transcribe_audio()

            if not input_text:
                continue

            wrapped_input = textwrap.fill(input_text, width=90)
            indented_input = "\n".join(
                [
                    "<div style='text-align: left;'>" + line + "</div>"
                    for line in wrapped_input.splitlines()
                ]
            )

            st.markdown(
                f"<div style='padding: 30px;'>"
                f"<div style='background-color: blue; padding: 10px; border-radius: 5px; color: white; text-align: left;'>"
                f"{indented_input}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

            if stop_keyword.lower() in input_text.lower():
                st.text("Restarting prompt...")
                conversation_history = []
                continue

            if exit_keyword.lower() in input_text.lower():
                end_message  = (
                    "Thank you for using our IT support AI assistant.\n"
                    "If you have any more questions or need assistance in the future, feel free to reach out. Have a great day!\n"
                )
                st.markdown(
                f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
                f"{end_message}</div>",
                unsafe_allow_html=True,
                )
                
                text_to_speech(end_message)
                

                break

            response_text = generate_response(input_text, conversation_history)
            print(response_text)
            wrapped_response = textwrap.fill(response_text, width=70)
            indented_response = "\n".join(
                [
                    "<div style='text-align: left;'>" + line + "</div>"
                    for line in wrapped_response.splitlines()
                ]
            )

            st.markdown(
                f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
                f"{indented_response}</div>",
                unsafe_allow_html=True,
            )

            # synthesize_and_play_speech(response_text)
            text_to_speech(response_text)
            conversation_history.append({"role": "user", "content": input_text})
            conversation_history.append({"role": "assistant", "content": response_text})


if __name__ == "__main__":
    main(stop_keyword="restart", exit_keyword="exit")





# def synthesize_and_play_speech(response_text):
#     tts = gTTS(text=response_text, lang='en')
#     tts.save('response.mp3')
#     os.system('mpg321 response.mp3')
#     os.remove('response.mp3')

# def get_current_weather(location, unit="fahrenheit"):
#     """Get the current weather in a given location"""
#     weather_info = {
#         "location": location,
#         "temperature": "72",
#         "unit": unit,
#         "forecast": ["sunny", "windy"],
#     }
#     return json.dumps(weather_info)


#     with open('output.mp3', 'wb') as f:
#         for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
#             if chunk:
#                 f.write(chunk)


#  url = f"https://api.elevenlabs.io/v1/text-to-speech/{config.ADVISOR_VOICE_ID}/stream"
#     data = {
#         "text": system_message["content"].replace('"', ''),
#         "voice_settings": {
#             "stability": 0.1,
#             "similarity_boost": 0.8
#         }
#     }

#     r = requests.post(url, headers={'xi-api-key': config.ELEVEN_LABS_API_KEY}, json=data)

#     output_filename = "reply.mp3"
#     with open(output_filename, "wb") as output:
#         output.write(r.content)

# voice = clone(
#     name="Alex - expressive narrator",
#     description="Young american man. Is a strong and expressive narrator",
# )

# audio = generate(text="Some very long text to be read by the voice", voice=voice)

# play(audio)

# history = History.from_api()
# print(history)