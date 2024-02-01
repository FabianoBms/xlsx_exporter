import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, Menu
import threading
import time
import os
import zipfile
import base64
from io import BytesIO
import time
from PIL import Image, ImageTk
from _1010_to_excel import processar_xml as processar_xml_1010
from _1200_to_excel import processar_xml as processar_xml_1200
from _2299_to_excel import processar_xml as processar_xml_2299
from _5011_to_excel import processar_xml as processar_xml_5011
from _5001_to_excel import processar_xml as processar_xml_5001

from tkinter import messagebox
from imagens_base_64 import image_data

from threading import Thread

import shutil
from datetime import datetime
import pandas as pd

try:
    from setup import get_version 
except:
    pass    


class Relatorios:
    def __init__(self, *args):
        self.data_evento = datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
        self.nome_empresa = ""
        self.CNPJ_empresa=""

        self.tempo_1010 = int(0)
        self.tempo_1200 = int(0)
        self.tempo_2299 = int(0)
        self.tempo_5011 = int(0)
        self.tempo_5001 = int(0)
        self.tempo_total = int(0)

        self.tempo_extract = int(0)
        self.tempo_export = int(0)
        
        self.quantidade_arquivos_1010=int(0)
        self.quantidade_arquivos_1200=int(0)
        self.quantidade_arquivos_2299=int(0)
        self.quantidade_arquivos_5011=int(0)
        self.quantidade_arquivos_5001=int(0)
        self.quantidade_arquivos_total=int(0)

    def get_tempo_total(self):
        return self.tempo_total
    
    def tempo_parcial(self, number_xml):
        if number_xml == 1010:
            return self.tempo_1010
        elif number_xml == 1200:
            return self.tempo_1200
        elif number_xml == 2299:
            return self.tempo_2299
        elif number_xml == 5011:
            return self.tempo_5011
        elif number_xml == 5001:
            return self.tempo_5001
        elif number_xml == "total":
            return self.get_tempo_total()
    def add_tempo(self, number_xml, tempo):
        if number_xml == 1010:
            self.tempo_1010 = tempo
        elif number_xml == 1200:
            self.tempo_1200 = tempo
        elif number_xml == 2299:
            self.tempo_2299 = tempo
        elif number_xml == 5011:
            self.tempo_5011 = tempo
        elif number_xml == 5001:
            self.tempo_5001 = tempo
             

