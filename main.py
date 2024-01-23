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


class MyApp(tk.Tk):
    def __init__(self, root):
        self.root = root
        self.dataframes = []
        self.root.title("BMS Projetos - Xlsx Exporter")
        self.root.geometry("750x650")
        self.root.minsize(750, 650)
        self.root.resizable(False, False)
        self.root.configure(bg="#001F3F")
        self.output_folder = []
        favicon = open("logo.png", "rb")
        self.root.iconphoto(False, tk.PhotoImage(file="logo.png"))

        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))

        background_image = ImageTk.PhotoImage(image)

        # Carregar a imagem do logotipo
        # logo_image = Image.open(r"Logo_BMS.png")
        logo_image = image.resize((200, 160))
        self.logo_image = ImageTk.PhotoImage(logo_image)

        self.create_ui()

    def create_ui(self):
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
            bg="#ebe5e4",
        )

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

        # add menu items to the File menu

        file_menu.add_command(
            label="Importar zip...", command=lambda: self.run_in_thread(self.extract)
        )

        file_menu.add_command(
            label="Abrir pasta output",
            command=lambda: self.run_in_thread(self.abrir_pasta_output),
        )

        file_menu.add_command(
            label="Apagar output",
            command=lambda: self.run_in_thread(self.apagar_arquivos_gerados),
        )
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
            answer = messagebox.askyesno(
                "Output",
                f'Existem {len(is_output[1])} {"pasta" if len(is_output[1]) == 1 else "pastas"} em output: \n {is_output[1]}\nDeseja manter estes arquivos??',
            )

            self.pb.grid(row=5, column=0, columnspan=4, pady=15, padx=10)
            self.pb.start()

            if answer == False:
                print(
                    f'Deletando pastas em output: {len(is_output[1])} {"pasta" if len(is_output[1]) == 1 else "pastas"}'
                )
                self.label_info[
                    "text"
                ] = f'Deletando pastas em output: {len(is_output[1])} {"pasta" if len(is_output[1]) == 1 else "pastas"}'
                for pasta in is_output[1]:
                    self.run_in_thread(shutil.rmtree(pasta))
                    print(f"pasta {pasta} deletada")
                    self.label_info["text"] = f"pasta {pasta} deletada"

            elif answer == True:
                self.output_folder = is_output[1]
                self.enable_buttons()

            self.pb.stop()
            self.pb.grid_forget()
    def abrir_logs(self):
        # Abrir o arquivo de logs.txt
        os.startfile("logs.txt")

    def limpar_logs(self):
        with open("logs.txt", "w", encoding="utf-8") as file:
            file.write("")
        messagebox.showinfo("Logs", "Logs limpos com sucesso", parent=self.root)    
    def sobre(self):
        messagebox.showinfo(
            "Sobre",
            "XLSX Exporter\n\nVersão: 1.0",
            parent=self.root,
            icon="info",
            type="ok",
            
        )
    def abrir_pasta_output(self):
        if os.path.exists("output"):
            os.startfile("output")
        else:
            os.makedirs("output")

    def check_output(self):
        if os.path.exists("output"):
            output_folders = []
            for folder in os.listdir("output"):
                output_folders.append(f"output/{folder}")
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

    def select_bt(self):
        print(self)

    def extract(self):
        self.pb.grid(
            row=5,
            column=0,
            columnspan=4,
            pady=15,
        )
        self.pb.start()

        try:
            # Função para o botão "Upload dos Arquivos ZIP"
            file_paths = filedialog.askopenfilenames( title="Selecione um arquivo ZIP", filetypes=[("Arquivos ZIP", "*.zip")])
            desired_files = ["1010.xml", "1200.xml", "2299.xml", "5001.xml", "5011.xml"]

            for file_path in file_paths:
                self.label_info["text"] = f"Arquivo selecionado: \n{file_path}\nAguarde..."
                # Criar uma pasta com o nome da empresa
                output_folder = os.path.join(
                    os.path.join("output", file_path.split("/")[-1].split(".")[0])
                )
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
            self.label_info["text"] = f"Erro ao extrair os arquivos: {e}"
            self.salvar_logs(f"Erro ao extrair os arquivos: {e}")
            self.pb.stop()
            self.pb.grid_forget()
            return

        self.enable_buttons()
        self.label_info["text"] = "Extração concluída!\nVocê pode exportar os arquivos!"
        self.pb.stop()
        self.pb.grid_forget()

    def run_in_thread(self, func, *args):
        try:
            t = threading.Thread(target=func, args=args)
            t.start()
        except Exception as e:
            print(f"Erro ao iniciar a thread: {e}")
            self.label_info["text"] = f"Erro ao iniciar a thread: {e}"
            self.salvar_logs(f"Erro ao iniciar a thread: {e}")
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
        for _folder in self.output_folder:
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
                    self.label_info[
                        "text"
                    ] = f"Extração concluída para o xml {number}.\n Quantidade de arquivos processados: {cont}"
                    print(
                        f"Extração concluída para o xml {number}.\n Quantidade de arquivos processados: {cont}"
                    )
                    total = total + cont
                    tempo_minutos = (time.time() - tempo_init) / 60
                    print(f"Tempo de execução: {tempo_minutos:.2f} minutos")
                except FileNotFoundError as e:
                    self.label_info[
                        "text"
                    ] = f"Extração falhou para o xml {number}.\n {e}"
                    print(f"Extração falhou para o xml {number}.\n {e}")
                    self.salvar_logs(f"Extração falhou para o xml {number}.\n {e}")
                    pass

        self.label_info[
            "text"
        ] = f"Extração concluída.\n Total de arquivos processados: {total}"
        print(f"Extração concluída.\n Total de arquivos processados: {total}")
        self.salvar_logs(
            f"Extração concluída para os arquivos {number}. Total de arquivos processados: {total}"
        )
        self.enable_buttons()
        self.button_start["state"] = tk.NORMAL
        self.pb.stop()
        self.pb.grid_forget()

        # print("Extração concluída")

    def apagar_arquivos_gerados(self):
        output_folders = self.output_folder
        for pasta in output_folders:
            arquivos = [
                arquivo for arquivo in os.listdir(pasta) if arquivo.endswith(".xlsx")
            ]
            for arquivo in arquivos:
                print(f"Deletandoo o arquivo {arquivo}")
                self.label_info["text"] = f"Deletando o arquivo {arquivo}"
                self.salvar_logs(f"Arquivo {arquivo} deletado!")
                os.remove(os.path.join(pasta, arquivo))
                self.label_info["text"] =""



    def start_export(self):
        self.pb.grid(
            row=5,
            column=0,
            columnspan=4,
            pady=15,
        )

        self.pb.start()
        tempo_init = time.time()
        doc_lists = {"1010": [], "1200": [], "2299": [], "5001": [], "5011": []}
        is_output = self.check_output()
        if is_output[0] == False:
            return
        else:
            self.output_folder = is_output[1]
            print(self.output_folder)

        for pasta in self.output_folder:
            arquivos = [arquivo for arquivo in os.listdir(pasta)]
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
            print(
                f"Extração concluída para o xml {doc_type}, quantidade de arquivos processados: {len(file_list)}"
            )
            self.salvar_logs(
                f"Extração concluída para o xml {doc_type},\n quantidade de arquivos processados: \n{len(file_list)}. Tempo de execução: {tempo_etapa}"
            )
            self.label_info["text"] = f"Extração concluída para o xml {doc_type}, \nTempo de execução: {tempo_etapa}"

            # print(tempo_etapa)
        print(f"Tempo total de execução: {tempo_etapa}")
        self.label_info["text"] = f"Extração concluída! Tempo total de execução: {tempo_etapa}"

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
            df_final.to_csv(f"resultados_{destino}_{doc_number}.csv", index=False)
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
        app.salvar_logs(f"Bye! {e}")
        app.root.destroy()
