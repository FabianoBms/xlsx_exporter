import pandas as pd
import matplotlib.pyplot as plt

def processar_linhas(arquivo):
    with open(arquivo, 'r') as f:
        # Ignorar cabeçalho
        next(f)
        
        for linha in f:
            # Dividir a linha em campos usando a vírgula como separador
            campos = linha.strip().split(',')
            
            # Converter o campo "ValorRubrica" para float substituindo a vírgula por ponto
            valor_rubrica = float(campos[1].replace('.', '').replace(',', '.'))
            
            yield campos[0], valor_rubrica

# Criar DataFrame a partir do gerador
df = pd.DataFrame(processar_linhas("output_260120240945_1200.csv"), columns=['Competencia', 'ValorRubrica'])

# Agrupar os dados por competência e calcular a soma dos valores
soma_por_competencia = df.groupby('Competencia')['ValorRubrica'].sum()

# Plotar o gráfico
plt.figure(figsize=(10, 6))
soma_por_competencia.plot(kind='bar')  # Você pode escolher o tipo de gráfico adequado (por exemplo, 'bar', 'line')
plt.title('Soma dos Valores por Competência')
plt.xlabel('Competência')
plt.ylabel('Soma dos Valores')
plt.grid(True)
plt.xticks(rotation=45)  # Rotacionar os rótulos do eixo x para facilitar a leitura
plt.tight_layout()
plt.show()
