from transformers import pipeline, InstructBlipProcessor, InstructBlipForConditionalGeneration
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
from uform.gen_model import VLMForCausalLM, VLMProcessor
import logging, sys


class Captioner:
    __context = {}

    @classmethod
    def __init__(self, logging_level = logging.DEBUG):
        logging.basicConfig(stream=sys.stdout, level=logging_level)
        logging.info(f'torch.cuda.is_available() -> {torch.cuda.is_available()}')

    @staticmethod
    def get_method_count():
        return 4

    @classmethod
    def method0(self, image):
        # https://huggingface.co/tasks/image-to-text
        model_name = 'Salesforce/blip-image-captioning-base'
        model_context_id = '0'

        if image is None:
            return model_name

        if model_context_id not in self.__context:
            context = {
                'captioner': pipeline('image-to-text', model=model_name, max_new_tokens=200)
            }
            self.__context[model_context_id] = context

        context = self.__context[model_context_id]
        captioner = context['captioner']

        return captioner(image)[0]["generated_text"]

    @classmethod
    def method1(self, image):
        # https://huggingface.co/microsoft/kosmos-2-patch14-224
        model_name = 'microsoft/kosmos-2-patch14-224'
        model_context_id = '1'

        if image is None:
            return model_name

        if model_context_id not in self.__context:
            context = {
                'model': AutoModelForVision2Seq.from_pretrained(model_name),
                'processor': AutoProcessor.from_pretrained(model_name)
            }
            self.__context[model_context_id] = context

        context = self.__context[model_context_id]
        model = context['model']
        processor = context['processor']
        prompt = "<grounding>An image of"
        #prompt = "<grounding>Describe this image in detail:"

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
    def method2(self, image):
        # https://huggingface.co/microsoft/kosmos-2-patch14-224
        model_name = 'unum-cloud/uform-gen'
        model_context_id = '2'

        if image is None:
            return model_name

        if model_context_id not in self.__context:
            context = {
                'model': VLMForCausalLM.from_pretrained(model_name),
                'processor': VLMProcessor.from_pretrained(model_name)
            }
            self.__context[model_context_id] = context

        context = self.__context[model_context_id]
        model = context['model']
        processor = context['processor']

        # prompt = '[cap] Narrate the contents of the image with precision.'
        # [cap] Summarize the visual content of the image.
        # [vqa] What is the main subject of the image?
        prompt = '[cap] Summarize the visual content of the image.'

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
    def method3(self, image):
        # https://huggingface.co/microsoft/kosmos-2-patch14-224
        model_name = 'Salesforce/instructblip-vicuna-7b'
        model_context_id = '3'

        if image is None:
            return model_name

        if model_context_id not in self.__context:
            context = {
                'model': InstructBlipForConditionalGeneration.from_pretrained(model_name),
                'processor': InstructBlipProcessor.from_pretrained(model_name)
            }
            self.__context[model_context_id] = context

        context = self.__context[model_context_id]
        model = context['model']
        processor = context['processor']

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)

        prompt = "Give a detailed description of this image."

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
    def get_describe_method(self, model_id):
        zeros = len(f'{self.get_method_count()}')
        method_name = f'method{model_id:0{zeros}d}'
        logging.debug(f'describe_method = {method_name}')
        return eval(f'self.{method_name}')


    @classmethod
    def describe(self, model_id, image):
        return self.get_describe_method(model_id)(image)
