@pyinstaller --add-binary=portaudio_x64.dll;. --add-binary=portaudio_x86.dll;. hz.py
@pyinstaller --add-binary=portaudio_x64.dll;. --add-binary=portaudio_x86.dll;. listen.py
@copy dist\hz\hz.exe dist\listen\
@copy dist\hz\hz.exe.manifest dist\listen
@del hz.spec listen.spec
@rd /s /q build __pycache__ dist\hz