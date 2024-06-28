# Overview
This document gives instruction on creating a series of images that are suitable for use as a slideshow.

The specific features of interest of this are that:

1. the images have a title and date superimposed on them
1. the format of the title and date come from template.psd file
2. the data for the files comes from a data.csv file
3. there is an "apply template.exe" which allows the ???

# Issues
There is a bit of clunkyness around where the images go and what they are named.

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
* Copy the `template.psd` into the new `slideshow` directory
* **Copy** the images that you wish to use from the `highlight` directory into the `slideshow` directory
* Open a cmd shell, cd to the `slideshow` directory and enter `dir /b *.jpg > data.csv
* Edit `data.csv`, e.g. in MS Excel, so that it has Image, Date, and Title headings, and enter the values you wish.
e.g.
```
Image,Date,Title
DSC_5501.jpg,2024 06 17,Durham
DSC_5505.jpg,2024 06 17,Durham
```  
Save and close the file.
* Open `template.psd` from the `slideshow` directory.  
* Image -> Variables -> Data Sets
* On the "`Variables`" dialog click "`Import...`"
* On the "`Import Data Set dialog`", 
	* select the `data.csv` you have just created.
	* encoding = Automatic
	* Use First Column for Data Set Names, unchecked
	* Replace Existing Data Sets, checked
	* Click "`OK`"
* On the "`Variables`" dialog click "`OK`"
* "`File`" -> "`Export`" -> "`Data Sets as Files`"
* In the "`Export Data Sets as Files`" dialog,
	* Select your `slideshow` folder
	* Data Set, All Data Sets
	* Leave the File Naming as is
	* File Extension, psd
	* Click `OK`
	* Photoshop will now create one psd file for each of the original images.
* Delete the original jpg files in the `slideshow` folder.
* Open "`File`" -> "`Scripts`" -> "`Image Processor`"
* On the "`Image Processor`" dialog:
	* select the 'slideshow' folder, 
	* save in same location, save as JPEG
	* File Type, Save as JPEG, quality 10
* The images will be in the JPEG directory, move them to the `slideshow` directory, and delete the .psd's, and the template.jpg
* 