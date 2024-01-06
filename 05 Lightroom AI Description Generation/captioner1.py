from transformers import pipeline
import torch
from PIL import Image

print(torch.cuda.is_available())
models = ['Salesforce/blip-image-captioning-base', 'microsoft/kosmos-2-patch14-224']
model = models[0]
print(f'model = {model}')

captioner = pipeline('image-to-text', model=model, max_new_tokens=200)
print(captioner('https://huggingface.co/datasets/Narsil/image_dummy/resolve/main/parrots.png'))

filename = 'test/images/DSC_3877.NEF'
with open(filename, "rb") as file:
    image = Image.open(file)
    print(captioner(image)[0]['generated_text'])


def caption(filename):
    return "hello"
