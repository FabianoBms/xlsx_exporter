#setup.py
from cx_Freeze import setup, Executable


setup(
    name = "Conversor de eventos para excel",
    version = "1.0.0",
    options = {"build_exe": {
        'packages': ["os","sys","ctypes","win32con","tkinter","PIL","base64","threading","io","tkinter","pandas"],
        'include_files': ["logo.png","favicon.ico"],
        'include_msvcr': True,
    }},
    executables = [Executable("main.py",base="Win32GUI",
                              icon="favicon.ico",
                              copyright="Copyright (C) 2022 BMS",
                            
                              )]
    )