import logging
import sys

import gradio as gr

from describe_image import describe_image

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def greet(dirname, filename):
    print(f'dirname={dirname} filename={filename}')
    return describe_image(dirname, filename)


demo = gr.Interface(
    fn=greet,
    inputs=["text", "text"],
    outputs=["text"],
)

demo.launch()
