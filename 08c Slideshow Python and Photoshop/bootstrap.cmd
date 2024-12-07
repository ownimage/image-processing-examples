mkdir slideshow
copy highlight\*.* slideshow
copy "P:\git\image-processing-examples\08c Slideshow Python and Photoshop\run.lnk" slideshow
copy "P:\git\image-processing-examples\08c Slideshow Python and Photoshop\refresh.cmd" slideshow
echo Image,Date,Title > slideshow\data.txt
call dir /b slideshow\*.jpg >> slideshow\data.txt
cd slideshow
run.lnk "%cd%\data.txt"
cd ..
del bootstrap.cmd

