import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk

class frameTitulo(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = parent

        self.frameCentral = tk.Frame(parent)
        self.frameCentral.grid(column=1, row=0)

        self.logo = ImageTk.PhotoImage(Image.open(Path("img\Marca-Rodama_.jpg")))
        self.logotipo = ttk.Label(parent, image=self.logo)
        self.logotipo.grid(column=0, row=0, sticky=tk.W)

        self.version = ttk.Label(self.frameCentral,text='Visor V1.0')
        self.version.pack(side=tk.TOP)

        self.logotipo2 = ttk.Label(parent,image=self.logo)
        self.logotipo2.grid(column=2, row=0, sticky=tk.E)     

        self.frameMenu = tk.Frame(parent)
        self.frameMenu.grid(column=0, row=1, columnspan=3)   



        self._crearBotones()   
    
    def _crearBotones(self):
        self.botonEventos = ttk.Button(self.frameCentral, text='Eventos', 
        command=lambda: self.controller.show_frame(self.controller.frameEventos))
        self.botonEventos.pack(side=tk.LEFT)
        
        self.botonTrazabilidad = ttk.Button(self.frameCentral, text='Trazabilidad',
        command=lambda: self.controller.show_frame(self.controller.frameTrazabilidad))
        self.botonTrazabilidad.pack(side=tk.LEFT)

        self.botonVisor = ttk.Button(self.frameCentral, text='Visor',
        command=lambda: self.controller.show_frame(self.controller.frameVisor))
        self.botonVisor.pack(side=tk.LEFT)  

        self.botonImprimirTamano = ttk.Button(self.frameCentral, text='Tamaño',
        command=self.controller.verGeometriaLabel)
        self.botonImprimirTamano.pack(side=tk.LEFT)  


