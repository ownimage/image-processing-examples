# Create Training Descriptions

## Background

See also [Lightroom AI Description Generation](README.md) which is also contained in this directory and has some general 
information on creating venv and running tests etc.

This task is about automatically creating the descriptions for training LORA (and other such) models.

This idea is that given a directory containing a set of images this will create a .txt file of the same 
base name of the image, containing the descriptions taken from each of the models specified.

## Running
Always need to run the following to activate the virtual environment

```
venv\Scripts\activate
```
### Running Create Training Descriptions
```
CR_TRD.cmd  <model_id>(,model_id)* <directory_path>