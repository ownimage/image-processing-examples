set HF_HUB_DISABLE_SYMLINKS_WARNING=true
venv\Scripts\deactivate
venv\Scripts\activate
del /Q test\test-directory\*.*
xcopy test\images\*.* test\test-directory\
python add_description.py test\test-directory
