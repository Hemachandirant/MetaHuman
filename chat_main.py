import openai
import streamlit as st
from generate_response import response_function

st.title("IT Expert")
openai.api_key = "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"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_response = response_function.generate_response(
            prompt, st.session_state.messages
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

        # Implement letter-by-letter printing
        st.markdown(full_response)
