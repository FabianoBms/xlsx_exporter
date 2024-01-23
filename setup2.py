from cx_Freeze import setup, Executable


company_name = "BMS Consultoria Tributária"
product_name = "XLSX Exporter"
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "excludes": ["unittest"],
    "zip_include_packages": ["os", "pandas", "bs4", "shutils", "Pillow"],
    "include_files": ["logo.png", "favicon.ico"],
    "include_msvcr": True,
}
bdist_msi_options = {
    "add_to_path": False,
    "initial_target_dir": r"C:\%s\%s" % (company_name, product_name),
}

setup(
    name = "Conversor de eventos para excel",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
    executables=[
        Executable(
            "main.py",
            base="Win32GUI",
            icon="favicon.ico",
            copyright="Copyright (C) 2022 BMS",  
            shortcut_name = "Conversor de eventos para excel",   
            shortcut_dir="DesktopFolder",
        )
    ],
)
