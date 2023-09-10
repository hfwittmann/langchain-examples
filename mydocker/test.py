from gpt4all import GPT4All
from time import time

start = time()
model = GPT4All("/gpt4all-files/ggml-model-gpt4all-falcon-q4_0.bin")
output = model.generate("The capital of France is ", max_tokens=10)
print(output)
print(f"time taken {time() -start}")
