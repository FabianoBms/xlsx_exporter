import json
from cx_Freeze import setup, Executable

# Ler o arquivo JSON de versionamento
with open("version.json", "r") as f:
    version_data = json.load(f)


def get_version():
    return f"{version_data['major']}.{version_data['minor']}.{version_data['patch']}"

if __name__ == "__main__":
    action = str(input("Qual ação (major, minor, patch)? "))
    if action not in ["major", "minor", "patch"]:
        action = "patch"    

    print(action)    
    # Determinar ação de versionamento (maior, menor, patch)
    # Supondo que você tenha uma variável chamada "action" que determina a ação
    if action == "major":
        version_data["major"] += 1
        version_data["minor"] = 0
        version_data["patch"] = 0
    elif action == "minor":
        version_data["minor"] += 1
        version_data["patch"] = 0
    elif action == "patch":
        version_data["patch"] += 1

    # Atualizar o arquivo JSON com a nova versão
    with open("version.json", "w") as f:
        json.dump(version_data, f)

    # Construir o número de versão
    version = f"{version_data['major']}.{version_data['minor']}.{version_data['patch']}"
    
    print("Versão:", version)
    # Restante do seu código setup.py
    company_name = "BMS Consultoria Tributária"
    product_name = "XLSX Exporter"

    build_exe_options = {
        "excludes": ["unittest"],
        "zip_include_packages": ["os", "pandas", "bs4", "shutils", "Pillow"],
        "include_files": ["logo.png", "favicon.ico", "version.json"],
        "include_msvcr": True,
    }

    bdist_msi_options = {
        "add_to_path": False,
        "initial_target_dir": r"C:\%s\%s" % (company_name, product_name),
    }

    
    setup(
        name="Conversor de eventos para excel",
        version=version,
        description="My GUI application!",
        options={"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
        executables=[
            Executable(
                "main.py",
                base="Win32GUI",
                icon="favicon.ico",
                copyright="Copyright (C) 2024 BMS",
                shortcut_name="Conversor de eventos para excel",
                shortcut_dir="DesktopFolder",
            )
        ],
    )
