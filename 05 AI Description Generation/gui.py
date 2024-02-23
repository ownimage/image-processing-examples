import logging
import sys

import gradio as gr

from describe_image import Describe_Image

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
describe_image = Describe_Image()


def describe(dirname, filename, size):
    desc = 'ERROR ERRORERROR'
    try:
        print(f'dirname={dirname} filename={filename}')
        desc = describe_image.describe_image(dirname, filename, size=size)
    except:
        pass
    return desc


demo = gr.Interface(
    fn=describe,
    inputs=["text", "text", "number"],
    outputs=["text"],
)

demo.launch()