class MyApp(tk.Tk):

    def __init__(self, root):
        self.relatorios = Relatorios()
        self.root = root
        self.dataframes = []
        self.root.title("BMS Projetos - Xlsx Exporter")
        self.root.geometry("750x650")
        self.root.minsize(750, 650)
        # self.root.resizable(False, False)
        self.root.configure(bg="#001F3F")
        self.exportados = []
        self.output_folder = []
        self.output_path = os.getcwd() + "/output"
        favicon = open("logo.png", "rb")
        self.root.iconphoto(False, tk.PhotoImage(file="logo.png"))

        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        logo_image = image.resize((200, 160))
        self.logo_image = ImageTk.PhotoImage(logo_image)

        self.create_ui()
    
    def handle_key_event(self, event):
        tecla_pressionada = event.keysym 
        ctrl = event.state & 4
        shift = event.state & 1
        alt = event.state & 8

        if tecla_pressionada == "m" and ctrl:
            print(f'{tecla_pressionada}, {ctrl}')
            
    def create_ui(self):

        self.root.bind('<Key>', self.handle_key_event)
        # Adicionar a imagem do logotipo ao rótulo
        self.logo_label = tk.Label(
            self.root,
            image=self.logo_image,
            bg="#001F3F",
        )
        self.logo_label.pack(pady=10, padx=20, side=tk.TOP)

        # Criar um frame centralizado
        self.frame = tk.Frame(self.root, width=650, height=440, bg="#ebe5e4")
        self.frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.frame.bind('<Double-1>',self.clear_label)
   

        # Criar os componentes dentro do frame
        # self.label = tk.Label(self.frame, text="BMS Projetos", bg='#ebe5e4')
        self.logo = tk.Label(
            self.frame, text="Xlsx Exporter", bg="#ebe5e4", font=("Arial", 20)
        )

        self.upload_button = tk.Button(
            self.frame,
            text="Upload dos Arquivos ZIP",
            command=lambda: self.run_in_thread(self.extract),
            width=20,
        )

        # Cinco botões de extração (inicialmente invisíveis)
        self.button_1010 = tk.Button(
            self.frame,
            text="Extrair 1010",
            width=15,
            command=lambda: self.run_in_thread(self.extract_number, 1010),
            state=tk.DISABLED,
        )
        self.button_1200 = tk.Button(
            self.frame,
            text="Extrair 1200",
            width=15,
            command=lambda: self.run_in_thread(self.extract_number, 1200),
            state=tk.DISABLED,
        )
        self.button_2299 = tk.Button(
            self.frame,
            text="Extrair 2299",
            width=15,
            command=lambda: self.run_in_thread(self.extract_number, 2299),
            state=tk.DISABLED,
        )
        self.button_5001 = tk.Button(
            self.frame,
            text="Extrair 5001",
            width=15,
            command=lambda: self.run_in_thread(self.extract_number, 5001),
            state=tk.DISABLED,
        )
        self.button_5011 = tk.Button(
            self.frame,
            text="Extrair 5011",
            width=15,
            command=lambda: self.run_in_thread(self.extract_number, 5011),
            state=tk.DISABLED,
        )
        self.button_start = tk.Button(
            self.frame,
            text="Iniciar exportação",
            width=15,
            command=lambda: self.run_in_thread(self.start_export),
            state=tk.DISABLED
        )

        self.label_info = tk.Label(
            self.frame,
            text="1 - Suba o arquivo zip contendo os XML's✔️\n2 - Clique no botão correspondente ao tipo de evento para fazer a extração✔️\n3 - Clique no botão 'Iniciar exportação'✔️\n4 - Aguarde a exportação ser concluída.",
            bg="#ebe5e4", font=("Arial", 8) )

        self.pb = ttk.Progressbar(self.frame, mode="indeterminate")

        # Posicionar os componentes usando o grid geometry
        # self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=15, sticky="news")
        self.logo.grid(row=0, column=1, columnspan=3, padx=180,pady=20, sticky="news")
        self.upload_button.grid(row=1, column=0, columnspan=4, padx=10, pady=15)

        self.button_1010.grid(row=2, column=1, pady=15, padx=(10))
        self.button_1200.grid(row=2, column=3, pady=15, padx=(0, 10))
        self.button_2299.grid(row=3, column=1, pady=15, padx=(10, 0))
        self.button_5001.grid(row=3, column=3, pady=15, padx=(0, 10))
        self.button_5011.grid(row=4, column=1, pady=15, padx=(10, 0))
        self.button_start.grid(row=4, column=3, pady=15, padx=(0, 10))
        self.label_info.grid(row=6, column=0, columnspan=4, padx=10, pady=15)

        # create a menubar
        menubar = Menu(self.root)
        root.config(menu=menubar)

        # create the file_menu
        file_menu = Menu(menubar, tearoff=0)


        file_menu.add_command( label="Importar zip...", command=lambda: self.run_in_thread(self.extract),  )
        file_menu.add_separator()
        # file_menu.add_command( label="Definir pasta output",command=lambda: self.run_in_thread(self.definir_pasta_output), )
        file_menu.add_command( label="Abrir pasta output",command=lambda: self.run_in_thread(self.abrir_pasta_output), )
        file_menu.add_separator()
        file_menu.add_command(label="Apagar arquivos gerados",command=lambda: self.run_in_thread(self.apagar_arquivos_gerados), )
        file_menu.add_command( label="Apagar output",command=lambda: self.run_in_thread(self.apagar_output),)
        
        file_menu.add_separator()
       
        file_menu.add_command(label="Mover exportados", command=lambda:self.run_in_thread(self.mover_exportados))
        file_menu.add_separator()

        # add Exit menu item
        file_menu.add_command(label="Sair", command=root.destroy)

        # add the File menu to the menubar
        menubar.add_cascade(label="Menu", menu=file_menu)

        # create the Help menu
        help_menu = Menu(menubar, tearoff=0)

        # help_menu.add_command(label='Welcome')
        help_menu.add_command(label="Abrir logs...", command=self.abrir_logs)
        help_menu.add_command(label="Limpar logs...", command=self.limpar_logs)

        help_menu.add_separator()
        help_menu.add_command(label="Sobre...", command=self.sobre)

        

        # add the Help menu to the menubar
        menubar.add_cascade(label="Ajuda", menu=help_menu)

        is_output = self.check_output()
        # print(is_output[0])
        if is_output[0] == True:
            answer = messagebox.askyesno("Output", f'Existem {len(is_output[1])} {"pasta" if len(is_output[1]) == 1 else "pastas"} em output: \n {is_output[1]}\nDeseja manter estes arquivos??',
            )

            self.pb.grid(row=5, column=0, columnspan=4, pady=15, padx=10)
            self.pb.start()

            if answer == False:
                self.run_in_thread(self.apagar_output())


            elif answer == True:
                self.output_folder = is_output[1]
                self.enable_buttons()
                self.button_start["state"] = tk.NORMAL
                quebra = "\n"
                pasta = '--> '.join(str(self.output_folder[x]+quebra) for x in range(len(self.output_folder)))
                self.label_info["text"] = f"Pastas recuperadas: {pasta}"
            
            self.pb.stop()
            self.pb.grid_forget()
    
    def clear_label(self, event):

        self.label_info["text"] = ""
    
    def abrir_logs(self):
        # Abrir o arquivo de logs.txt
        os.startfile("logs.txt")


    def mover_exportados(self):
        self.label_info["text"] = " "
        
        if len(self.exportados) == 0:
            self.check_output()
        # Abrir caixa de diálogo para selecionar o diretório de destino
        destino = filedialog.askdirectory(title="Selecione o diretório de destino")

        if destino:
            # Mover cada arquivo exportado para o diretório de destino
            for arquivo in self.exportados[:]:  # Utilizamos [:] para criar uma cópia da lista
                try:
                    nome_arquivo = os.path.basename(arquivo)
                    # Construir o caminho de destino
                    destino_arquivo = os.path.join(destino, nome_arquivo)
                    shutil.move(arquivo, destino_arquivo)
                    print(f"Arquivo {nome_arquivo} movido para {destino}")
                    self.salvar_logs(f"Arquivo {nome_arquivo} movido para {destino}")
                    self.label_info["text"] = self.label_info["text"]+ '\n' + f"Arquivo {nome_arquivo} movido para {destino}"

                    self.exportados.remove(arquivo)
                except Exception as e:
                    print(f"Erro ao mover arquivo {nome_arquivo}: {e}")
                    self.salvar_logs(f"Erro ao mover arquivo {nome_arquivo}: {e}")
        self.pb.stop()
        self.pb.grid_forget() 
                  
    def limpar_logs(self):
        with open("logs.txt", "w", encoding="utf-8") as file:
            file.write("")
        messagebox.showinfo("Logs", "Logs limpos com sucesso", parent=self.root)    
    
    def sobre(self):
        try:
            versao = get_version()
        except:
            versao = "nao identificado"
        messagebox.showinfo(
            "BMS Consultoria Tributária",
            f"XLSX Exporter\n\nVersão: {versao} \n Conversor de eventos para excel\n Copyright (C) 2024 BMS",
            parent=self.root,
            icon="info",
            type="ok",            
        )
    
    def definir_pasta_output(self):
        self.output_path = filedialog.askdirectory(
            title="Selecione a pasta de output", parent=self.root

        )
    
    def abrir_pasta_output(self):
        print(self.output_path)
        if os.path.exists(self.output_path):
            os.startfile(self.output_path)
        else:
            os.makedirs(self.output_path)

    def check_output(self):
        print('checking output...')

        if os.path.exists(self.output_path):
            output_folders = []

            for folder in os.listdir(self.output_path):
                print(folder)

                if not folder.endswith('.csv'):
                  print('aqui--> ', folder)
                  output_folders.append(f"{self.output_path}/{folder}")
                elif folder.endswith('.csv'):
                    self.exportados.append(f"{self.output_path}/{folder}")
            print('exportados: ', self.exportados)


            if len(output_folders) == 0:
                return False, []   
                     
            return True, output_folders
        
        else:
            return False, []

    def enable_buttons(self):
        # Habilitar os botões após o upload dos arquivos
        self.button_1010["state"] = tk.NORMAL
        self.button_1200["state"] = tk.NORMAL
        self.button_2299["state"] = tk.NORMAL
        self.button_5001["state"] = tk.NORMAL
        self.button_5011["state"] = tk.NORMAL
        #self.button_start["state"] = tk.NORMAL

    def disable_buttons(self):
        # Habilitar os botões após o upload dos arquivos
        self.button_1010["state"] = tk.DISABLED
        self.button_1200["state"] = tk.DISABLED
        self.button_2299["state"] = tk.DISABLED
        self.button_5001["state"] = tk.DISABLED
        self.button_5011["state"] = tk.DISABLED
        self.button_start["state"] = tk.DISABLED

    def salvar_logs(self, logs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("logs.txt", "a", encoding="utf-8") as file:
            file.write(timestamp + " - " + logs + "\n")

    def extract(self):
 
        try:
            # Função para o botão "Upload dos Arquivos ZIP"            
            file_paths = filedialog.askopenfilenames( title="Selecione um arquivo ZIP", filetypes=[("Arquivos ZIP", "*.zip")])
            desired_files = ["1010.xml", "1200.xml", "2299.xml", "5001.xml", "5011.xml"]
            if len(file_paths) == 0:
                self.label_info["text"] = "Nenhum arquivo selecionado"
                self.pb.forget()
                return
            self.pb.grid(
                row=5,
                column=0,
                columnspan=4,
                pady=15,
            )
                
            self.pb.start()
            for file_path in file_paths:
                self.label_info["text"] = f"Arquivo selecionado: \n{file_path}\nAguarde..."
                # Criar uma pasta com o nome da empresa
                output_folder = os.path.join( os.path.join("output", file_path.split("/")[-1].split(".")[0]))
                os.makedirs(output_folder, exist_ok=True)

                self.output_folder.append(output_folder)
                # print(f"Output_folder: {output_folder}")
                # Extrair apenas os arquivos desejados
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    for file_info in zip_ref.infolist():
                        for desired_file in desired_files:
                            if file_info.filename.endswith(desired_file):
                                # Garantir que o diretório exista antes de extrair o arquivo
                                target_path = os.path.join(
                                    output_folder, os.path.splitext(desired_file)[0]
                                )
                                os.makedirs(target_path, exist_ok=True)
                                zip_ref.extract(file_info, target_path)

        except Exception as e:
            print(f"Erro ao extrair os arquivos: {e}")
            self.label_info["text"] = f"Erro ao extrair os arquivos:\n {e}"
            self.salvar_logs(f"Erro ao extrair os arquivos:\n {e}")
            self.pb.stop()
            self.pb.grid_forget()
            return

        self.enable_buttons()
        self.label_info["text"] = "Extração concluída!\nVocê pode exportar os arquivos!"
        self.button_start["state"] = tk.NORMAL
        self.pb.stop()
        self.pb.grid_forget()

    def run_in_thread(self, func, *args):
        try:
            t = threading.Thread(target=func, args=args)
            t.start()
        except Exception as e:
            print(f"Erro ao iniciar a thread: {e}")
            self.label_info["text"] = f"Erro ao iniciar a thread:\n {e}"
            self.salvar_logs(f"Erro ao iniciar a thread:\n {e}")
            return

    def extract_number(self, number):
        tempo_init = time.time()
        self.pb.grid(
            row=5,
            column=0,
            columnspan=4,
            pady=15,
        )
        self.disable_buttons()

        self.pb.start()
        total = 0
        tempo = 0
        for _folder in self.output_folder:
            try:
                if os.path.isdir(_folder):
                    if f"_{number}.xlsx" in os.listdir(os.path.join(_folder)):                
                        print(f"Arquivo {number}.xlsx encontrado na pasta 'output'")
                        self.label_info["text"] = f"Arquivo {number}.xlsx já existe na pasta 'output'"
                

                    else:
                        try:
                            iter_number = (
                                arquivo_xml
                                for arquivo_xml in os.listdir(
                                    os.path.join(_folder, str(number))
                                )
                                if arquivo_xml.endswith(f"{str(number)}.xml")
                            )
                            print(f"Extraindo para o xml {number} o arquivo {iter_number}")
                            dfs = []
                            cont = 0

                            for val in iter_number:
                                cont += 1
                                # print(f"Extraindo para o número {number} o arquivo {val}")
                                self.label_info[
                                    "text"
                                ] = f"Extraindo para o xml {number} o arquivo \n{val}"
                                caminho = os.path.join(_folder, str(number), val)
                                # df = threading.Thread(target=self.dummy_function, args=(caminho,)).start()
                                if number == 1200:
                                    df = processar_xml_1200(caminho)
                                elif number == 1010:
                                    df = processar_xml_1010(caminho)
                                elif number == 2299:
                                    df = processar_xml_2299(caminho)
                                elif number == 5001:
                                    df = processar_xml_5001(caminho)
                                elif number == 5011:
                                    df = processar_xml_5011(caminho)

                                dfs.append(df)

                            # Concatenar todos os DataFrames em um único DataFrame
                            df_final = pd.concat(dfs, ignore_index=True)
                            self.dataframes.append(df_final)

                            df_final.to_excel(
                                os.path.join(_folder, f"_{number}.xlsx"), index=False
                            )
                            
                            total = total + cont
                            # Calcula o tempo de execução em minutos
                            tempo_minutos = (time.time() - tempo_init) / 60

                            # Calcula os segundos restantes
                            tempo_segundos = (time.time() - tempo_init) % 60

                            # Formata a mensagem de tempo de execução
                            tempo = f"Tempo de execução: {int(tempo_minutos)} minutos e {tempo_segundos:.2f} segundos"
                            self.relatorios.add_tempo(number, tempo)

                            self.label_info["text"] = f"Extração concluída para o xml {number}.\n Quantidade de arquivos processados: {cont if cont > 0 else len (os.listdir(os.path.join(_folder, str(number))))}\n {tempo}"
                        
                        except FileNotFoundError as e:
                            self.label_info["text"] = f"Extração falhou para o xml {number}.\n {e}"
                            print(f"Extração falhou para o xml {number}.\n {e}")
                            self.salvar_logs(f"Extração falhou para o xml {number}.\n {e}")
                            self.pb.stop()
                            self.pb.grid_forget()
                            # self.enable_buttons_buttons()
                            continue
            except Exception as e:
                self.label_info['text'] = str(e)
                self.pb.stop()
                self.pb.grid_forget()
                # self.enable_buttons_buttons()
                return

        if total > 0 :                
            self.label_info["text"] = f"Extração concluída para o xml {number}.\n Quantidade de arquivos processados: {cont if cont > 0 else len (os.listdir(os.path.join(_folder, str(number))))}\n {tempo}"
        
        self.salvar_logs(f"Extração concluída para os arquivos {number}. Total de arquivos processados: {total} {tempo}")
        self.enable_buttons()
        self.button_start["state"] = tk.NORMAL
        self.pb.stop()
        self.pb.grid_forget()

        # print("Extração concluída")

    def apagar_arquivos_gerados(self):
        self.label_info["text"] = "Deletando arquivos gerados..."
        output_folders = self.output_folder

        if len(output_folders) == 0:
            self.label_info["text"] = "Não ha arquivos a serem deletados!"

        for pasta in output_folders:

            if os.path.isdir(pasta):
                arquivos = [arquivo for arquivo in os.listdir(pasta) if arquivo.endswith(".xlsx")]
                print(arquivos)

                if len(arquivos) == 0:
                    self.label_info["text"] = "Não ha arquivos a serem deletados!"
                    return
                
                for arquivo in arquivos:
                    print(f"Deletando o arquivo {arquivo}")
                    self.label_info["text"] = self.label_info["text"] + '\n' + f"Deletando o arquivo:\n{arquivo}"
                    
                    os.remove(os.path.join(pasta, arquivo))
                    self.salvar_logs(f"Arquivo {arquivo} deletado!")
        
    def apagar_output(self):
        try:
            is_output = self.check_output()
            print( f'Deletando pastas em output: {len(is_output[1])} {"pasta" if len(is_output[1]) == 1 else "pastas"}'  )
            self.label_info["text" ] = f'Deletando pastas em output: {len(is_output[1])} {"pasta" if len(is_output[1]) == 1 else "pastas"}'
            
            for pasta in is_output[1]:
                self.run_in_thread(shutil.rmtree(pasta))
                print(f"Pasta {pasta} deletada")

            self.label_info["text"] = f"Pasta {pasta} deletada"
            self.disable_buttons()
        except UnboundLocalError as e:
            print(f"Erro: {e.with_traceback}")
            self.label_info["text"] = "Não ha arquivos a serem deletados!"

    def start_export(self):
        tempo_export = time.time()
        self.pb.grid(
            row=5,
            column=0,
            columnspan=4,
            pady=15,
        )

        self.pb.start()
        tempo_init = time.time()
        doc_lists = {"1010": [], "1200": [], "2299": [], "5001": [], "5011": []}
        tempo_final = float(00.00)
        is_output = self.check_output()
        if is_output[0] == False:
            return
        else:
            self.output_folder = is_output[1]
            print(self.output_folder)

        for pasta in self.output_folder:
            if os.path.isdir(pasta):                
                arquivos = [arquivo for arquivo in os.listdir(pasta) ]
                for arquivo in arquivos:
                    try:
                        doc_number = None
                        if arquivo.endswith(doc_number := "1010.xlsx"):
                            doc_lists["1010"].append(os.path.join(pasta, arquivo))
                        elif arquivo.endswith(doc_number := "1200.xlsx"):
                            doc_lists["1200"].append(os.path.join(pasta, arquivo))
                        elif arquivo.endswith(doc_number := "2299.xlsx"):
                            doc_lists["2299"].append(os.path.join(pasta, arquivo))
                        elif arquivo.endswith(doc_number := "5001.xlsx"):
                            doc_lists["5001"].append(os.path.join(pasta, arquivo))
                        elif arquivo.endswith(doc_number := "5011.xlsx"):
                            doc_lists["5011"].append(os.path.join(pasta, arquivo))
                    except Exception as e:
                        print(f"Erro ao processar arquivo {arquivo}: {e}")
                        self.salvar_logs(f"Erro ao processar arquivo {arquivo}: {e}")

        for doc_type, file_list in doc_lists.items():
            # print( doc_lists.items())
            self.run_in_thread(self.juntar_xmls(doc_type, file_list, pasta))
            tempo_etapa = time.time() - tempo_init
            tempo_etapa_horas = tempo_etapa / 3600
            tempo_etapa_minutos = tempo_etapa / 60
            tempo_etapa_segundos = tempo_etapa % 60
            tempo_etapa_format = f"{int(tempo_etapa_minutos)} minutos : {int(tempo_etapa_segundos)} segundos"
            
            print( f"Exportação concluída para o xml {doc_type}, quantidade de arquivos processados: {len(file_list)}")
            self.salvar_logs(f"Extração concluída para o xml {doc_type}, quantidade de arquivos processados: {len(file_list)}. Tempo de execução: {tempo_etapa}")
            self.label_info["text"] = f"Extração concluída para o xml {doc_type}, \nTempo de execução: {tempo_etapa_format}"
            tempo_final = tempo_final+tempo_etapa

        tempo_final_format = f"{int(tempo_final / 60)} minutos : {int(tempo_final % 60)} segundos"    # print(tempo_etapa)
        print(f"Tempo total de execução: \n{tempo_final_format}")
        self.label_info["text"] = f"Exportação concluída para o xml {doc_type}, \n Tempo total de execução:\n {tempo_final_format}"
        self.relatorios.tempo_export = tempo_final

        self.pb.stop()
        self.pb.grid_forget()

    def juntar_xmls(self, doc_number, file_list, destino):
        
        destino = destino.split("/")[1].replace(" ", "_")
        if len(file_list) == 0:
            return
        try:
            df_final = pd.concat(
                [pd.read_excel(arquivo) for arquivo in file_list], ignore_index=True
            )
            file = f"output_{datetime.now().strftime('%d%m%Y%H%M')}_{doc_number}.csv"
            df_final.to_csv(os.path.join( "output",file), index=False)
            print(f"Arquivo {doc_number} salvo em {destino}")
            self.salvar_logs(f"Arquivo {doc_number} salvo em {destino}")

        except FileNotFoundError as e:
            print(f"Erro FileNotFoundError: {e}")

        except Exception as e:
            print(f"Erro Exception: {e}")

        finally:
            print(f"Extração concluída para o xml {doc_number}.")
            self.label_info["text"] = f"Extração concluída para o xml {doc_number}."



# Iniciar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    try:
        app.root.mainloop()
    except KeyboardInterrupt as e:
        print("bye!")
        app.root.destroy()
    except Exception as e:
        app.salvar_logs(f"Bye! {e}")
        app.root.destroy()
