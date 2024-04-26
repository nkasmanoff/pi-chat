import cherrypy
from generate_gguf import generate_gguf
import os
import time


class Root(object):
    @cherrypy.expose
    def index(self):
        # create image upload form
        return """
<html>
<head>
    <title>Raspberry Cam</title>
    <style>
        input[type="file"] {
            width: 300px;
            height: 40px;
        }
        input[type="text"] {
            width: 100%;
            height: 200p1;
        }
    </style>
</head>
<body>
    <h1>Raspberry Cam</h1>
    <form action="generate" method="post" enctype="multipart/form-data">
        <input type="file" name="image" />
        <input type="text" name="prompt" />
        <input type="submit" />
    </form>
</body>
</html>
        """

    # in future version, this photo will be taken automatically via the camera

    @cherrypy.expose
    def generate(self, image, prompt):
        # save image
        # generate response
        with open("image.jpg", "wb") as f:
            f.write(image.file.read())
        start_time = time.time()
        answer = generate_gguf(llama_cpp_path="../md-gguf/llama.cpp/",
                               model_path="../md-gguf/moondream2/moondream2-text-model-f16.gguf",
                               mmproj_path="../md-gguf/moondream2/moondream2-mmproj-f16.gguf",
                               image_path="image.jpg",
                               prompt=f'"{prompt}"',
                               temp=0.)
        end_time = time.time()
        out_html = f"""
            <html>
            <head>
            </head>
            <body>
            <h2>Prompt:</h2>
            <p>{prompt}</p>            
            <h2>Response:</h2>
            <p>{answer}</p>
            <h2>Time taken:</h2>
            <p>{round(end_time - start_time,2)} seconds</p>
            </body>
            </html>
        """

        return out_html


if __name__ == '__main__':
    # Runs on http://0.0.0.0:5000 accessible over the network
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 5000,
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': ''
        }
    })
    cherrypy.quickstart(Root())
