@pyinstaller hz.py
@copy portaudio_x64.dll dist\hz\
@del hz.spec
@rd /s /q build __pycache__