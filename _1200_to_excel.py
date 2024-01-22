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

# Configurar a formatação de moeda
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def converter_para_moeda(valor):
    try:
        return valor.replace(".", ",")
    except ValueError:
        return valor

def extrair_1200(xml_content):
    def extrair_infoPerApur(ideEstabLot):
        matricula = (
            ideEstabLot.find("matricula").text if ideEstabLot.find("matricula") else 0
        )
        nrInsc = ideEstabLot.find("nrInsc").text
        tpInsc = ideEstabLot.find("tpInsc").text
        codLotacao = ideEstabLot.find("codLotacao").text

        

        tabela_remun = {
            "InscricaoEstabelecimento": formatar_cnpj(nrInsc),
            "TipoInscricao": tpInsc,
            "CodLotacao": codLotacao,
            "Matricula": matricula,
        }

        itensRemuns = ideEstabLot.find_all("itensRemun")
        items = []
        for j, itensRemun in enumerate(itensRemuns):
            CodRubrica = itensRemun.find("codRubr").text
            IdTabRubrica = itensRemun.find("ideTabRubr").text
            vrRubr = itensRemun.find("vrRubr").text
            qtdRubr = (
                itensRemun.find("qtdRubr").text if itensRemun.find("qtdRubr") else ""
            )
            agenteNocivo = ideEstabLot.find("infoAgNocivo")
            grauAgenteNocivo = agenteNocivo.find("grauExp").text if agenteNocivo else ""

            item = {
                "CodRubrica": CodRubrica,
                "IdTabRubrica": IdTabRubrica,
                "ValorRubrica": vrRubr,
                "QuantidadeRubrica": qtdRubr,
                "GrauAgenteNocivo": grauAgenteNocivo,
            }

           
            items.append(item)

        tabela_remun["RubricasRemuneracao"] = items
        return tabela_remun

    def extrair_infoPerAnt(infoperiodo):
        tabela_itensRemunAnt = {
            "nrInsc": infoperiodo.find("nrInsc").text,
            "tpInsc": infoperiodo.find("tpInsc").text,
            "codLotacao": infoperiodo.find("codLotacao").text,
            "Matricula": infoperiodo.find("matricula").text
            if infoPerAnt.find("matricula")
            else 0,
            "RubricasRemuneracao": [],
        }

        itensRemuns = infoperiodo.find_all("itensRemun")
        for itensRemun in itensRemuns:
            item = {
                "CodRubrica": itensRemun.find("codRubr").text,
                "IdTabRubrica": itensRemun.find("ideTabRubr").text,
                "ValorRubrica": itensRemun.find("vrRubr").text,
                "QuantidadeRubrica": itensRemun.find("qtdRubr").text
                if itensRemun.find("qtdRubr")
                else "",
            }

            tabela_itensRemunAnt["RubricasRemuneracao"].append(item)

        return tabela_itensRemunAnt



    new_json = {}
    soup = BeautifulSoup(xml_content, "xml")

    
    

    # raiz
    raiz = soup.find("nrInsc")
    if raiz:
        raiz = raiz.text
    else:
        print("raiz não encontrada")
        return None
        return json.dumps(new_json, ensure_ascii=False, indent=4)

    # evtRemun
    evtRemun = soup.find("evtRemun")
    if evtRemun:
        evtRemun = evtRemun.get("Id")
    else:
        print("evtRemun não encontrado")
        return json.dumps(new_json, ensure_ascii=False, indent=4)

    # perApur
    perApur = soup.find("perApur")
    if perApur:
        perApur = perApur.text
    else:
        print("perApur não encontrado")
        perApur = ""
        pass
 
    cpfTrab = soup.find("cpfTrab").text



    Recibo = soup.find_all("nrRecibo")[-1].text     
    

    DataGeracaoEvento = evtRemun[17:25]
    DataGeracaoEvento = datetime.strptime(DataGeracaoEvento, "%Y%m%d").strftime("%d-%m-%Y")

    
    #new_json["RaizCNPJ"] = raiz
    new_json["IdentificadorEvento"] = evtRemun
    new_json["NumRecibo"] = Recibo
    new_json["CPF"] = formatar_string_para__cpf(cpfTrab)
    #new_json["DataDesligamento"] = ""
    #new_json["TipoEvento"] = "0"
    new_json["DataGeracaoEvento"] = DataGeracaoEvento

    dmDevs = soup.find_all("dmDev")
    lista_dmDev = []

    for  dmDev in dmDevs:
        ideDmDev = dmDev.find("ideDmDev").text
        codCateg = dmDev.find("codCateg").text

        tabela_dmDev = {
            "IdentificadorDemonstrativoPagamento": ideDmDev,
            "CodCategoria": codCateg,
            "RemuneracaoCompetencia": [],
        }

        infoPerApurs = dmDev.find_all("infoPerApur")
        infoPerAnts = dmDev.find_all("infoPerAnt")

        if infoPerApurs:
            for infoPerApur in infoPerApurs:
                ideEstabLots = infoPerApur.find_all("ideEstabLot")

                for ideEstabLot in ideEstabLots:
                    remunPerApurs = ideEstabLot.find_all("remunPerApur")
                    for i, remunPerApur in enumerate(remunPerApurs):
                        try:
                            perApur =datetime.strptime(perApur, "%Y-%m").strftime("%m-%Y")
                        except:
                            pass

                        tabela_dmDev["RemuneracaoCompetencia"].append(
                            {
                                "Competencia": perApur,
                                "BitComplementar": "0",
                                "EstabelecimentoTrabalhador": [
                                    extrair_infoPerApur(ideEstabLot)
                                ],
                            }
                        )

        if infoPerAnts:
            for infoPerAnt in infoPerAnts:
                dsc = infoPerAnt.find("dsc").text
                infoperiodos = infoPerAnt.find_all("idePeriodo")
                for infoperiodo in infoperiodos:
                    tabela_dmDev["RemuneracaoCompetencia"].append(
                        {
                            "Competencia": infoperiodo.find("perRef").text,
                            "BitComplementar": "1",
                            "EstabelecimentoTrabalhador": [
                                extrair_infoPerAnt(infoperiodo)
                            ],
                            "descricao": dsc,
                        }
                    )

        lista_dmDev.append(tabela_dmDev)

    new_json["DemonstrativoTrabalhador"] = lista_dmDev

    return json.dumps(new_json, ensure_ascii=False, indent=4)

