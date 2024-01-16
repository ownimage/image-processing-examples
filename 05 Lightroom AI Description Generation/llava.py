import requests
from PIL import Image
from timeit import default_timer as timer

import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration

model_id = "llava-hf/llava-1.5-7b-hf"

prompt = "USER: <image>\nWhat are these?\nASSISTANT:"
image_file = "http://images.cocodataset.org/val2017/000000039769.jpg"

model = LlavaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
).to(0)

processor = AutoProcessor.from_pretrained(model_id)


raw_image = Image.open(requests.get(image_file, stream=True).raw)

start = timer()

inputs = processor(prompt, raw_image, return_tensors='pt').to(0, torch.float16)

output = model.generate(**inputs, max_new_tokens=200, do_sample=False)
print(processor.decode(output[0][2:], skip_special_tokens=True))

end = timer()
print(f'duration = {end - start}')  # Time in seconds, e.g. 5.38091952400282