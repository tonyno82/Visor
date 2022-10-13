import queue
import tkinter as tk
from tkinter import ttk

class FrameEventos(tk.Frame):
    def __init__(self, manager):
        super().__init__(manager)
        self.logger = manager.logger
        self.manager = manager
        self.colaMensajes = self.manager.colaLogger
        # Color original background='#f50a41', 
        self.configure(height=980, width=1280)
        self.infoPLC = self.manager.conexionPLC.valoresPLC

        self.framePantallaLog = tk.Frame(self)
        self.framePantallaLog.configure(width=1280, height=750)
        self.framePantallaLog.columnconfigure(0, weight=1)
        self.framePantallaLog.rowconfigure(0, weight=1)
        self.framePantallaLog.grid(column=0, row=1,columnspan=2)
        self.framePantallaLog.grid_propagate(False)

        self._iniciarVariablesImportantes()
        self.pantallaLog = tk.Text(self.framePantallaLog, state='disable', width=150, height=45, wrap=None)
        self.pantallaLog.grid(column=0, row=0, sticky=tk.EW)
        # Bucles de actualizacion
        self._actualizarPantallaLog()
        self._actualizarVariables()


    def _escribirPantalla(self, msg):
        numlineas = int(self.pantallaLog.index('end - 1 line').split('.')[0])
        self.pantallaLog['state'] = 'normal'
        if numlineas == 45:
            self.pantallaLog.delete(1.0, 2.0)
        if self.pantallaLog.index('end-1c') != '1.0':
            self.pantallaLog.insert('end', '\n')
        self.pantallaLog.insert('end', msg)
        self.pantallaLog['state'] = 'disable'

    def _iniciarVariablesImportantes(self):
        separadorVariables = tk.LabelFrame(self, text='Variables')
        separadorVariables.grid(column=0, row=0, sticky=tk.W)
        self.dicStringVar = {}
        dicLabel = {}
        contador = 0
        for key, value in self.infoPLC.items():
            self.dicStringVar[key] = tk.StringVar()
            # self.valoresPLC['Datos_Registro']
            if key == 'Datos_Registro':
                value = str(value)[:50]
                self.dicStringVar[key].set(value)
            else:
                self.dicStringVar[key].set(value)
            dicLabel[key] = tk.Label(separadorVariables, text=key).grid(column=0, row=contador)
            dicLabel[key] = tk.Label(separadorVariables, textvariable=self.dicStringVar[key]).grid(column=1, row=contador)
            contador += 1
    
    def _actualizarVariables(self):
        for key, value in self.infoPLC.items():
            if key == 'Datos_Registro':
                value = str(value)[:50]
                self.dicStringVar[key].set(value)
            else:
                self.dicStringVar[key].set(value)
        self.manager.after(500, self._actualizarVariables)


    def _actualizarPantallaLog(self):
        while True:
            try:
                mensaje = self.colaMensajes.get_nowait()
            except queue.Empty:
                break
            else:
                self._escribirPantalla(mensaje.getMessage())
        self.after(500, self._actualizarPantallaLog)
