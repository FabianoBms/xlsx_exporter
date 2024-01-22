import tkinter as tk
from tkinter import filedialog
import os
import zipfile
import time
from datetime import timedelta

PATHS = []

NOMES_ARQUIVOS = [
    "5011.xml",
    "1010.xml",
    "1200.xml",
    "2299.xml",
    "5001.xml"
]

def extrair_zip(nome_arquivo_zip, nomes_arquivos, diretorio_saida):
    try:
        with zipfile.ZipFile(nome_arquivo_zip, 'r') as zip_ref:
            for nome_arquivo in nomes_arquivos:
                for filename in zip_ref.namelist():
                    if filename.endswith(nome_arquivo):
                        caminho_pasta_especifica = os.path.join(diretorio_saida, nome_arquivo.replace('.xml', ''))
                        if not os.path.exists(caminho_pasta_especifica):
                            os.makedirs(caminho_pasta_especifica)
                        caminho_arquivo_saida = os.path.join(caminho_pasta_especifica, os.path.basename(filename))
                        zip_ref.extract(filename, caminho_pasta_especifica)
    except Exception as e:
        print('Erro ao extrair os arquivos do zip', e)
    finally:
        print('Extração concluída :', nome_arquivo_zip)

def listar_arquivos_zip_em_pasta(main_folder):
    folder_list = [os.path.join(main_folder, folder) for folder in os.listdir(main_folder) if
                   os.path.isdir(os.path.join(main_folder, folder))]
    zip_files_dict = {}

    for folder in folder_list:
        zip_files = [f for f in os.listdir(folder) if f.endswith('.zip')]
        if zip_files:
            zip_files_dict[os.path.basename(folder)] = zip_files
    return zip_files_dict

def automate_extract(output_folder, main_folder, _dict):
    for nome_pasta, nomes_arquivos_zip in _dict.items():
        for nome_arquivo_zip in nomes_arquivos_zip:
            caminho_zip = os.path.join(main_folder, nome_pasta, nome_arquivo_zip)
            extrair_zip(caminho_zip, NOMES_ARQUIVOS, output_folder)

def main():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter

    main_folder = filedialog.askdirectory(title="Selecione a pasta principal")
    output_folder = os.path.join(os.path.dirname(__file__), "output")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    dicionario = listar_arquivos_zip_em_pasta(main_folder)
    print(dicionario)
    print("Output_folder: " + output_folder)

    automate_extract(output_folder, main_folder, dicionario)

if __name__ == "__main__":
    start_time = time.time()

    print("Automatizando...")

    main()

    end_time = time.time()
    total_time = end_time - start_time

    formatted_time = str(timedelta(seconds=int(total_time)))
    print(f"Tempo total de extração: {formatted_time}")
