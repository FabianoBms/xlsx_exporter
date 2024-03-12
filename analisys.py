import os
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# Verifica se o caminho do arquivo existe antes de ler o arquivo
path = r"C:\Users\frocha\Desktop\XLSX_EXPORTER"
if not os.path.exists(path):
    raise FileNotFoundError(f'O caminho especificado "{path}" não existe.')

# Lê o arquivo Excel
dataframe = pd.read_excel(os.path.join(path, "output_190220240938_1200.xlsx"), engine="openpyxl")

# Mapear os formatos possíveis
formatos = ['%d-%m-%Y', '%m-%Y', '%Y-%m']

try:
    dataframe['ValorRubrica'] = dataframe['ValorRubrica'].replace(',', '.', regex=True).astype('float64')
    # dataframe['NumRecibo'] = dataframe['NumRecibo'].astype('string')
    # dataframe['CPF'] = dataframe['CPF'].astype('string')
    # dataframe['IdentificadorEvento'] = dataframe['IdentificadorEvento'].astype('string')
    # dataframe['IdentificadorDemonstrativoPagamento'] = dataframe['IdentificadorDemonstrativoPagamento'].astype('string')
    # dataframe['descricao'] = dataframe['descricao'].astype('category')
    # dataframe['CodRubrica'] = dataframe['CodRubrica'].astype('category')
    # dataframe['CodLotacao'] = dataframe['CodLotacao'].astype('category')
    # dataframe['InscricaoEstabelecimento'] = dataframe['InscricaoEstabelecimento'].astype('category')
    # dataframe['GrauAgenteNocivo'] = dataframe['GrauAgenteNocivo'].astype('category')
    # dataframe['DataGeracaoEvento'] = dataframe['DataGeracaoEvento'].astype('string')
    # dataframe['Competencia'] = dataframe['Competencia'].astype('string')
    # dataframe['Competencia'] = pd.DatetimeIndex(dataframe['Competencia'])
    # dataframe['DataGeracaoEvento'] = pd.to_datetime(dataframe['DataGeracaoEvento'], format='mixed', errors='coerce')
    # dataframe['Competencia'] = dataframe['Competencia'].dt.strftime('%m-%Y')
    # dataframe['DataGeracaoEvento'] = dataframe['DataGeracaoEvento'].dt.strftime('%d-%m-%Y')

except Exception as e:
    print("erro", e)


dataframe.to_excel(os.path.join(path, "output_190220240938_1200.xlsx"), index=False)

total_valor_rub = dataframe['ValorRubrica'].sum()


valor_formatado = locale.currency(total_valor_rub)
print("Total da coluna ValorRubrica:", valor_formatado)

# Imprime as últimas linhas do DataFrame
print(dataframe.head())
dataframe.info()


# Conta os valores na primeira coluna do DataFrame
# print("count", dataframe[dataframe.columns[0]].count())

# Remove linhas com valores não numéricos na coluna 'ValorRubrica'
# dataframe = dataframe[pd.to_numeric(dataframe['ValorRubrica'], errors='coerce').notnull()]


# Verifica se houve algum valor não numérico que foi convertido para NaN (Not a Number)
# if dataframe['ValorRubrica'].isnull().any():
#     print("A coluna 'ValorRubrica' contém valores não numéricos.")

# Agora você pode somar os valores da coluna 'ValorRubrica'
# ValorRubrica_sum = dataframe['ValorRubrica'].sum()

# print(type(ValorRubrica_sum))

# print("Soma da coluna ValorRubrica:", ValorRubrica_sum)

# Lista das somas de 

# Cria uma nova coluna no DataFrame para armazenar os valores modificados
#dataframe['nova_evtTabRubrica'] = dataframe['evtTabRubrica'].apply(lambda x: "508629" if "508629" in x else x)

# Imprime as linhas onde o valor foi substituído
#print(dataframe[dataframe['nova_evtTabRubrica'] == "508629"])

# Salva o DataFrame modificado em um novo arquivo Excel
# output_path = os.path.join(path, "output_1010.xlsx")
# dataframe.to_excel(output_path, index=False)
# print(f'DataFrame modificado salvo em {output_path}.')


