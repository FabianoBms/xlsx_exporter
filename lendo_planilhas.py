from bs4 import BeautifulSoup
import os
import json
#from connect import conectar
import pyperclip
from datetime import datetime
import time
from formats import formatar_cnpj, formatar_string_para__cpf

def extrair_1010(xml_content):
    new_dict = {}
    soup = BeautifulSoup(xml_content, "xml")
    evtTabRubrica = soup.find("evtTabRubrica").get("Id")  # 1x
    nrRecibo = soup.find("nrRecibo").text  # 1x
    tpInsc = soup.find("tpInsc").text  # 1x
    nrInsc = soup.find("nrInsc").text  # 8, 11 ou 14
    inclusao = soup.find("inclusao")  # 0-1x
    alteracao = soup.find("alteracao")  # 0-1x
    exclusao = soup.find("exclusao")  # 0-1x

    tabela = {
        "evtTabRubrica": evtTabRubrica,
        "nrRecibo": nrRecibo,
        "tpInsc": tpInsc,
        "nrInsc": nrInsc,
    }

    if inclusao:
        codRubr = inclusao.find("codRubr").text
        ideTabRubr = inclusao.find("ideTabRubr").text
        iniValid = inclusao.find("iniValid").text
        dscRubr = inclusao.find("dscRubr")
        if dscRubr != None: dscRubr = dscRubr.text
        else: dscRubr = ""
        natRubr = inclusao.find("natRubr").text
        tpRubr = inclusao.find("tpRubr").text
        codIncCP = inclusao.find("codIncCP").text
        codIncIRRF = inclusao.find("codIncIRRF").text
        codIncFGTS = inclusao.find("codIncFGTS").text        
        fimValid = ""
        if inclusao.find("fimValid") != None: fimValid = inclusao.find("fimValid").text     
            
        tabela_inclusao = {
            "tipo": 0,
            "codRubr": codRubr,
            "ideTabRubr": ideTabRubr,
            "iniValid": iniValid,
            "fimValid": fimValid,
            "dscRubr": dscRubr,
            "natRubr": natRubr,
            "tpRubr": tpRubr,
            "codIncCP": codIncCP,
            "codIncIRRF": codIncIRRF,
            "codIncFGTS": codIncFGTS,
        }
        tabela.update(tabela_inclusao)
        
    elif alteracao:
        codRubr = alteracao.find("codRubr").text
        ideTabRubr = alteracao.find("ideTabRubr").text
        iniValid = alteracao.find("iniValid").text
        dscRubr = alteracao.find("dscRubr")
        if dscRubr != None: dscRubr = dscRubr.text
        else: dscRubr = ""
        natRubr = alteracao.find("natRubr").text
        tpRubr = alteracao.find("tpRubr").text
        codIncCP = alteracao.find("codIncCP").text
        codIncIRRF = alteracao.find("codIncIRRF").text
        codIncFGTS = alteracao.find("codIncFGTS").text

        if alteracao.find("fimValid") != None: fimValid = alteracao.find("fimValid").text
        tipo = 1
        
        fimValid = alteracao.find("fimValid")
        if fimValid != None: fimValid = fimValid.text
        tabela_alteracao = {
            "tipo": tipo,
            "codRubr": codRubr,
            "ideTabRubr": ideTabRubr,
            "iniValid": iniValid,
            "fimValid": fimValid,
            "dscRubr": dscRubr,
            "natRubr": natRubr,
            "tpRubr": tpRubr,
            "codIncCP": codIncCP,
            "codIncIRRF": codIncIRRF,
            "codIncFGTS": codIncFGTS,
        }
        tabela.update(tabela_alteracao)

    elif exclusao:
        codRubr = exclusao.find("codRubr").text
        ideTabRubr = exclusao.find("ideTabRubr").text
        iniValid = exclusao.find("iniValid").text
        dscRubr = ""
     
        fimValid = exclusao.find("fimValid")
        if fimValid != None: fimValid = fimValid.text
        tabela_exclusao = {
            "tipo": 2,
            "codRubr": codRubr,
            "ideTabRubr": ideTabRubr,
            "iniValid": iniValid,
            "dscRubr": dscRubr,
            "fimValid": fimValid,
            "tpRubr": "",
            "natRubr": "",
             "codIncCP": "",
            "codIncIRRF": "",
            "codIncFGTS": "",
        }
        tabela.update(tabela_exclusao)        
    else:
        pass
    
    new_dict = json.dumps(tabela, ensure_ascii=False)
    #print(new_dict)
    return new_dict

