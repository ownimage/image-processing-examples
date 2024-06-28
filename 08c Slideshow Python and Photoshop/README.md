# Overview
This document gives instruction on creating a series of images that are suitable for use as a slideshow.

The specific features of interest of this are that:

1. the images have a title and date superimposed on them
1. the format of the title and date come from template.psd file
2. the data for the files comes from a data.csv file

# Assumptions, pre-requisites and directory structure
My normal working practice is for each days shoot to have a directory of images in NEF format, with a sub directory origJPG for the original jpgs, e.g.

Then a separate directory called highlight with the processed highlight images.

```
20240619 - Rookhope
|-- highlight
|   |-- 002.jpg
|-- origJPG
|   |--	001.jpg
|   |--	002.jpg
|-- 001.NEF
|-- 002.NEF
```
Into that I will add a `slideshow` directory where the final set of files will reside.

The templates are designed for use with files that fit into 1920x1080 resolution.

# Instructions
1. into the base directory (the one that contains highlight) copy bootstrap.cmd and run it.  This will create the slideshow directory and copy the highlight images into it. 
2. go to the slideshow directory
3. copy create_data_txt.cmd and "run.cmd Shortcut.lnk" into it
4. run the create_data_txt.cmd.  This will create a file called data.txt, fill it with the names of the files in the directory, and delete the create_data_txt.cmd file.
5. Edit the data.txt to add the dates and titles for the files
6. drop the data.txt onto the "run.cmd Shortcut.lnk"

# Problems
You might need to re-create the run.cmd shortcut and rename it to run.



# References


https://martechwithme.com/photoshop-scripting-with-python-on-windows/

Controlling photoshop with Python

https://loonghao.github.io/photoshop-python-api/examples/#replace-images

https://photoshop-python-api.readthedocs.io/en/master/examples.html?highlight=select%20layer#load-selection

https://github.com/loonghao/photoshop-python-api/issues/38

Interesting PS API
https://loonghao.github.io/photoshop-python-api/reference/photoshop/api/_document/