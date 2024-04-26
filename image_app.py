import streamlit as st
import random
import os
from generate_gguf import generate_gguf


st.title("Tiny Image Chat")


# file uploader
uploaded_file = st.file_uploader("Choose an image...",
                                 # type is jpg or png
                                 type=["jpg", "png", "jpeg", "tif", "tiff"])


# text input
prompt = st.text_input("Question", "")
submit = st.button("Submit")


if uploaded_file and submit:
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

    random_str = str(random.randint(0, 100000))
    with open(f"image_{random_str}.jpg", "wb") as f:
        f.write(uploaded_file.read())

    output = generate_gguf(llama_cpp_path="../md-gguf/llama.cpp/",
                           model_path="../md-gguf/moondream2/moondream2-text-model-f16.gguf",
                           mmproj_path="../md-gguf/moondream2/moondream2-mmproj-f16.gguf",
                           image_path=f"image_{random_str}.jpg",
                           prompt=f'"{prompt}"',
                           temp=0.)

    # delete image
    os.remove(f"image_{random_str}.jpg")
    st.write(output)
