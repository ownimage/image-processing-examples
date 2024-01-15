set HF_HUB_DISABLE_SYMLINKS_WARNING=true
REM venv\Scripts\deactivate
REM venv\Scripts\activate

rd /Q /S test
xcopy sample\images\*.* test\test-directory-no-description\
xcopy sample\images\*.* test\test-directory-description\
copy sample\description.txt test\test-directory-description\

python add_description.py 0 test
