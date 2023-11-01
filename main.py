import streamlit as st
import winsound
import os
# import asyncio
import textwrap
from datetime import datetime
from persist import persist, load_widget_state
from generate_response import response_function
from generate_response_azure import response_function_azure
from speech_func import Speech
# from speech_processing import Start_recording

# Create an instance of the Speech class
speech_functions = Speech()

# Define a persistent key for st.session_state.messages
messages_key = persist("messages")

# Initialize st.session_state.messages as a list if not already defined
st.session_state.messages = st.session_state.get(messages_key, [])




def main(stop_keyword="restart", exit_keyword="exit"):
    st.title("🖥️ AI IT Support Portal by GENAI")

    # Add a welcoming image or logo
    st.image("AI.jpg")

    # Add a catchy headline
    st.header("Welcome to Our AI IT Support Portal")

    # Add a brief description
    st.write(
        "Get expert AI IT support and assistance right here. Whether you have questions, issues, or need help,\n"
        "You can ask our Intelligent Voice Assistant And Chat Assitance depends upon your Convenience."
    )

    # Display IT support-related content
    st.subheader("Explore Our AI IT Support Services")

    # Add content related to your IT services
    st.markdown("Here's what AI Assistant offer to help you with your IT needs:")

    # Service 1: Password Reset
    st.markdown(
        "1. **Password Reset:** Forgot your password? No worries, Our Intelligent Virtual Assistant help you reset it."
    )

    # Service 2: Software Installation
    st.markdown(
        "2. **Software Installation:** Need to install software on your computer? Intelligent Virtual Assistant will guide you through the process."
    )

    # Service 3: Network Troubleshooting
    st.markdown(
        "3. **Network Troubleshooting:** Experiencing network issues? Our AI IT Expert will diagnose and fix the problem."
    )

    # Service 4: Hardware Support
    st.markdown(
        "4. **Hardware Support:** Problems with your hardware? Let us know, and Our AI IT Expert provide solutions."
    )

    # Service 5: General IT Queries
    st.markdown(
        "5. **General IT Queries:** Have questions about IT? Ask us anything, and Our IVA provide answers."
    )

    # Add a call-to-action or promotional content
    st.subheader("Get Started Today!")

    st.write(
        "Ready to get the IT support you need? Feel free to explore our Fully Functional AI IT Support and reach out to Our IVA Service whenever you're ready."
    )

    # Add a button for users to take action
    if st.button("Contact Us"):
        # You can customize this action based on your application's needs
        st.write("Contact form or support contact information can go here.")



def Speech_support(stop_keyword="restart", exit_keyword="exit"):
    st.title("🤖 Intelligent Voice Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.sidebar.write("Settings")

    st.sidebar.selectbox("Choose Your Preferred Language", st.session_state["languages"], key=persist("language_name"))

    st.sidebar.write("Press the Start button and ask me a question. I will respond.")

    if st.sidebar.button("Start", key="speech_button"):
        st.session_state.should_exit = True

        st.sidebar.write(
            "Note:  You can start your question over by saying Restart during question input..."
        )  # Instruction section
        st.sidebar.write(
            "You can Stop the session by Clicking below 'Stop' Button"
        )  # Instruction section

        if st.sidebar.button("Stop", key="stop_button"):
            st.session_state.should_exit = True

        welcome_message = "Hi, I am MyLiva, How can I assist you today"

        st.markdown(
            f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
            f"{welcome_message}</div>",
            unsafe_allow_html=True,
        )

        speech_functions.text_to_speech_azure(welcome_message)
        # speech_functions.synthesize_and_play_speech(welcome_message)
        # speech_functions.text_to_speech_elevanlabs(welcome_message)
        
        output_folder = f'./Output/{datetime.now().strftime("%Y%m%d_%H%M%S")}/'
        os.makedirs(output_folder)

        while st.session_state.should_exit:
            st.text("🤖 Listening...")
            winsound.Beep(800, 200)  # Play a beep sound when ready for input

            # input_text = speech_functions.transcribe_audio()
            input_text = speech_functions.speech_to_text_azure()
            # input_text = await Start_recording(output_folder=output_folder)[0]['DisplayText']



            if not input_text:
                not_listening = "Your voice is not audible, can you say it again?"
                st.markdown(
                    f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
                    f"{not_listening}</div>",
                    unsafe_allow_html=True,
                )
                # speech_functions.synthesize_and_play_speech(not_listening)
                #speech_functions.text_to_speech_elevanlabs(not_listening)
                speech_functions.text_to_speech_azure(not_listening)
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
                st.session_state.messages = []
                continue

            # try:
            # response_text = response_function.generate_response(
            #     input_text, st.session_state.messages
            # )
            response_text = response_function_azure.generate_response_azure(
                input_text, st.session_state.messages
            )
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

            speech_functions.text_to_speech_azure(response_text)
            # speech_functions.synthesize_and_play_speech(response_text)
            # speech_functions.text_to_speech_elevanlabs(response_text)
            st.session_state.messages.append(
                {"role": "user", "content": input_text}
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )


def Chat_support():
    st.title("🤖 Intelligent Chat Support")

    st.sidebar.selectbox("Selectbox", st.session_state["languages"], key=persist("language_name"))

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("ai"):
            full_response = response_function_azure.generate_response_azure(
                prompt, st.session_state.messages
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

            # Implement letter-by-letter printing
            st.markdown(full_response)


if "page" not in st.session_state:
    # Initialize session state.
    st.session_state.update({
        # Default page.
        "page": "Home",

        "list": [],

        # Languages which you prefer
        "languages": ["English", "French", "Hindi", "Tamil"],
    })

page_names_to_funcs = {
    "Home": main,
    "🗣️SPEECH SUPPORT": Speech_support,
    "💬CHAT SUPPORT": Chat_support,
}

# Load widget state
load_widget_state()

demo_name = st.sidebar.selectbox("Choose Your Preference", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
