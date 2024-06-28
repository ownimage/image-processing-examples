echo Image,Date,Title > data.txt
call dir /b *.jpg >> data.txt
del create_data_txt.cmd