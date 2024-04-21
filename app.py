import streamlit as st
import ollama
import time
from prompt import system_prompt
# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
st.title("Tiny Chat")

st.write("This is a chatbot that can help you with your questions. Ask me anything.")



def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [    {
        'role': 'assistant',
        'content': f'{system_prompt}',
    },]

# Display chat messages from history on app rerun
for i, message in enumerate(st.session_state.messages):
    if i == 0:
        continue
    with st.chat_message(message["role"], avatar="🧑" if message["role"] == "user" else "🐈"):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user", avatar="🧑").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = ollama.chat(model='llama3:8b-instruct-q2_K', messages=st.session_state.messages)

    reply = response['message']['content']

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar = "🐈"):
        #st.markdown(reply)
        st.write_stream(response_generator(reply))

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": reply})