def json_to_dataframe(json_content):
    data = json.loads(json_content)

    # DataFrame para as informações gerais
    df_geral = pd.DataFrame([data])

    # DataFrame para as informações de Demonstrativo Trabalhador
    df_dmDev = pd.DataFrame(data["DemonstrativoTrabalhador"])

    # Explodir colunas com listas em novas linhas
    df_dmDev = df_dmDev.explode("RemuneracaoCompetencia").reset_index(drop=True)
    df_dmDev = pd.concat([df_dmDev.drop(["RemuneracaoCompetencia"], axis=1), df_dmDev["RemuneracaoCompetencia"].apply(pd.Series)], axis=1)

    # Explodir a coluna 'EstabelecimentoTrabalhador' e 'RubricasRemuneracao'
    df_dmDev = df_dmDev.explode("EstabelecimentoTrabalhador").reset_index(drop=True)
    df_dmDev = pd.concat([df_dmDev.drop(["EstabelecimentoTrabalhador"], axis=1), df_dmDev["EstabelecimentoTrabalhador"].apply(pd.Series)], axis=1)

    df_dmDev = df_dmDev.explode("RubricasRemuneracao").reset_index(drop=True)
    df_dmDev = pd.concat([df_dmDev.drop(["RubricasRemuneracao"], axis=1), df_dmDev["RubricasRemuneracao"].apply(pd.Series)], axis=1)

    # Repetir informações gerais nas linhas
    df_geral_repeated = pd.concat([df_geral] * len(df_dmDev), ignore_index=True)

    # Adicionar informações gerais repetidas ao DataFrame final
    df_final = pd.concat([df_geral_repeated, df_dmDev], axis=1)
    # Remover a coluna 'DemonstrativoTrabalhador'
    df_final = df_final.drop(['DemonstrativoTrabalhador'], axis=1)
    
    df_final['ValorRubrica'] = df_final['ValorRubrica'].apply(converter_para_moeda)

    return df_final

# Função para processar um arquivo XML e retornar um DataFrame
def processar_xml(xml_path):
    with open(xml_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()
    json_content = extrair_1200(xml_content)
    df = json_to_dataframe(json_content)
    return df

if __name__ == '__main__':

    arquivos_zip = filedialog.askopenfilenames()
    for arquivo_zip in arquivos_zip:
        lista_1200 = (xml for xml in zipfile.ZipFile(arquivo_zip).namelist() if xml.endswith('1200.xml'))
        pasta_1200  = zipfile.ZipFile(arquivo_zip).extractall('1200', members=lista_1200)  
    
    # Lista para armazenar DataFrames individuais
    dfs = []
    # Iterar sobre os arquivos XML na pasta
    # Iterate over the files in the '1200' directory
    for arquivo_xml in os.listdir('1200'):
        # Process each XML file
        if arquivo_xml.endswith('.xml'):
            xml_path = os.path.join('1200', arquivo_xml)
            df = processar_xml(xml_path)
            # Converter os valores da coluna 'ValorRubrica' para moeda
            
            dfs.append(df)
    
    # Concatenar todos os DataFrames em um único DataFrame
    df_final = pd.concat(dfs, ignore_index=True)

    # Salvar DataFrame em um arquivo Excel
    df_final.to_csv(os.path.join('resultado_1200.xlsx'), index=False)