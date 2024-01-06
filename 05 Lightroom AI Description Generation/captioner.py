import sys

from transformers import pipeline
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq


# def method0(image_path):
#     # https://huggingface.co/tasks/image-to-text
#     model_name = 'Salesforce/blip-image-captioning-base'
#     if image_path is None:
#         print(f'model_name = {model_name}')
#         return
#
#     captioner = pipeline('image-to-text', model=model_name, max_new_tokens=200)
#     with open(image_path, "rb") as file:
#         image = Image.open(file)
#         print(f'{image_path} : {captioner(image)[0]["generated_text"]}')


# def method1(image_path):
#     # https://huggingface.co/microsoft/kosmos-2-patch14-224
#     model_name = 'microsoft/kosmos-2-patch14-224'
#     if image_path is None:
#         print(f'model_name = {model_name}')
#         return
#
#     model = AutoModelForVision2Seq.from_pretrained(model_name)
#     processor = AutoProcessor.from_pretrained(model_name)
#     prompt = "<grounding>An image of"
#
#     with open(image_path, "rb") as file:
#         image = Image.open(file)
#         inputs = processor(text=prompt, images=image, return_tensors="pt")
#
#         generated_ids = model.generate(
#             pixel_values=inputs["pixel_values"],
#             input_ids=inputs["input_ids"],
#             attention_mask=inputs["attention_mask"],
#             image_embeds=None,
#             image_embeds_position_mask=inputs["image_embeds_position_mask"],
#             use_cache=True,
#             max_new_tokens=128,
#         )
#         generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
#         processed_text, entities = processor.post_process_generation(generated_text)
#         print(processed_text)

METHOD_COUNT = 2
USAGE = 'captioner <model_id> <directory_path>'
USAGE_MODEL_ID = f'model_id must be an integer >= 0 and < METHOD_COUNT'


class Captioner:
    model_id = 0
    dir_path = ''
    context = None
    describe_method = None

    @classmethod
    def __init__(self, model_id, dir_path):
        self.model_id = model_id
        self.dir_path = dir_path
        print(f'model = {self.describe(None)}')
        print(f'torch.cuda.is_available() -> {torch.cuda.is_available()}')

    @classmethod
    def method0(self, image_path):
        # https://huggingface.co/tasks/image-to-text
        model_name = 'Salesforce/blip-image-captioning-base'
        if image_path is None:
            return model_name

        if self.context is None:
            self.context = {
                'captioner' : pipeline('image-to-text', model=model_name, max_new_tokens=200)
            }

        captioner = self.context['captioner']

        with open(image_path, "rb") as file:
            image = Image.open(file)
            return captioner(image)[0]["generated_text"]

    @classmethod
    def method1(self, image_path):
        # https://huggingface.co/microsoft/kosmos-2-patch14-224
        model_name = 'microsoft/kosmos-2-patch14-224'
        if image_path is None:
            return model_name

        if self.context is None:
            self.context = {
                'model' : AutoModelForVision2Seq.from_pretrained(model_name),
                'processor' : AutoProcessor.from_pretrained(model_name)
            }

        model = self.context['model']
        processor = self.context['processor']
        prompt = "<grounding>An image of"

        with open(image_path, "rb") as file:
            image = Image.open(file)
            inputs = processor(text=prompt, images=image, return_tensors="pt")

            generated_ids = model.generate(
                pixel_values=inputs["pixel_values"],
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                image_embeds=None,
                image_embeds_position_mask=inputs["image_embeds_position_mask"],
                use_cache=True,
                max_new_tokens=128,
            )
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            processed_text, entities = processor.post_process_generation(generated_text)
            return processed_text

    @classmethod
    def get_describe_method(self):
        if self.describe_method is None:
            zeros = len(f'{METHOD_COUNT}')
            method_name = f'method{self.model_id:0{zeros}d}'
            print(f'describe_method = {method_name}')
            self.describe_method = eval(f'self.{method_name}')

        return self.describe_method


    @classmethod
    def describe(self, image_path):
        return self.get_describe_method()(image_path)


if len(sys.argv) != 3:
    print(USAGE)
    exit()

try:
    model_id = int(sys.argv[1])
    if 0 <= model_id < METHOD_COUNT:
        print(f'model_id = {model_id}')
    else:
        exit()
except:
    print(USAGE)
    print(USAGE_MODEL_ID)
    exit()

dir_path = int(sys.argv[2])
print(f'dir_path = {dir_path}')
#TODO check that the dir_path exists

captioner = Captioner(model_id, dir_path)

image_path = 'test/images/DSC_3877.NEF'
print(f'{image_path} : {captioner.describe(image_path)}')

image_path = 'test/images/DSC_3879.NEF'
print(f'{image_path} : {captioner.describe(image_path)}')