from transformers import pipeline, InstructBlipProcessor, InstructBlipForConditionalGeneration
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
from uform.gen_model import VLMForCausalLM, VLMProcessor


class Captioner:
    __model_id = 0
    __context = None
    __describe_method = None

    @classmethod
    def __init__(self, model_id):
        self.__model_id = model_id
        print(f'model = {self.describe(None)}')
        print(f'torch.cuda.is_available() -> {torch.cuda.is_available()}')

    @staticmethod
    def get_method_count():
        return 4

    @classmethod
    def method0(self, image_path):
        # https://huggingface.co/tasks/image-to-text
        model_name = 'Salesforce/blip-image-captioning-base'
        if image_path is None:
            return model_name

        if self.__context is None:
            self.__context = {
                'captioner': pipeline('image-to-text', model=model_name, max_new_tokens=200)
            }

        captioner = self.__context['captioner']

        with open(image_path, "rb") as file:
            image = Image.open(file)
            image.thumbnail((image.width / 4, image.height / 4))
            return captioner(image)[0]["generated_text"]

    @classmethod
    def method1(self, image_path):
        # https://huggingface.co/microsoft/kosmos-2-patch14-224
        model_name = 'microsoft/kosmos-2-patch14-224'
        if image_path is None:
            return model_name

        if self.__context is None:
            self.__context = {
                'model': AutoModelForVision2Seq.from_pretrained(model_name),
                'processor': AutoProcessor.from_pretrained(model_name)
            }

        model = self.__context['model']
        processor = self.__context['processor']
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
    def method2(self, image_path):
        # https://huggingface.co/microsoft/kosmos-2-patch14-224
        model_name = 'unum-cloud/uform-gen'
        if image_path is None:
            return model_name

        if self.__context is None:
            self.__context = {
                'model': VLMForCausalLM.from_pretrained(model_name),
                'processor': VLMProcessor.from_pretrained(model_name)
            }

        model = self.__context['model']
        processor = self.__context['processor']

        # [cap] Narrate the contents of the image with precision.
        # [cap] Summarize the visual content of the image.
        # [vqa] What is the main subject of the image?
        prompt = '[cap] Summarize the visual content of the image.'
        with open(image_path, "rb") as file:
            image = Image.open(file)
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
            return decoded_text.replace('<|im_end|>', '')

    @classmethod
    def method3(self, image_path):
        # https://huggingface.co/microsoft/kosmos-2-patch14-224
        model_name = 'Salesforce/instructblip-vicuna-7b'
        if image_path is None:
            return model_name

        if self.__context is None:
            self.__context = {
                'model': InstructBlipForConditionalGeneration.from_pretrained(model_name),
                'processor': InstructBlipProcessor.from_pretrained(model_name)
            }
            print(f'torch.cuda.is_available() = {torch.cuda.is_available()}')

        model = self.__context['model']
        processor = self.__context['processor']

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)

        prompt = "Give a detailed description of this image."
        with open(image_path, "rb") as file:
            image = Image.open(file)
            image.thumbnail((image.width/4, image.height/4))
            inputs = processor(images=image, text=prompt, return_tensors="pt").to(device)

            outputs = model.generate(
                **inputs,
                do_sample=True,
                num_beams=5,
                max_length=256,
                min_length=1,
                # top_p=0.9,
                repetition_penalty=1.5,
                length_penalty=1.0,
                temperature=1,
            )
            generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
            return generated_text

    @classmethod
    def get_describe_method(self):
        if self.__describe_method is None:
            zeros = len(f'{self.get_method_count()}')
            method_name = f'method{self.__model_id:0{zeros}d}'
            print(f'describe_method = {method_name}')
            self.__describe_method = eval(f'self.{method_name}')

        return self.__describe_method

    @classmethod
    def describe(self, image_path):
        return self.get_describe_method()(image_path)
