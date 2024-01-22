import tkinter as tk
from tkinter import filedialog
from functools import partial
import pandas as pd

def combinar_planilhas(diretorio_saida, arquivos_selecionados):
    # Criar um DataFrame vazio para armazenar os dados
    dados_combinados = pd.DataFrame()

    # Iterar sobre os arquivos Excel e concatenar os DataFrames
    for arquivo_excel in arquivos_selecionados:
        df = pd.read_excel(arquivo_excel)
        dados_combinados = pd.concat([dados_combinados, df], ignore_index=True)

    # Salvar o DataFrame combinado em um novo arquivo Excel
    dados_combinados.to_excel(diretorio_saida, index=False)
    resultado_label.config(text="Arquivo combinado salvo em {}".format(diretorio_saida))

def selecionar_diretorio_saida():
    diretorio_saida = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])
    diretorio_saida_entry.delete(0, tk.END)
    diretorio_saida_entry.insert(0, diretorio_saida)

def selecionar_arquivos():
    arquivos_selecionados = filedialog.askdirectory()
    arquivos_selecionados_entry.delete(0, tk.END)
    arquivos_selecionados_entry.insert(0, arquivos_selecionados)

# Criar a janela principal
janela = tk.Tk()
janela.title("Combinar Planilhas Excel")

# Widgets
diretorio_saida_label = tk.Label(janela, text="Diretório de Saída:")
diretorio_saida_entry = tk.Entry(janela, width=40)
selecionar_saida_button = tk.Button(janela, text="Selecionar", command=selecionar_diretorio_saida)

arquivos_selecionados_label = tk.Label(janela, text="Arquivos Selecionados:")
arquivos_selecionados_entry = tk.Entry(janela, width=40)
selecionar_arquivos_button = tk.Button(janela, text="Selecionar", command=selecionar_arquivos)

combinar_button = tk.Button(janela, text="Combinar Planilhas", command=partial(combinar_planilhas, diretorio_saida_entry.get(), arquivos_selecionados_entry.get()))

resultado_label = tk.Label(janela, text="")

# Layout
diretorio_saida_label.grid(row=0, column=0, pady=5, padx=5, sticky=tk.E)
diretorio_saida_entry.grid(row=0, column=1, pady=5, padx=5)
selecionar_saida_button.grid(row=0, column=2, pady=5, padx=5)

arquivos_selecionados_label.grid(row=1, column=0, pady=5, padx=5, sticky=tk.E)
arquivos_selecionados_entry.grid(row=1, column=1, pady=5, padx=5)
selecionar_arquivos_button.grid(row=1, column=2, pady=5, padx=5)

combinar_button.grid(row=2, column=1, pady=10)
resultado_label.grid(row=3, column=0, columnspan=3, pady=10)

# Iniciar a janela
janela.mainloop()
