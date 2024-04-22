import ollama
import gradio as gr
import os

def answer_question(img, prompt):
    # save image to disk
    img.save("image.jpg")

    res = ollama.chat(
        model="bakllava:7b-v1-q2_K",
        messages=[
            {
                'role': 'user',
                'content': prompt,
                'images': ["image.jpg"]
            }
        ]
    )
    # delete image
    os.remove("image.jpg")  
    return res['message']['content']



with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Tiny chat (with images)
        ### Upload an image, wait about 5 minutes, and get an answer to your question!
        """
    )
    with gr.Row():
        prompt = gr.Textbox(label="Input Prompt", placeholder="Type here...", scale=4)
        submit = gr.Button("Submit")
    with gr.Row():
        img = gr.Image(type="pil", label="Upload an Image")
        output = gr.TextArea(label="Response")
    submit.click(answer_question, [img, prompt], output)
    prompt.submit(answer_question, [img, prompt], output)

demo.queue().launch(debug=True)