def inserir_1010(json, conn):
    if conn:
        cursor = conn.cursor()
        sql = f'''\
            SET NOCOUNT ON;
            DECLARE @pRetornoMSG NVARCHAR(255),
                    @pRetornoOP int

            EXEC [InsercaoEventoS1010]
                @pRaizCNPJ = '{json["nrInsc"]}',
                @pIdentificadorEvento = '{json["evtTabRubrica"]}',
                @pNumRecibo = '{json["nrRecibo"]}',
                @pCodRubrica = '{json["codRubr"]}',
                @pIdTabRubrica = '{json["ideTabRubr"]}',
                @pInicioValidade = '{json["iniValid"]}',
                @pFimValidade = '',
                @pDescricaoRubrica = '{json["dscRubr"]}',
                @pCodTipoRubrica = '{json["tpRubr"]}',
                @pTipoInformacao = '{json["tipo"]}',
                @pNaturezaRubrica = '{json["natRubr"]}',
                @pCodIncidenciaPrevidSocial = '{json["codIncCP"]}',
                @pCodIncidenciaIRRF = '{json["codIncIRRF"]}',
                @pCodIncidenciaFGTS = '{json["codIncFGTS"]}',
                @pRetornoOP = @pRetornoOP OUTPUT,
                @pRetornoMSG = @pRetornoMSG OUTPUT;
            SELECT @pRetornoOP as RetornoOP, @pRetornoMSG as RetornoMSG;
            '''
        try:
            cursor.execute(sql)
            retorno = cursor.fetchall()

            if retorno[0][0] == 1:
                return 1
            else:
                return retorno[0][1]
        except Exception as e:
            return e
        
