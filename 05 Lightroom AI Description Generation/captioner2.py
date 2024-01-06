#https://huggingface.co/unum-cloud/uform-gen
from uform.gen_model import VLMForCausalLM, VLMProcessor
from PIL import Image
import torch

model = VLMForCausalLM.from_pretrained("unum-cloud/uform-gen")
processor = VLMProcessor.from_pretrained("unum-cloud/uform-gen")

# [cap] Narrate the contents of the image with precision.
# [cap] Summarize the visual content of the image.
# [vqa] What is the main subject of the image?
prompt = "[cap] Narrate the contents of the image with precision."
image = Image.open('https://huggingface.co/spaces/llava-hf/llava-4bit/resolve/main/examples/baklava.png')

inputs = processor(texts=[prompt], images=[image], return_tensors="pt")
with torch.inference_mode():
     output = model.generate(
        **inputs,
        do_sample=False,
        use_cache=True,
        max_new_tokens=128,
        eos_token_id=32001,
        pad_token_id=processor.tokenizer.pad_token_id
    )

prompt_len = inputs["input_ids"].shape[1]
decoded_text = processor.batch_decode(output[:, prompt_len:])[0]

print(f'prompt_len = {prompt_len}')
print(f'decoded_text = {decoded_text}')
