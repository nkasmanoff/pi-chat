import streamlit as st
import ollama
import time
from prompt import system_prompt
import os
import random
# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
st.title("Tiny Chat")

st.write("This is a chatbot that can help you with your questions. Ask me anything.")
st.write("Sadly this is pretty slow program so you may need to wait a few minutes.")

tab1, tab2 = st.tabs(["Chat", "Image Chat"])

def generate_response():
    response = ollama.chat(model='llama3:8b-instruct-q2_K', stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token



with tab1:
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [    {
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
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]}) 





with tab2:  
    st.write("Please ignore the text box at the bottom. Just use the input question below.")

    # file uploader
    uploaded_file = st.file_uploader("Choose an image...", 
                                    # type is jpg or png
                                        type=["jpg", "png","jpeg","tif","tiff"])    


    # text input
    prompt = st.text_input("Input question", "")
    submit = st.button("Submit")


    if uploaded_file and submit:

        def generate_image_response():
            response = ollama.chat(
                model="llava:7b-v1.6-mistral-q2_K",
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                      'images': [f"image_{random_str}.jpg"]
                    }
                ],
                stream=True
            )
            for partial_resp in response:
                token = partial_resp["message"]["content"]
                st.session_state["full_image_message"] += token
                yield token

        st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

        random_str = str(random.randint(0, 100000))
        with open(f"image_{random_str}.jpg", "wb") as f:
            f.write(uploaded_file.read())
        
        st.session_state["full_image_message"] = ""
        st.chat_message("assistant", avatar="🐈").write_stream(generate_image_response
                                                                )
        os.remove(f"image_{random_str}.jpg")  


            