def extrair_1200(xml_content):
    def extrair_infoPerApur(ideEstabLot):
        matricula = (
            ideEstabLot.find("matricula").text if ideEstabLot.find("matricula") else 0
        )
        nrInsc = ideEstabLot.find("nrInsc").text
        tpInsc = ideEstabLot.find("tpInsc").text
        codLotacao = ideEstabLot.find("codLotacao").text
        

        tabela_remun = {
            "InscricaoEstabelecimento": nrInsc,
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
    DataGeracaoEvento = datetime.strptime(DataGeracaoEvento, "%Y%m%d").strftime("%Y-%m-%d")
    
    new_json["RaizCNPJ"] = raiz
    new_json["IdentificadorEvento"] = evtRemun
    new_json["NumRecibo"] = Recibo
    new_json["CPF"] = formatar_string_para__cpf(cpfTrab)
    new_json["DataDesligamento"] = ""
    new_json["TipoEvento"] = "0"
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





def inserir_1200(json, conn):
    cursor = conn.cursor()

    sql = f"""\
        DECLARE @pRetornoOP int,
                @pRetornoMSG nvarchar(255)

        EXEC    InsercaoEventoS1200
                @pJSONTrabalhadores = N'{json}',
                @pRetornoOP = @pRetornoOP OUTPUT,
                @pRetornoMSG = @pRetornoMSG OUTPUT

        SELECT  @pRetornoOP as N'@pRetornoOP',
        @pRetornoMSG as N'@pRetornoMSG' """
    
    try:
        cursor.execute(sql)
        retorno = cursor.fetchall()

        if retorno[0][0] == 1:
            return 1
        
        else:
            return retorno[0][1]
        
    except Exception as e:
        print(e)
        return e


def extrair_2299(xml_content):

    def extrair_infoPerApur(ideEstabLot, matr):
        matricula = matr
        nrInsc = ideEstabLot.find("nrInsc").text
        tpInsc = ideEstabLot.find("tpInsc").text
        codLotacao = ideEstabLot.find("codLotacao").text

        tabela_remun = {
            "InscricaoEstabelecimento": nrInsc,
            "TipoInscricao": tpInsc,
            "CodLotacao": codLotacao,
            "Matricula": matricula,
        }

        detVerbas = ideEstabLot.find_all("detVerbas")
        items = []
        for j, detVerbas in enumerate(detVerbas):
            CodRubrica = detVerbas.find("codRubr").text
            IdTabRubrica = detVerbas.find("ideTabRubr").text
            vrRubr = detVerbas.find("vrRubr").text
            qtdRubr = (
                detVerbas.find("qtdRubr").text if detVerbas.find("qtdRubr") else ""
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
        try:
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
        except Exception as e:
            print(e)        

        return tabela_itensRemunAnt

    try:

        new_json = {}
        soup = BeautifulSoup(xml_content, "xml")

        # raiz
        raiz = soup.find("nrInsc")
        if raiz:
            raiz = raiz.text
        else:
            print("raiz não encontrada")
            return json.dumps(new_json, ensure_ascii=False, indent=4)

        # evtDeslig
        evtDeslig = soup.find("evtDeslig")
        if evtDeslig:
            evtDeslig = evtDeslig.get("Id")
        else:
            print("evtDeslig não encontrado")
            return json.dumps(new_json, ensure_ascii=False, indent=4)

        # dtDeslig
        dtDeslig = soup.find("dtDeslig")
        if dtDeslig:
            dtDeslig = dtDeslig.text
        else:
            print("dtDeslig não encontrado")
            dtDeslig = ""
            pass
    
        cpfTrab = soup.find("cpfTrab").text
        nrRecibo = soup.find_all("nrRecibo")[-1].text
        matricula = soup.find("matricula").text
        DataGeracaoEvento = evtDeslig[17:25]
        DataGeracaoEvento = datetime.strptime(DataGeracaoEvento, "%Y%m%d").strftime("%Y-%m-%d")
        
        new_json["RaizCNPJ"] = raiz
        new_json["IdentificadorEvento"] = evtDeslig
        new_json["NumRecibo"] = nrRecibo
        new_json["CPF"] = cpfTrab
        new_json["DataDesligamento"] = dtDeslig
        new_json["TipoEvento"] = "1"
        new_json["DataGeracaoEvento"] = DataGeracaoEvento

        dmDevs = soup.find_all("dmDev")

        lista_dmDev = []

        for  dmDev in dmDevs:
            ideDmDev = dmDev.find("ideDmDev").text
        

            tabela_dmDev = {
                "IdentificadorDemonstrativoPagamento": ideDmDev,
            
                "RemuneracaoCompetencia": [],
            }

            infoPerApurs = dmDev.find_all("infoPerApur")
            infoPerAnts = dmDev.find_all("infoPerAnt")

            if infoPerApurs:
                for infoPerApur in infoPerApurs:
                    ideEstabLots = infoPerApur.find_all("ideEstabLot")

                    for ideEstabLot in ideEstabLots:
                        detVerbass = ideEstabLot.find_all("detVerbas")                   
                        tabela_dmDev["RemuneracaoCompetencia"].append(
                            {
                                "Competencia": dtDeslig[0:7],
                                "BitComplementar": "0",
                                "EstabelecimentoTrabalhador": [
                                    extrair_infoPerApur(ideEstabLot, matricula)
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
                                "Competencia": infoperiodo.find("perRef").text[0:7],
                                "BitComplementar": "1",
                                "EstabelecimentoTrabalhador": [
                                    extrair_infoPerAnt(infoperiodo)
                                ],
                                "descricao": dsc,
                            }
                        )

            lista_dmDev.append(tabela_dmDev)

        new_json["DemonstrativoTrabalhador"] = lista_dmDev

        

    except Exception as e:
        print(e)

    return json.dumps(new_json, ensure_ascii=False, indent=4)


def inserir_2299(json, conn):
    cursor = conn.cursor()

    sql = f"""\
        DECLARE	@pRetornoOP int,
                @pRetornoMSG nvarchar(255)

        EXEC	InsercaoEventoS2299
                @pJSONTrabalhadores = '{json}',
                @pRetornoOP = @pRetornoOP OUTPUT,
                @pRetornoMSG = @pRetornoMSG OUTPUT

        SELECT	@pRetornoOP as N'@pRetornoOP',
                @pRetornoMSG as N'@pRetornoMSG' 
        """
    
    try:
        cursor.execute(sql)
        retorno = cursor.fetchall()

        if retorno[0][0] == 1:
            return 1
        
        else:
            return retorno[0][1]
        
    except Exception as e:
        print(e)
        return e   
    

def extrair_5001(xml_content):
    
    soup = BeautifulSoup(xml_content, "xml") 
     
    evtBasesTrab = soup.find('evtBasesTrab')
    if evtBasesTrab == None: return {}   
    else : evtBasesTrab = evtBasesTrab.get('Id')
    nrRecArqBase = soup.find('nrRecArqBase').text
    perApur = soup.find('perApur').text
    cpfTrab = soup.find('cpfTrab').text
    nrInsc = soup.find('nrInsc')
    if nrInsc == None: nrInsc = ""
    else: nrInsc = nrInsc.text
    tpInsc = soup.find('tpInsc').text
       
    tabela = {
        "RaizCNPJ": nrInsc,
        "IdentificadorEvento": evtBasesTrab,     
        "NumReciboArquivoBase": nrRecArqBase,
        "CPF": cpfTrab,
        "Competencia": perApur        
        }
    
    infoCpCalcs = soup.find_all('infoCpCalc')
    #print(len(infoCpCalcs))
    lista_infoCpCal = []

    if len(infoCpCalcs) ==0:
        tabela['ContribuicoesSegurado'] = lista_infoCpCal
        
    else:
        pass

    for infoCpCal in infoCpCalcs:
        vrCpSeg = infoCpCal.find('vrCpSeg')
        if vrCpSeg == None: vrCpSeg = ""
        else: vrCpSeg = vrCpSeg.text

        vrDescSeg = infoCpCal.find('vrDescSeg')
        if vrDescSeg == None: vrDescSeg = ""
        else: vrDescSeg = vrDescSeg.text

        tabela_infoCpCal = {
                "ValorContribuicaoSegurado": vrCpSeg,
                "ValorDescontoSegurado": vrDescSeg
                }
        #print(tabela_infoCpCal)

        lista_infoCpCal.append(tabela_infoCpCal)
    tabela['ContribuicoesSegurado'] = lista_infoCpCal

        
    try:
        infoCp = soup.find('infoCp')
        lista_infoCp = []

        if infoCp == None: 
            tabela['EstabelecimentoTrabalhador'] = lista_infoCp
            return json.dumps(tabela)

        ideEstabLots = infoCp.find_all('ideEstabLot')
        
        for index, ideEstabLot in enumerate(ideEstabLots):           
            tpInsc = ideEstabLot.find('tpInsc').text
            nrInsc = ideEstabLot.find('nrInsc').text
            codLotacao = ideEstabLot.find('codLotacao').text
            matricula = ideEstabLot.find('matricula')
            if matricula == None: matricula = ""
            else: matricula = matricula.text

            tabela_ideEstabLot = {
                "TipoInscricao": tpInsc,
                "InscricaoEstabelecimento": nrInsc,
                "CodLotacao": codLotacao,
                'matricula': matricula,                
            }
            lista_infoCp.append(tabela_ideEstabLot)

            tabela['EstabelecimentoTrabalhador'] = lista_infoCp

            infoCategIncids = ideEstabLot.find_all('infoCategIncid') 
            lista_infoCategIncid = []
            for ii, infoCategIncid in enumerate(infoCategIncids):
                
                codCateg = infoCategIncid.find('codCateg').text

                tabela_infoCategIncid = {                    
                    'CodCategoria':codCateg,
                    "InfoBaseCalculo": []
                }

                lista_infoCategIncid.append(tabela_infoCategIncid)
                tabela['EstabelecimentoTrabalhador'][index]["InfoCategoria"] = lista_infoCategIncid

                infoBaseCS = infoCategIncid.find_all('infoBaseCS')
                if infoBaseCS == None:
                    return json.dumps(tabela)
                items = []
                for j,infoBase in enumerate(infoBaseCS):
                    ind13 = infoBase.find('ind13').text 
                    tpValor = infoBase.find('tpValor').text
                    valor = infoBase.find('valor').text

                    item = {
                    "CodCategoria": "101",
                    "IndDecimoTerceiro": ind13,
                    "TipoValorApuracao": tpValor,
                    "ValorBaseCalculo": valor
                    }
                    items.append(item)

            tabela ['EstabelecimentoTrabalhador'][index] ['InfoCategoria'][ii]['InfoBaseCalculo']  = items
    
    
    except Exception as e:
        #print(evtBasesTrab)
        print(f"error{e}")

    #print(tabela)
    new_dict = json.dumps(tabela)
    return new_dict


def inserir_5001(json,conn):
    cursor = conn.cursor()
    sql = f'''\
            DECLARE @pRetornoOP int,
                @pRetornoMSG nvarchar(255)

        EXEC	InsercaoEventoS5001
                @pJSONTrabalhadores = '{json}',
                @pRetornoOP = @pRetornoOP OUTPUT,
                @pRetornoMSG = @pRetornoMSG OUTPUT

        SELECT	@pRetornoOP as N'@pRetornoOP',
                @pRetornoMSG as N'@pRetornoMSG'

    '''
    try:
        cursor.execute(sql)
        retorno = cursor.fetchall()

        if retorno[0][0] == 1:
            return 1
        
        else:
            return retorno[0][1]
        
    except Exception as e:
        
        return e
    

def extrair_5011(xml_content, to="json"):
    dfs = []
    soup = BeautifulSoup(xml_content, "xml")   
    evtCS = soup.find('evtCS').get('Id')   
    
    perApur = soup.find('perApur').text
    nrInsc = soup.find('nrInsc').text
    nrRecArqBase = soup.find('nrRecArqBase').text       
    ideEstabs = soup.find_all('ideEstab') 

       
    tabela = {
        'RaizCNPJ': nrInsc,
        'IdentificadorEvento': evtCS,
        'NumRecibo': nrRecArqBase,        
        'Competencia': perApur,       
    }   

    lista_ideEstab = []
    lista_LotEmpresa = []
    for i, ideEstab in enumerate(ideEstabs):
        
        basesRemuns=ideEstab.find_all('basesRemun')
        listaBaseRemun = []
        for j,baseRemun in enumerate(basesRemuns):

            tabela3 = {
                'CodCategoria' : baseRemun.find('codCateg').text,
                'ValorBaseCP' : baseRemun.find('vrBcCp00').text,
                'ValorBaseCP15' : baseRemun.find('vrBcCp15').text,
                'ValorBaseCP20' : baseRemun.find('vrBcCp20').text,
                'ValorBaseCP25' : baseRemun.find('vrBcCp25').text,                
            }   
            listaBaseRemun.append(tabela3)

        tabelaInfoEmpresa = {
            'TipoInscricao': ideEstab.find('tpInsc').text,
            'InscricaoEstabelecimento': ideEstab.find('nrInsc').text,
            'CNAE' : ideEstab.find('cnaePrep').text,
            'AliquotaRAT': ideEstab.find('aliqRat').text,
            'FAP': ideEstab.find('fap').text,
            'RATAJust': ideEstab.find('aliqRatAjust').text,
            "LotacaoEmpresa":
            [
                {
                    "CodLotacao": ideEstab.find('codLotacao').text,
                    "FPAS": ideEstab.find('fpas').text,
                    "CodTerceiros": ideEstab.find('codTercs').text,
                    "BasesRemuneracaoContribuicao":listaBaseRemun,
                }
            ]
        }
        lista_ideEstab.append(tabelaInfoEmpresa)
        tabela['InfoEmpresa'] = lista_ideEstab

 
    if to == "clipboard":
         pyperclip.copy(json.dumps(tabela))
    elif to == "dict":
        return tabela
    else :
        return json.dumps(tabela)


def inserir_5011(json, conn):
    cursor = conn.cursor()

    sql = f"""\
        DECLARE @pRetornoOP int,
                @pRetornoMSG nvarchar(255)

        EXEC	InsercaoEventoS5011
                @pJSONTrabalhadores = '{json}',
                @pRetornoOP = @pRetornoOP OUTPUT,
                @pRetornoMSG = @pRetornoMSG OUTPUT

        SELECT	@pRetornoOP as N'@pRetornoOP',
                @pRetornoMSG as N'@pRetornoMSG' 
        """
    
    try:
        cursor.execute(sql)
        retorno = cursor.fetchall()

        if retorno[0][0] == 1:
            return 1
        
        else:
            return retorno[0][1]
        
    except Exception as e:
        print(e)
        return e
    

def processar_pasta_xml(caminho_base, conn):
    inicio_total = datetime.now()

    # Verificar se o caminho_base existe
    if not os.path.isdir(caminho_base):
        print("Caminho base não encontrado.")
        return

    # Iterar sobre as subpastas dentro de caminho_base
    for subpasta in os.listdir(caminho_base):
        inicio_pasta = datetime.now()
        caminho_subpasta = os.path.join(caminho_base, subpasta)
        numero_funcao = subpasta.split('.')[0]

        # Processar arquivos XML dentro da subpasta
        for arquivo in os.listdir(caminho_subpasta):
            if arquivo.endswith(".xml"):
                caminho_arquivo = os.path.join(caminho_subpasta, arquivo)
                with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                    conteudo_xml = file.read()

                    # Chamar funções baseado no número da função
                    if numero_funcao == "1010":
                        resultado = extrair_1010(conteudo_xml)
                        inserir_1010(resultado, conn)
                    
                    elif numero_funcao == "2299":
                        resultado = extrair_2299(conteudo_xml)
                        inserir_2299(resultado, conn)
                    elif numero_funcao == "5001":
                        resultado = extrair_5001(conteudo_xml)
                        inserir_5001(resultado, conn)
                    elif numero_funcao == "5011":
                        resultado = extrair_5011(conteudo_xml)
                        inserir_5011(resultado, conn)

                    elif numero_funcao == "1200":
                        resultado = extrair_1200(conteudo_xml)
                        if resultado == None:
                            print(caminho_arquivo)                        
                        inserir_1200(resultado, conn)
        

        fim_pasta = datetime.now()
        tempo_pasta = fim_pasta - inicio_pasta
        print(f"Tempo de processamento da pasta {subpasta}: {tempo_pasta}")


    fim_total = datetime.now()                        
    tempo_total = fim_total - inicio_total
    print(f"Tempo total de processamento: {tempo_total}")
    

if __name__ == "__main__":
    start_time = time.time()
    #conn = conectar()
    print("Conectado!")
    pasta =fr"C:\Users\frocha\Documents\ePrevCredito\Server\blueprints\extract\functions\pasta1"

    # arquivos = [arquivo for arquivo in os.listdir(pasta) ]
    # print(arquivos)

    # for arquivo in arquivos:
    #     print(os.path.join(pasta, arquivo))
    #     content = open(os.path.join(pasta, arquivo)).read()        
    #     dados = extrair_1200(content)
    #     resp = inserir_1200(dados)
    #     print(resp)        

    caminho_base = rf'C:\Users\frocha\Documents\ePrevCredito\Server\blueprints\extract\functions\output'
    processar_pasta_xml(caminho_base)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tempo total de execução: {total_time} segundos")
