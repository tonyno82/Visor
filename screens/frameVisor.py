import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import queue



class FrameVisor(tk.Frame):
    def __init__(self, manager):
        super().__init__(manager)
        # Manager
        self.manager = manager
        self.logger = manager.logger
        self.contador = manager.contador

        # Configuraciones
        self.gestionModelo = manager.gestionModelo
        self.config = manager.config
        self.listaEtapasReseteo = self.gestionModelo.listaEtapasReseteo
        self.configure(background='#121212', height=980, width=1280)

        # Frames Info
        self.frameInfo = tk.Frame(self)
        self.frameInfo.configure(width=1280)
        self.frameInfo.grid(row=0, column=0)
        # self.frameInfo.grid_propagate(False)
        self._agregarInfo()


        # Frames Fotos
        self.frameFotos = ttk.Frame(self)
        self.frameFotos.configure(height= 954,width=1280)
        self.frameFotos.grid(row=1, column=0)
        self.frameFotos.columnconfigure(0, weight=1)
        self.frameFotos.columnconfigure(1, weight=1)
        self.frameFotos.rowconfigure(0, weight=1)
        self.frameFotos.rowconfigure(1, weight=1)
        self.frameFotos.grid_propagate(False)

        # Variables
        self.imagen = {}
        self.label = {}
    

    
    def crearLabel(self, foto):
        """recibe una foto y inserta laber en la pantalla, actualmente en formato 2x2 y 3x3 para imagenes de 640x480"""
        logger = self.logger
        nLed = self.manager.contador
        nLedObjetivo = self.manager.conexionPLC.valoresPLC['Num_Inspecciones_Obj']
        if nLedObjetivo <= 4:
            self._reducirFoto(foto, 608, 456)
            if nLed <= 2:
                self.logger.debug(f'if nLed <= 2 -> Contador {nLed}')
                self.label[nLed].grid(column=nLed-1, row=0)
            else:
                self.logger.debug(f'else: -> Contador {nLed}')
                self.label[nLed].grid(column=nLed-3, row=1)
        elif nLedObjetivo <= 8:
            self._reducirFoto(foto, 420, 315)
            if nLed < 4:
                self.label[nLed].grid(column=nLed-1, row=0)
            elif nLed < 7:
                self.label[nLed].grid(column=nLed-4, row=1)
            elif nLed >= 7:
                self.label[nLed].grid(column=nLed-7, row=2)
    
    def _verGeometriaLabel(self):
        self.logger.debug(f'Tamaño label botones -> {self.frameInfo.winfo_geometry()}')

    def _agregarInfo(self):
        botton1 = ttk.Button(self.frameInfo, text="Boton1", command=self._verGeometriaLabel).grid(row=0, column=0)
        botton2 = ttk.Button(self.frameInfo, text="Boton2").grid(row=0, column=1)
        botton3 = ttk.Button(self.frameInfo, text="Boton3").grid(row=0, column=2)

    
    def _reducirFoto(self, foto, ancho, alto):
        logger = self.logger
        nLed = self.manager.contador
        self.logger.debug(f'Nled ({nLed}) creando label reduciendo fotos')
        self.imagen[nLed] = Image.open(foto)
        logger.debug(f'tamaño de la imagen {self.imagen[nLed].size}, reduciendo a {ancho}x{alto}')
        self.imagen[nLed] = self.imagen[nLed].resize((ancho, alto))
        self.imagen[nLed] = ImageTk.PhotoImage(self.imagen[nLed])
        self.label[nLed] = tk.Label(self.frameFotos, text = foto.stem, image=self.imagen[nLed], relief="raised", compound='top')
    
    def borrarImagenes(self):
        for a in self.label:
            self.label[a].grid_forget()
        self.imagen = {}
        self.label = {}


        





