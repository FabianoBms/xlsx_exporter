import pandas as pd
import json
from datetime import datetime
from bs4 import BeautifulSoup
import os
import zipfile
import locale
import json
from tkinter import filedialog
import csv
from dataframe import to_extrair_5001



import json
from bs4 import BeautifulSoup


def salvar_logs(logs):
    with open('logs.txt', 'a', encoding='utf-8') as file:
        file.write(logs + '\n')


def processar_xml(xml_path):
    with open(xml_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()
    try:       
        df = to_extrair_5001(xml_content)          
    except Exception as e:
        logs = f"Erro ao processar o arquivo {xml_path}: {e} - {xml_path}"
        salvar_logs(logs)
        df = pd.DataFrame()
    
    return df




    

if __name__ == '__main__':
    
    arquivos_zip = filedialog.askopenfilenames()
    for arquivo_zip in arquivos_zip:
        lista_5001 = (xml for xml in zipfile.ZipFile(arquivo_zip).namelist() if xml.endswith('5001.xml'))
        pasta_5001  = zipfile.ZipFile(arquivo_zip).extractall('5001', members=lista_5001)  
    
    # Lista para armazenar DataFrames individuais
    dfs = []

    # Iterar sobre os arquivos XML na pasta '5001'
    for i, arquivo_xml_5001 in enumerate(os.listdir('5001')):
        # Processar cada arquivo XML usando a nova função
        if arquivo_xml_5001.endswith('.xml'):
            
            try:
                xml_path_5001 = os.path.join('5001', arquivo_xml_5001)
                df_5001 = processar_xml(xml_path_5001).reset_index(drop=True)
                print(f"Processando o arquivo {i} {arquivo_xml_5001}: {df_5001.shape}'xml_path_5001'")
                dfs.append(df_5001)
                

            except Exception as e:
                print(f"Erro ao processar o arquivo {i} {arquivo_xml_5001}: {e}")
                continue
   # Iterar sobre os DataFrames na lista dfs e resetar os índices
    for i in range(len(dfs)):
        dfs[i] = dfs[i].reset_index(drop=True)

    # Verificar se há índices duplicados
    for i, df in enumerate(dfs):
        if df.index.duplicated().any():
            print(f"Índices duplicados encontrados no DataFrame {i}.")

    try:
        # Concatenar todos os DataFrames na lista dfs
        df_final = pd.concat(dfs, ignore_index=True)
    except Exception as e:
        print(f"Erro ao concatenar os DataFrames: {e}")
        salvar_logs(f"Erro ao concatenar os DataFrames: {e}")
         

    # Salvar DataFrame em um arquivo Excel
    df_final.to_csv(os.path.join('resultado_5001.xlsx'), index=False)
