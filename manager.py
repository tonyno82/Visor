import tkinter as tk
import queue
import threading
from watchdog.observers import Observer
from pathlib import Path
from PIL import ImageTk, Image
import ctypes

import config.gestionModeloQ2, config.gestionModeloCX482
import config.config

from funciones.gestionLog import generadorDeLogs

from screens.frameEventos import FrameEventos
from screens.frameReconexion import FrameReconexion
from screens.frameTrazabilidad import FrameTraza
from screens.frameVisor import FrameVisor
from screens.frameTitulo import frameTitulo

from funciones.gestionADS import ConexPLC
from funciones.gestionCicloVisor import CicloVisor

from funciones.observador import MyEventHandler
from funciones.gestionRegistros import GestionRegistros
from funciones.gestionBBDD import GestionBBDD
from funciones.gestionArchivos import GestionArchivos
import pdb


class Manager(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configuracion de Icono para Barra de Tareas de windows
        myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.option_add('*tearOff', False)

        # Configuraciones
        self.gestionModelo = config.gestionModeloQ2
        self.config = config.config

        self.title(self.gestionModelo.nombreVisor)
        if self.config.pCompleta:
            self.state("zoomed")
        self.geometry(self.config.tPantalla)
        self.resizable(False, False)
        # self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        # self.iconbitmap('img\Imagotipo-Rodama_ico.ico')
        self.img_logo = ImageTk.PhotoImage(Image.open(r'img\Imagotipo-Rodama_ico.ico'))
        self.iconphoto(True, self.img_logo)
        # Contador Fotos
        self.contador = 0

        # Logger
        self.colaLogger = queue.Queue(1000)
        self.logger = generadorDeLogs(self.config.ubicacionLog, self.config.nombreLog, self.colaLogger)
 
        # Observador
        self.colaObservador = queue.Queue(1000)
        self.observadorOK = False
        self.configuracionObservador()

        # Gestion BBDD
        self.conexBBDD = False
        self.gestionBBDD = GestionBBDD(self)
        self.gestionBBDD.comprobarConexBBDD()

        # Gestion Archivos
        self.gestionArchivos = GestionArchivos(self)
        self.gestionArchivos.moverArchivosEnOrigen()

        # Conexion PLC
        self.conexionPLC = ConexPLC(self)
        self.hiloPLC = threading.Thread(target=self.conexionPLC.iniciarScan)
        self.hiloPLC.start()

        # Frames
        self.frames = {}
        self._iniciarFrames()
        
        # Ciclo Visor
        self.gestionRegistros = GestionRegistros(self)
        self.cicloVisor = CicloVisor(self)
        self.hilocicloVisor = threading.Thread(target=self.cicloVisor.inicioCicloVisor)
        self.hilocicloVisor.start()


        # Protocolo para cerrar ventana
        self.protocol("WM_DELETE_WINDOW", self._on_closing)


        
    def _on_closing(self):
        self.logger.debug('Cerrando Aplicacion')
        if self.hiloPLC.isAlive():
            self.logger.debug('Hilo ScanPLC encontrado, cerrando hilo')
            self.conexionPLC.stopHilo = True
            self.hiloPLC.join()
            self.logger.debug('Hilo ScanPLC cerrado')
        if self.hilocicloVisor.isAlive():
            self.logger.debug('Hilo cicloVisor encontrado, cerrando hilo')
            self.cicloVisor.stopHilo = True
            self.hilocicloVisor.join()
            self.logger.debug('Hilo cicloVisor cerrado')
        if self.observador:
            if self.observador.is_alive():
                self.logger.debug('Hilo Observador encontrado, cerrando hilo')
                self.observador.stop()
                self.observador.join()
                self.logger.debug('Hilo Observador cerrado')
        self.destroy()

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def configuracionObservador(self):
        self.logger.debug('Iniciando Observador')
        # Por si no se crea la variables no tener error al cerrar el programa
        self.observador = None
        if Path(self.config.cObservador).exists():
            try:
                self.observador = Observer()
                self.observador.schedule(MyEventHandler(self.colaObservador, self.logger), self.config.cObservador, recursive=True)
                self.observador.start()
            except Exception as e:
                self.logger.error('Error al iniciar Observador')
                self.logger.error(e)
            else:
                self.logger.info('Observador iniciado con exito')
                self.observadorOK = True
        else:
            self.logger.error('Error al iniciar Observador')
            self.logger.error(f'Carpeta {self.config.cObservador} no encontrada')
            self.observadorOK = False

    def _iniciarFrames(self):
        self.frameEventos = FrameEventos
        self.frameReconexion = FrameReconexion
        self.frameTrazabilidad = FrameTraza
        self.frameVisor = FrameVisor
        self.titulo = frameTitulo(self)

        for F in (FrameEventos, FrameReconexion, FrameTraza, FrameVisor):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(column=0, row=2, columnspan=3, sticky=tk.NSEW)
            # frame.grid_propagate(False)
        self.show_frame(FrameEventos)