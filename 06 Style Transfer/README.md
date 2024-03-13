# Style Transfer

## Background

The idea of this is that I want to be able to copy the style of a bunch of images and use txt2img
to create images of a similar style.

This assumes that the checkpoint, and LORA has been trained (see 03 Lora Training)

This should contain the comfyUI workflow to make this work, "Style Transfer.json".

This should include:
1. checkpoint
2. LORA
3. additional description in the text
4. IP adapter
5. hypernetwork
6. textual inversion
7. anything else I can train

The "Style Transfer.json" started life as the "IP Adapter.json" in "../04 IP Adapter".