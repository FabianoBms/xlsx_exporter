import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CsvPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Plotter")
        self.root.geometry("800x600")

        self.plot_types = ["Scatter", "Line", "Bar"]
        self.plot_type_var = tk.StringVar(value=self.plot_types[0])
        plot_menu = tk.OptionMenu(self.root, self.plot_type_var, *self.plot_types, command=self.plot_esocial)
        plot_menu.pack(padx=10, pady=10)
        load_button = tk.Button(self.root, text="Load CSV", command=self.load_csv)
        load_button.pack(padx=10, pady=10)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

        self.widgets = self.canvas.get_tk_widget()
        self.widgets.pack(padx=10, pady=10)

        self.df = None

    def load_csv(self):
        try:
            file_path = filedialog.askopenfilename()
            if file_path:
                self.df = pd.read_csv(file_path)
                print(self.df.head())
                self.df['ValorRubrica'] = self.df['ValorRubrica'].str.replace(',', '.').astype(float)
                self.plot()
        except Exception as e:
            print("Erro ao carregar o arquivo CSV:", e)

    def plot(self):
        print('plot')
        if self.df is not None:
            plot_type = self.plot_type_var.get()
            x = self.df.columns[0]
            y = self.df.columns[1]

            self.ax.clear()

            if plot_type == "Scatter":
                self.ax.scatter(self.df[x], self.df[y], label=f"{y} vs {x}")
            elif plot_type == "Line":
                self.ax.plot(self.df[x], self.df[y], label=f"{y} vs {x}")
            elif plot_type == "Bar":
                self.ax.bar(self.df[x], self.df[y], label=f"{y} vs {x}")

            self.ax.set_xlabel(x)
            self.ax.set_ylabel(y)
            self.ax.legend()
            self.canvas.draw()

    def plot_esocial(self):
        if self.df is not None:
            plot_type = self.plot_type_var.get()  
            # Agrupar os dados por competência e calcular a soma dos valores
            soma_por_competencia = self.df.groupby('Competencia')['ValorRubrica'].sum()

            # Plotar o gráfico
            plt.figure(figsize=(10, 6))
            soma_por_competencia.plot(kind=plot_type)  # Você pode escolher o tipo de gráfico adequado (por exemplo, 'bar', 'line')
            plt.title('Soma dos Valores por Competência')
            plt.xlabel('Competência')
            plt.ylabel('Soma dos Valores')
            plt.grid(True)
            plt.xticks(rotation=45)  # Rotacionar os rótulos do eixo x para facilitar a leitura
            plt.tight_layout()
            plt.show() 


if __name__ == "__main__":
    root = tk.Tk()
    app = CsvPlotter(root)
    root.mainloop()
