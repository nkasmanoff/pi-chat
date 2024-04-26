import streamlit as st
import ollama
from prompt import system_prompt
import os
import random
# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
st.title("Tiny Chat")

st.write("This is a chatbot that can help you with your questions. Ask me anything.")
st.write("Sadly this is pretty slow program so you may need to wait a few minutes.")


def generate_response():
    response = ollama.chat(model='llama3:instruct',
                           stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        'role': 'assistant',
        'content': f'{system_prompt}',
    }]

for i, msg in enumerate(st.session_state.messages):
    if i == 0:
        continue
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🐈").write(msg["content"])


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🐈").write_stream(generate_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": st.session_state["full_message"]})
