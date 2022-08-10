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

        # Variables
        self.imagen = {}
        self.label = {}
    
    def crearLabel(self, foto):
        """recibe una foto y inserta laber en la pantalla, actualmente en formato 2x2 y 3x3 para imagenes de 640x480"""
        nLed = self.manager.contador
        self.nLedObjetivo = self.manager.conexionPLC.valoresPLC['Num_Inspecciones_Obj']
        if self.nLedObjetivo <= 4:
            self._configura_columnas()
            # La fotos del sensor de keyence viene a 640x480
            self._reducirFoto(foto)
            if nLed <= 2:
                self.logger.debug(f'if nLed <= 2 -> Contador {nLed}')
                self.label[nLed].grid(column=nLed-1, row=0)
            else:
                self.logger.debug(f'else: -> Contador {nLed}')
                self.label[nLed].grid(column=nLed-3, row=1)
        elif self.nLedObjetivo <= 8:
            self._configura_columnas()
            # La fotos del sensor de keyence viene a 640x480
            self._reducirFoto(foto)
            if nLed < 4:
                self.label[nLed].grid(column=nLed-1, row=0)
            elif nLed < 7:
                self.label[nLed].grid(column=nLed-4, row=1)
            elif nLed >= 7:
                self.label[nLed].grid(column=nLed-7, row=2)

    def _configura_columnas(self):
        """Configura el grid para que cada foto quede en el centro de su espacio segun su son 4 u 8 fotos"""
        if self.nLedObjetivo <= 4:
            for n in range(0, 2):
                self.columnconfigure(n, weight=1)
                self.rowconfigure(n, weight=1)
        elif self.nLedObjetivo <= 8:
            for n in range(0, 3):
                self.columnconfigure(n, weight=1)
                self.rowconfigure(n, weight=1)           


    def _reducirFoto(self, foto):
        """Reduce las fotos a la altura maxima del frame, lleva una correcion que es 25 o 35 que es la altura del texto inferior"""
        self.logger.debug(f'Reduciendo foto -> Tamaño label fotos -> {self.winfo_height()}')
        self.logger.debug(f'Numero de led objetivo -> {self.nLedObjetivo}')
        if self.nLedObjetivo <= 4:
            alturaMaximaFoto = int(round(((self.winfo_height() // 2)/(480+25))*640, 0))
        elif self.nLedObjetivo <= 8:
            alturaMaximaFoto = int(round(((self.winfo_height() // 3)/(480+35))*640, 0))
        alturaMaximaFoto = alturaMaximaFoto,alturaMaximaFoto
        nLed = self.manager.contador
        self.logger.debug(f'Nled ({nLed}) creando label reduciendo fotos')
        self.imagen[nLed] = Image.open(foto)
        self.logger.debug(f'reduciendo imagen a maximo = {alturaMaximaFoto}')
        self.imagen[nLed].thumbnail(alturaMaximaFoto, Image.ANTIALIAS)
        self.logger.debug(f'Medida Final = {self.imagen[nLed].size}')
        self.imagen[nLed] = ImageTk.PhotoImage(self.imagen[nLed])
        self.label[nLed] = tk.Label(self, text = foto.stem, image=self.imagen[nLed], relief="raised", compound='top')
    
    def borrarImagenes(self):
        """Borra todo el grid de fotos"""
        for a in self.label:
            self.label[a].grid_forget()
        self.imagen = {}
        self.label = {}


        





