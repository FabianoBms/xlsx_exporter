import base64
import customtkinter


from PIL import Image, ImageTk
from io import BytesIO

from imagens_base_64 import image_data
from load import ImageLabel
from threading import Thread

import shutil
from datetime import datetime

import pandas as pd

class MyApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.dataframes = []
        self.title("BMS Projetos - Xlsx Exporter")
        self.geometry("650x550")    
        #self.resizable(False, False)            
       
        self.output_folder = []
    
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        #image = Image.open()

        #background_image = customtkinter.Imagecustomtkinter.PhotoImage(image)
 
        # Carregar a imagem do logotipo
        #logo_image = Image.open(r"Logo_BMS.png")  
        logo_image = image.resize((100, 100))  
        #self.logo_image = customtkinter.Imagecustomtkinter.PhotoImage(logo_image)
        
        self.create_ui()

    def create_ui(self): 
        # Adicionar a imagem do logotipo ao rótulo
        self.logo_label = customtkinter.CTkLabel(self, 
                                                #  image=self.logo_image, 
                                                )
        self.logo_label.pack(pady=10, padx=20, side=customtkinter.TOP) 

        # Criar um frame centralizado
        self.frame = customtkinter.CTkFrame(self, width=650, height=440)
        self.frame.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)
   
        # Criar os componentes dentro do frame
        #self.label = customtkinter.CTkLabel(self.frame, text="BMS Projetos", bg='#ebe5e4')
        self.logo = customtkinter.CTkLabel(self.frame, text="Xlsx Exporter",  font=("Arial", 20))
        self.upload_button = customtkinter.CTkButton(self.frame, text="Upload dos Arquivos ZIP", command=lambda: self.run_in_thread(self.extract), width=20)
        
        # Cinco botões de extração (inicialmente invisíveis)
        self.button_1010 = customtkinter.CTkButton(self.frame, text="Extrair 1010", width=15, command=lambda: self.run_in_thread(self.extract_number,1010), state=customtkinter.DISABLED)
        self.button_1200 = customtkinter.CTkButton(self.frame, text="Extrair 1200", width=15, command=lambda: self.run_in_thread(self.extract_number,1200), state=customtkinter.DISABLED)
        self.button_2299 = customtkinter.CTkButton(self.frame, text="Extrair 2299", width=15, command=lambda: self.run_in_thread(self.extract_number,2299), state=customtkinter.DISABLED)
        self.button_5001 = customtkinter.CTkButton(self.frame, text="Extrair 5001", width=15, command=lambda: self.run_in_thread(self.extract_number,5001), state=customtkinter.DISABLED)
        self.button_5011 = customtkinter.CTkButton(self.frame, text="Extrair 5011", width=15, command=lambda: self.run_in_thread(self.extract_number,5011), state=customtkinter.DISABLED)
        self.button_start = customtkinter.CTkButton(self.frame, text="Iniciar exportação", width=15, command=lambda: self.run_in_thread(self.start_export()), 
                                    #   state=customtkinter.DISABLED
                                      )
       
        self.label_info = customtkinter.CTkLabel(self.frame, text="1 - Suba o arquivo zip contendo os XML's✔️\n2 - Clique no botão correspondente ao tipo de evento para fazer a extração✔️\n3 - Clique no botão 'Iniciar exportação'✔️\n4 - Aguarde a exportação ser concluída.") 
 
        self.pb = customtkinter.CTkProgressBar(self.frame, mode="indeterminate")
        
        # Posicionar os componentes usando o grid geometry
        #self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=15, sticky="news")
        self.logo.grid(row=0, column=1, columnspan=3, padx=180, sticky="news")
        self.upload_button.grid(row=1, column=0, columnspan=4, padx=10, pady=15)

        self.button_1010.grid(row=2, column=1, pady=15, padx=(10))
        self.button_1200.grid(row=2, column=3, pady=15, padx=(0,10))
        self.button_2299.grid(row=3, column=1, pady=15, padx=(10,0))
        self.button_5001.grid(row=3, column=3, pady=15, padx=(0,10)) 
        self.button_5011.grid(row=4, column=1, pady=15, padx=(10,0))
        self.button_start.grid(row=4, column=3, pady=15, padx=(0,10))
        self.label_info.grid(row=6, column=0, columnspan=4, padx=10, pady=15)

# Instanciar e iniciar o aplicativo

if __name__ == "__main__":


    app = MyApp()
    try:        
        app.mainloop()
    except KeyboardInterrupt as e:
        print('bye!')
        app.salvar_logs(f"Bye! {e}")
        app.destroy()