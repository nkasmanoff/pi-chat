import argparse
import gradio as gr
import os
from generate_gguf import generate_gguf

parser = argparse.ArgumentParser()
parser.add_argument("--cpu", action="store_true")
args = parser.parse_args()


def answer_question(img, prompt):
    # save image
    img.save("image.jpg")
    # generate response
    answer = generate_gguf(llama_cpp_path="../md-gguf/llama.cpp/",
                           model_path="../md-gguf/moondream2/moondream2-text-model-f16.gguf",
                           mmproj_path="../md-gguf/moondream2/moondream2-mmproj-f16.gguf",
                           image_path="image.jpg",
                           prompt=f'"{prompt}"',
                           temp=0.)
    os.remove("image.jpg")
    return answer


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # 🌔 moondream
        ### A tiny vision language model. [GitHub](https://github.com/vikhyat/moondream)
        """
    )
    with gr.Row():
        prompt = gr.Textbox(label="Input Prompt",
                            placeholder="Type here...", scale=4)
        submit = gr.Button("Submit")
    with gr.Row():
        img = gr.Image(type="pil", label="Upload an Image")
        output = gr.TextArea(label="Response")
    submit.click(answer_question, [img, prompt], output)
    prompt.submit(answer_question, [img, prompt], output)

demo.queue().launch(debug=False, share=True)
