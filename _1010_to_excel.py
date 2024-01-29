import pandas as pd
import json
from datetime import datetime
import os
import zipfile
import locale
import json
from tkinter import filedialog
from formats import formatar_cnpj
from lendo_planilhas import extrair_1010

# Configurar a formatação de moeda
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def converter_para_moeda(valor):
    try:
        return valor.replace(".", ",")
    except ValueError:
        return valor



def json_to_dataframe(json_content):
    data = json.loads(json_content)

    # DataFrame para as informações gerais
    df_geral = pd.DataFrame([data])

   

    return df_geral

# Função para processar um arquivo XML e retornar um DataFrame
def processar_xml(xml_path):
    with open(xml_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()
    json_content = extrair_1010(xml_content)
    df = json_to_dataframe(json_content)
    return df

if __name__ == '__main__':

    arquivos_zip = filedialog.askopenfilenames()
    for arquivo_zip in arquivos_zip:
        lista_1010 = (xml for xml in zipfile.ZipFile(arquivo_zip).namelist() if xml.endswith('1010.xml'))
        pasta_1010  = zipfile.ZipFile(arquivo_zip).extractall('1010', members=lista_1010)  
    
    # Lista para armazenar DataFrames individuais
    dfs = []
    # Iterar sobre os arquivos XML na pasta
    # Iterate over the files in the '1010' directory
    for arquivo_xml in os.listdir('1010'):
        # Process each XML file
        if arquivo_xml.endswith('.xml'):
            xml_path = os.path.join('1010', arquivo_xml)
            df = processar_xml(xml_path)
            # Converter os valores da coluna 'ValorRubrica' para moeda            
            dfs.append(df)
    
    # Concatenar todos os DataFrames em um único DataFrame
    df_final = pd.concat(dfs, ignore_index=True)

    # Salvar DataFrame em um arquivo Excel
    df_final.to_csv(os.path.join('resultado_1010.xlsx'), index=False)