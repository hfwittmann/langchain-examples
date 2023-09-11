from gpt4all import GPT4All
from time import time

start = time()
model = GPT4All("orca-mini-13b.ggmlv3.q4_0.bin") # GPT4All("orca-mini-3b.ggmlv3.q4_0.bin") # GPT4All("/gpt4all-files/ggml-model-gpt4all-falcon-q4_0.bin")
output = model.generate("The capital of France is ", max_tokens=20)
print(output)
print(f"time taken {time() -start}")
