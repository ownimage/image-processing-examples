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
2. For each file in the directory it needs to create a file names <filename>.txt with the AI description of the content of the file.
3. I then needs to merge the description into the associated XMP file in the Extended Description
```
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <x:xmpmeta>
        <rdf:Description>
            <Iptc4xmpCore:ExtDescrAccessibility>
                <rdf:Alt>
                    <rdf:li xml:lang="x-default">Hello Ambassador</rdf:li>
                </rdf:Alt>
           </Iptc4xmpCore:ExtDescrAccessibility>
        </rdf:Description>
    </rdf:RDF>
</x:xmpmeta>            
```
Note that the closing for rdf:RDF and x:xmpmeta look wrong

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

