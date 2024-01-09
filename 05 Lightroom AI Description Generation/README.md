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

1. Needs to work with NEF, DNG, JPG files
2. For each file in the directory it needs to create a file with the AI description of the content of the file.  
This would be one file for the whole directory with one line per file with the filename.xmp, and the new comment.
3. I then needs to merge the description into the associated XMP file in the UserComment.  
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
```
python test_xmp_processor.py -v
```
## Todo

1) in add_description.py unpack the image, this means it can be resized as needed.  
This means that this image is passed to the methods rather than the path
2) Allow for multiple methods to be cached, this means that the context needs to be method specific.
3) Have the method that is passed in be a list of methods
4) Test that can write into a single file
5) Test can merge file in 4) into .xml