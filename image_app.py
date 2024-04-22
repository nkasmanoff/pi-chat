import streamlit as st
import random
import os
import ollama



st.title("Tiny Chat with Images")

st.write("This is a chatbot that can help you with your questions. Ask me anything.")
st.write("Sadly this is pretty slow program so you may need to wait a few minutes.")

# file uploader
uploaded_file = st.file_uploader("Choose an image...", 
                                 # type is jpg or png
                                    type=["jpg", "png"])    


# text input
prompt = st.text_input("Input Question", "")
submit = st.button("Submit")


if uploaded_file and submit:
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

    random_str = str(random.randint(0, 100000))
    with open(f"image_{random_str}.jpg", "wb") as f:
        f.write(uploaded_file.read())
    
    res = ollama.chat(
        model="bakllava:7b-v1-q2_K",
        messages=[
            {
                'role': 'user',
                'content': prompt,
                'images': [f"image_{random_str}.jpg"]
            }
        ]
    )
    # delete image
    os.remove(f"image_{random_str}.jpg")  
    st.write(res['message']['content'])
else:
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    