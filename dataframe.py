import pandas as pd
from bs4 import BeautifulSoup
from formats import formatar_cnpj, formatar_string_para__cpf
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from pandas import json_normalize


def to_extrair_5001(xml_content):
    soup = BeautifulSoup(xml_content, "xml")
    evtBasesTrab = soup.find('evtBasesTrab')
    if evtBasesTrab is None:
        return pd.DataFrame()

    evtBasesTrab_id = evtBasesTrab.get('Id')
    nrRecArqBase = soup.find('nrRecArqBase').text
    perApur = soup.find('perApur').text
    cpfTrab = soup.find('cpfTrab').text
    nrInsc = soup.find('nrInsc')
    nrInsc = nrInsc.text if nrInsc else ""
    tpInsc = soup.find('tpInsc').text
    try:
        perApur=datetime.strptime(perApur, "%Y-%m").strftime("%m-%Y"),
        #print(perApur)
    except:
        pass

    tabela = {
        #"RaizCNPJ": nrInsc,
        "IdentificadorEvento": evtBasesTrab_id,
        "NumReciboArquivoBase": nrRecArqBase,
        "CPF": formatar_string_para__cpf(cpfTrab),
        "Competencia": perApur[0],
      
        "EstabelecimentoTrabalhador": []
    }

    infoCpCalcs = soup.find_all('infoCpCalc')
    
    for infoCpCal in infoCpCalcs:
        vrCpSeg = ""
        try:
            vrCpSeg = infoCpCal.find('vrCpSeg')

        except:
            pass
               

        vrDescSeg = infoCpCal.find('vrDescSeg')
        vrDescSeg = vrDescSeg.text if vrDescSeg else ""
 
        ideEstabLots = soup.find_all('ideEstabLot')

        for ideEstabLot in ideEstabLots:
            tpInsc = ideEstabLot.find('tpInsc').text
            nrInsc = ideEstabLot.find('nrInsc').text
            codLotacao = ideEstabLot.find('codLotacao').text
            matricula = ideEstabLot.find('matricula')
            matricula = matricula.text if matricula else ""

            tabela_ideEstabLot = {
                "ValorContribuicaoSegurado": vrCpSeg,
                "ValorDescontoSegurado": vrDescSeg.replace (".", ",") if vrDescSeg else "",
                "TipoInscricao": tpInsc,
                "InscricaoEstabelecimento": formatar_cnpj(nrInsc),
                "CodLotacao": codLotacao,
                'matricula': matricula,
                "InfoCategoria": []
            }

            infoCategIncids = ideEstabLot.find_all('infoCategIncid')

            for infoCategIncid in infoCategIncids:
                codCateg = infoCategIncid.find('codCateg').text

                tabela_infoCategIncid = {                
                    "InfoBaseCalculo": []
                }

                infoBaseCS = infoCategIncid.find_all('infoBaseCS')

                for infoBase in infoBaseCS:
                    ind13 = infoBase.find('ind13').text
                    tpValor = infoBase.find('tpValor').text
                    valor = infoBase.find('valor').text
                    try:
                        valor = datetime.strptime(valor, "%Y-%m").strftime("%m-%Y")
                        print(valor)
                    except:
                        pass

                    item = {       
                        'CodCategoria': codCateg,            
                        "IndDecimoTerceiro": ind13,
                        "TipoValorApuracao": tpValor,
                        "ValorBaseCalculo": valor.replace (".", ",")
                    }

                    tabela_infoCategIncid["InfoBaseCalculo"].append(item)          
                tabela_ideEstabLot["InfoCategoria"].append(tabela_infoCategIncid)
            tabela["EstabelecimentoTrabalhador"].append(tabela_ideEstabLot)
    
        # Converte a coluna 'EstabelecimentoTrabalhador' em DataFrame
        df_estab_trabalhador = pd.DataFrame(tabela.get("EstabelecimentoTrabalhador", [{}]))
        
        if not df_estab_trabalhador.empty:  
            if not df_estab_trabalhador["InfoCategoria"].empty:
                # Explodir as colunas 'InfoCategoria' e 'InfoBaseCalculo' em 'EstabelecimentoTrabalhador'
                df_estab_trabalhador = df_estab_trabalhador.explode("InfoCategoria").reset_index(drop=True)
                df_estab_trabalhador = pd.concat([df_estab_trabalhador.drop(["InfoCategoria"], axis=1), df_estab_trabalhador["InfoCategoria"].apply(pd.Series)], axis=1)
            if not df_estab_trabalhador["InfoBaseCalculo"].empty:
                df_estab_trabalhador = df_estab_trabalhador.explode("InfoBaseCalculo").reset_index(drop=True)
                df_estab_trabalhador = pd.concat([df_estab_trabalhador.drop(["InfoBaseCalculo"], axis=1), df_estab_trabalhador["InfoBaseCalculo"].apply(pd.Series)], axis=1)

        # Repetir informações gerais nas linhas
        try:
            df_geral_repeated = pd.concat([pd.DataFrame([tabela])] * len(df_estab_trabalhador), ignore_index=True)
            # Adicionar informações gerais repetidas ao DataFrame final
            df_final = pd.concat([df_geral_repeated.reset_index(drop=True), df_estab_trabalhador.reset_index(drop=True)] if not df_estab_trabalhador.empty else df_geral_repeated, axis=1)
            # Excluir a coluna 'EstabelecimentoTrabalhador'
            df_final = df_final.drop(['EstabelecimentoTrabalhador'], axis=1)
            

        except:
            df_geral_repeated = pd.DataFrame([tabela])
            #df_final = pd.concat(df_geral_repeated.reset_index(drop=True), axis=1)
            df_final = df_geral_repeated.drop(['EstabelecimentoTrabalhador'], axis=1)

    

        return df_final

if __name__ == "__main__":

    with open(r"C:\Users\frocha\Documents\ePrevCredito\Server\blueprints\extract\functions\output\5001\ID0010000000000000000000006025430730.S-5001.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()

    df_final = to_extrair_5001(xml_content)
    df_final.to_excel('excel.xlsx', index=False)
