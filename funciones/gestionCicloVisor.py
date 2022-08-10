import tkinter as tk
from PIL import ImageTk, Image
import queue
import time


class CicloVisor():
    def __init__(self, manager):
        self.manager = manager
        self.logger = self.manager.logger
        self.conexionPLC = self.manager.conexionPLC
        self.colaObservador = self.manager.colaObservador
        self.stopHilo = False
        self.comprobarObservador = False
        self.compruebaConexionPLC = False
        self.gestionRegistros = self.manager.gestionRegistros
        self.gestionArchivos = self.manager.gestionArchivos

        # Configuraciones
        self.gestionModelo = manager.gestionModelo
        self.config = manager.config
        self.listaEtapasReseteo = self.gestionModelo.listaEtapasReseteo     
        self.listaArchivosCreados = []
        self.listaArchivosAMover = []


    
    def inicioCicloVisor(self):
        self.frameVisor = self.manager.frames[self.manager.frameVisor]
        self._comprobarCondicionyRun()

    def _comenzarScan(self):
        while self.conexionPLC.conexOk:
            if self.stopHilo:
                return
            
            ### TODO : Crear mosaico de Fotos 
            if not self.manager.conexionPLC.valoresPLC['Marcha_Inspeccion'] \
                and self.manager.conexionPLC.valoresPLC['Num_Inspecciones_Interno'] == self.manager.conexionPLC.valoresPLC['Num_Inspecciones_Obj'] \
                and self.manager.conexionPLC.valoresPLC['Num_Inspecciones_Interno'] != 0 \
                and self.manager.conexionPLC.valoresPLC['cicloOk'] == False: 
                    self.gestionRegistros.gestionRegistro()
            if self.conexionPLC.valoresPLC['resetVisor']:
                archivosAMover = self.listaArchivosAMover
                self._resetCiclo()
                self.logger.debug('Moviendo archivo :')
                self.logger.debug(archivosAMover)
                self.gestionArchivos.moverListaArchivosInpeccionados(archivosAMover)

            if self.manager.conexionPLC.valoresPLC['Marcha_Inspeccion'] \
                and self.conexionPLC.valoresPLC['Pausa'] \
                and self.manager.contador != 0:
                    self.logger.warning('#### OJO #### Ha empezado la inspeccion y no hemos reiniciado el contador')
                    self.logger.warning('Reiniciando label y moviendo archivos ...')
                    archivosAMover = self.listaArchivosAMover
                    self._resetCiclo()
                    self.gestionArchivos.moverListaArchivosInpeccionados(archivosAMover)
            try:
                self.nuevoArchivo = self.colaObservador.get_nowait()
            except queue.Empty:
                time.sleep(0.5)
            else:
                self._insertarArchivoAMover()
                self._insertarEnPantalla()
                time.sleep(0.5)
        # Si se sale del bucle, comprobamos de nuevo y arrancamos.
        self._comprobarCondicionyRun()


    def _insertarEnPantalla(self):
        if not self.conexionPLC.valoresPLC['Pausa'] and self.nuevoArchivo.suffix in [".bmp", ".jpeg"] and self.manager.contador < self.conexionPLC.valoresPLC['Num_Inspecciones_Obj']:
            self.manager.contador += 1
            self.listaArchivosCreados.append(self.nuevoArchivo)
            self.logger.debug(f"Añadiendo {self.nuevoArchivo} a pantalla. -> NºLed : {self.manager.contador}/{self.conexionPLC.valoresPLC['Num_Inspecciones_Obj']}")
            self.frameVisor.crearLabel(self.nuevoArchivo)

    def _insertarArchivoAMover(self):
        if self.nuevoArchivo.is_dir():
            self.logger.debug(f'Carpeta {self.nuevoArchivo} creada !')
            return
        elif self.nuevoArchivo.is_file():
            if self.nuevoArchivo in self.listaArchivosAMover:
                self.logger.warning(f'OJO {self.nuevoArchivo.name} REPETIDO')
                return
            elif self.conexionPLC.valoresPLC['Pausa']:
                self.logger.warning(f'{self.nuevoArchivo.name} creado con el observador Desconectado')
                self.listaArchivosAMover.append(self.nuevoArchivo)
            elif self.manager.contador >= self.conexionPLC.valoresPLC['Num_Inspecciones_Obj']:
                self.logger.warning(f'{self.nuevoArchivo.name} creado con el contador de fotos a {self.manager.contador}')
            else:
                self.logger.debug(f'{self.nuevoArchivo} añadido a listaArchivosAMover')
                self.listaArchivosAMover.append(self.nuevoArchivo)


    def _comprobarCondicionyRun(self):
        if self.stopHilo:
            return
        self._compruebaConexionPLC()
        self.logger.debug('CicloVisor Iniciado')
        self._comenzarScan()


    def _compruebaConexionPLC(self):
        while not self.conexionPLC.conexOk:
            if self.stopHilo:
                return
            # self.logger.error('Error inicioCicloVisor(), Conexion con PLC está OFF')
            time.sleep(5)
        
    def _resetCiclo(self):
        self.logger.debug('Borrando Fotos')
        self.frameVisor.borrarImagenes()
        self.logger.debug('Reseteando contador')
        self.manager.contador = 0
        self.logger.debug('Poniendo Reset a 0')
        self.conexionPLC.valoresPLC['resetVisor'] = False
        self.logger.debug('Borrando listado de archivos')
        self.listaArchivosCreados = []
        self.listaArchivosAMover = []
        self.logger.debug('Reseteando Ciclo OK')
        self.conexionPLC.valoresPLC['cicloOk'] = False