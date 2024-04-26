import subprocess


def generate_gguf(llama_cpp_path, model_path, mmproj_path, image_path, prompt, temp):
    command = f"./{llama_cpp_path}llava-cli -m {model_path} --mmproj {mmproj_path} --image {image_path} --temp {temp} -p {prompt}"
    print("Command: ", command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    output = process.stdout.read()
    return output.decode('utf-8')


if __name__ == '__main__':
    llama_cpp_path = "../md-gguf/llama.cpp/"
    model_path = "../md-gguf/moondream2/moondream2-text-model-f16.gguf"
    mmproj_path = "../md-gguf/moondream2/moondream2-mmproj-f16.gguf"
    image_path = "../thief.jpeg"
    temp = 0.
    prompt = '"anything suspicious!?"'

    output = generate_gguf(llama_cpp_path, model_path,
                           mmproj_path, image_path, prompt, temp)
    print('--------------')
    print("Output: ", output)
