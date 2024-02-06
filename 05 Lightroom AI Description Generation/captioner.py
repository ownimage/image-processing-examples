import logging
from timeit import default_timer as timer

import torch
from transformers import AutoProcessor, AutoModelForVision2Seq, LlavaForConditionalGeneration
from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration, BlipProcessor, \
    BlipForConditionalGeneration
from uform.gen_model import VLMForCausalLM, VLMProcessor

from stats import Stats


class Captioner:

    def __init__(self):
        self.__context = {}
        self.__stats = Stats()
        logging.info(f'torch.cuda.is_available() -> {torch.cuda.is_available()}')

    @staticmethod
    def get_method_count():
        return 5

    def method0(self, image, prompt=None):
        default_prompt = 'This is a picture of'
        prompt = default_prompt if prompt is None else prompt
        # https://huggingface.co/tasks/image-to-text
        model_name = 'Salesforce/blip-image-captioning-base'
        model_context_id = '0'

        if image is None:
            return model_name

        if model_context_id not in self.__context:
            context = {
                'processor': BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base"),
                'model': BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(
                    "cuda")
            }
            self.__context[model_context_id] = context

        context = self.__context[model_context_id]
        processor = context['processor']
        model = context['model']

        inputs = processor(image, prompt, return_tensors="pt").to("cuda")

        out = model.generate(**inputs, max_new_tokens=128)

        return processor.decode(out[0], skip_special_tokens=True)

    def method1(self, image, prompt=None):
        default_prompt = '<grounding>An image of'
        prompt = default_prompt if prompt is None else prompt
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

    def method2(self, image, prompt=None):
        default_prompt = '[cap] Summarize the visual content of the image.'
        prompt = default_prompt if prompt is None else '[cap] ' + prompt
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

    def method3(self, image, prompt=None):
        default_prompt = 'Give a detailed description of this image.'
        prompt = default_prompt if prompt is None else prompt
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

    def method4(self, image, prompt=None):
        model_context_id = '4'
        model_name = 'llava-hf/llava-1.5-7b-hf'
        default_prompt = 'USER: <image>\nDescribe this image in more detail'
        # https://huggingface.co/llava-hf/llava-1.5-7b-hf

        if image is None:
            return model_name

        prompt = default_prompt if prompt is None else prompt

        if model_context_id not in self.__context:
            context = {
                'model': LlavaForConditionalGeneration.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16,
                    low_cpu_mem_usage=True
                ).to(0),
                'processor': AutoProcessor.from_pretrained(model_name)
            }
            self.__context[model_context_id] = context

        context = self.__context[model_context_id]
        model = context['model']
        processor = context['processor']

        inputs = processor(prompt, image, return_tensors='pt').to(0, torch.float16)
        output = model.generate(**inputs, max_new_tokens=200, do_sample=False)
        generated_text = processor.decode(output[0][2:], skip_special_tokens=True)
        generated_text = generated_text.replace('ER:', '')
        generated_text = generated_text.replace('\n', '')
        generated_text = generated_text.strip()
        generated_text = generated_text.replace('Describe this image in more detail.', '')
        generated_text = generated_text.replace('.', '. ')
        generated_text = generated_text.replace('  ', ' ')
        generated_text = generated_text.rstrip()
        return generated_text

    def get_describe_method(self, model_id):
        zeros = len(f'{self.get_method_count()}')
        method_name = f'method{model_id:0{zeros}d}'
        logging.debug(f'describe_method = {method_name}')
        return eval(f'self.{method_name}')

    def get_stats(self):
        return self.__stats.get()

    def describe(self, model_id, image, prompt=None):
        start = timer()
        description = self.get_describe_method(model_id)(image, prompt)
        logging.debug(description)
        end = timer()
        word_count = len(description.split())
        duration = end - start
        logging.info(f'duration = {duration}')  # Time in seconds, e.g. 5.38091952400282
        self.__stats.add(model_id, duration, word_count)
        return description
