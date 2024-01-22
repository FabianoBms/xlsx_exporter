from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"


executables = [Executable(script="main.py", 
                          base=base,                         
                          copyright="Copyright (C) 2024 BMS")]


build_exe_options = {
    "packages": 
        ["csv", "time", "os", "glob", "pathlib"], 
    "includes": 
        ["tkinter"]
    
  }


bdist_msi_options = {
        "add_to_path": False,
        "target_name": "Xlsx Exporter"
    }

setup(
    name = "Xlsx Exporter",
    options = {
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options 
        },
    version = "1.5",
    description = 'Xlsx Exporter',
    executables = executables
)