# Lightroom AI Description Generation

## Background

I have thousands and thousands of photos that I have taken and filed over the years.  
Almost without exception these do not have any description associated with them.
This means that unless I know the year they were taken, or I can search on what I called the place when I filed them it is difficult/impossible to find anything.

## Proposal

What I need is a tool that can look at a folder (or nested set of folders) and use AI to generate a description of each of the images as a text file.
The tool will then merge it into the Lightroom xmp file.
I will then need to manually trigger a reimport metadata in Lightroom.
I will then be able to search for the values in the description in Lightroom.

## Requirements

1. DONE Needs to work with NEF, DNG, JPG files
2. DONE For each file in the directory it needs to create a file with the AI description of the content of the file.  
This would be one file for the whole directory with one line per file with the filename.xmp, and the new comment.
Note that the xmp files are automatically updated.
3. DONE I then needs to merge the description into the associated XMP file in the UserComment.  
Note that although it suggests that you might be able to have multiple lines, only the first li is used.
```
<x:xmpmeta ...>
 <rdf:RDF ...>
  <rdf:Description ...>
   <exif:UserComment>
    <rdf:Alt>
     <rdf:li xml:lang="x-repair">Line Oney</rdf:li>
    </rdf:Alt>
   </exif:UserComment>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>      
```
4. DONE Should be able to have a description.txt in each folder and add that content to the description if it is present.
5. CLOSED Should include the folder name in the description (if it is not already included in the search)
This is not needed as a search any searchable field will include the folder name
The folder name is alreay in the search
6. Look at this model https://huggingface.co/llava-hf/llava-1.5-7b-hf
7. Does reducing the image size mean that the descriptions process quicker?
8. What stats should be kept (execution, sum of time, sum of time squared, sum of words, sum of words squared ... should this ignore the first run
9. Should be able to add or replace descriptions, and choose which model to add
10. Should I put a gradio front end on this
11. Currently it asks for a model but then adds models 0,1,2 regardless of selection
12. Should I break out the models into a separate directory and scan it, this seems to be a more scalable solution than methods

## Non requirements

1. I am not aiming to do person identification at the moment.


## Getting started

You will need python 3.10.6 (any 3.10 will probably work) and virtualenv.
To install virtual env 
> pip install virtualenv

To create the venv and use it
```
pip -m virtualenv venv
venv\Scripts\activate
```
## Running

```
venv\Scripts\activate
python add_description.py
```

## Running tests
To run the unit tests 
```
python -m uinttest discover
```
To run the e2e tests run
```commandline
TEST.cmd
```
## Todo

1) in add_description.py unpack the image, this means it can be resized as needed.  
This means that this image is passed to the methods rather than the path
2) Allow for multiple methods to be cached, this means that the context needs to be method specific.
3) Have the method that is passed in be a list of methods
4) Test that can write into a single file
5) Test can merge file in 4) into .xml