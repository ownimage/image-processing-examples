python timestamp_properties.py run.properties start
:repeat
python add_lr_xmp_description.py 0 %1 || goto :repeat
echo Success!
