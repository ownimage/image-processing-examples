# TurboXL img2img

## Introduction

What I want to be able to do is to sketch an image in my favorite drawing tool, e.g. PhotoShop or ClipStudio.
And have it generate using StableDiffusion to improve my drawing.

## Notes

You need to have ComfyUI running.
In the CachingImageLoader put the path to your image.
To enable the auto rerun, in ComfyUI, under the 'Queue Prompt' button enable 'Extra Options', then check 'Auto Queue'.
If you get an error with the model the link for it is below.

## Files

|file|notes|
|workflow_api_img2img.json|is the file that was downloaded from the references below|
|image_refiner.json|is the workflow file that I have created.

## Other sources

This will use one of my notes to enable re-reading of a file, which can be found at https://github.com/ownimage/ComfyUI-ownimage.

## References
https://github.com/SharCodin/SDXL-Turbo-ComfyUI-Workflows
https://www.youtube.com/watch?v=FUjBB-2qEUM
Model from https://huggingface.co/stabilityai/sdxl-turbo/resolve/main/sd_xl_turbo_1.0_fp16.safetensors?download=true