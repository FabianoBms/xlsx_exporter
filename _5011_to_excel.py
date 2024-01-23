import pandas as pd
import json
from datetime import datetime
from bs4 import BeautifulSoup
import os
import zipfile
import locale
import json
from tkinter import filedialog
from formats import formatar_cnpj, formatar_string_para__cpf
from lendo_planilhas import extrair_5011

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

    # DataFrame para as informações de Demonstrativo Trabalhador
    df_dmDev = pd.DataFrame(data["InfoEmpresa"])

    # Explodir colunas com listas em novas linhas
    df_dmDev = df_dmDev.explode("LotacaoEmpresa").reset_index(drop=True)
    df_dmDev = pd.concat([df_dmDev.drop(["LotacaoEmpresa"], axis=1), df_dmDev["LotacaoEmpresa"].apply(pd.Series)], axis=1)

   
    df_dmDev = df_dmDev.explode("BasesRemuneracaoContribuicao").reset_index(drop=True)
    df_dmDev = pd.concat([df_dmDev.drop(["BasesRemuneracaoContribuicao"], axis=1), df_dmDev["BasesRemuneracaoContribuicao"].apply(pd.Series)], axis=1)

    # Repetir informações gerais nas linhas
    df_geral_repeated = pd.concat([df_geral] * len(df_dmDev), ignore_index=True)

    # Adicionar informações gerais repetidas ao DataFrame final
    df_final = pd.concat([df_geral_repeated, df_dmDev], axis=1)
    # Remover a coluna 'DemonstrativoTrabalhador'
    #df_final = df_final.drop(['DemonstrativoTrabalhador'], axis=1)

    return df_final

# Função para processar um arquivo XML e retornar um DataFrame
def processar_xml(xml_path):
    with open(xml_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()
    json_content = extrair_5011(xml_content)
    df = json_to_dataframe(json_content)
    return df

if __name__ == '__main__':

    arquivos_zip = filedialog.askopenfilenames()
    for arquivo_zip in arquivos_zip:
        lista_5011 = (xml for xml in zipfile.ZipFile(arquivo_zip).namelist() if xml.endswith('5011.xml'))
        pasta_5011  = zipfile.ZipFile(arquivo_zip).extractall('5011', members=lista_5011)  
    
        # Lista para armazenar DataFrames individuais
        dfs = []
        # Iterar sobre os arquivos XML na pasta
        # Iterate over the files in the '5011' directory
        for arquivo_xml in os.listdir('5011'):
            # Process each XML file
            if arquivo_xml.endswith('5011.xml'):
                xml_path = os.path.join('5011', arquivo_xml)
                df = processar_xml(xml_path)
                # Converter os valores da coluna 'ValorRubrica' para moeda
                #df['ValorRubrica'] = df['ValorRubrica'].apply(converter_para_moeda)
                dfs.append(df)
    
    # Concatenar todos os DataFrames em um único DataFrame
    df_final = pd.concat(dfs, ignore_index=True)

    # Salvar DataFrame em um arquivo Excel
    df_final.to_csv(os.path.join('resultado_5011.xlsx'), index=False)