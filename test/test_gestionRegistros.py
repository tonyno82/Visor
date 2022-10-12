import logging
from pathlib import Path
from funciones.gestionRegistros import GestionRegistros
from funciones.gestionBBDD import GestionBBDD
from config import gestionModeloQ2, gestionModeloCX482
from config import config
import logging
import pdb
import shutil
import os
import time

class ManagerQ2:
    def __init__(self):
        class _cicloVisor:
            def __init__(self):
                self.listaArchivosCreados = []
        class _conexionPLC:
            def __init__(self):
                self.valoresPLC = {
                    'Etapa_Principal' : 0, 
                    'Marcha_Inspeccion' : 0,
                    'Datos_Registro' : 0,
                    'Num_Inspecciones_Obj' : 4,
                    'tiempoScanMedido' : 0,
                    'Num_Inspecciones_Interno' : 4,
                    'Pausa' : True,
                    'resetVisor' : False,
                    'cicloOk' : False,
                    'cicloInterrumpido' : False
                    }
        self.logger = logging.getLogger('My_Logger')
        self.config = config
        self.contador = 4
        self.gestionModelo = gestionModeloQ2
        self.conexBBDD = False


        self.cicloVisor = _cicloVisor()
        self.conexionPLC = _conexionPLC()
        self.gestionBBDD = GestionBBDD(self)

class ManagerCX482:
    def __init__(self):
        self.logger = logging.getLogger('My_Logger')
        self.gestionModelo = gestionModeloCX482
        self.config = config
        self.contador = 4
        self.conexBBDD = False
        
        class _cicloVisor:
            def __init__(self):
                self.listaArchivosCreados = []
        class _conexionPLC:
            def __init__(self):
                self.valoresPLC = {
                    'Etapa_Principal' : 0, 
                    'Marcha_Inspeccion' : 0,
                    'Datos_Registro' : 0,
                    'Num_Inspecciones_Obj' : 8,
                    'tiempoScanMedido' : 0,
                    'Num_Inspecciones_Interno' : 8,
                    'Pausa' : True,
                    'resetVisor' : False,
                    'cicloOk' : False,
                    'cicloInterrumpido' : False
                    }

        self.cicloVisor = _cicloVisor()
        self.conexionPLC = _conexionPLC()
        self.gestionBBDD = GestionBBDD(self)

"""AUN NO DESARROLLADA"""