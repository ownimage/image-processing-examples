# Introduction

The purpose of this is to create a yearbook from all the slideshows that have been created (see 08c ...)

# Method overview

Given a year directory
This will create a yearbook sub-directory
Treewalk the directories in the year looking for year/x/slideshow or year/w/x/slideshow directory
It will then loop through all the jpgs in the slideshow directory
    copy them to the yearbook subdirectory renaming them with their parent direcotry name <x>_filename.jpg


