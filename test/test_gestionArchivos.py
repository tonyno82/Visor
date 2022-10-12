import logging
from pathlib import Path
from unittest.mock import patch
from funciones.gestionRegistros import GestionRegistros
from funciones.gestionBBDD import GestionBBDD
from funciones.gestionArchivos import GestionArchivos
from config import gestionModeloQ2, gestionModeloCX482
from config import config
import logging
import pdb
import tempfile
import time
import os
import shutil

from test.test_gestionBBDD import ManagerCX482

class ManagerQ2:
    def __init__(self):
        class Config:
            def __init__(self):
                self.cObservador = "pruebasObservador"
                self.cDestino = "pruebasObservador"

        self.logger = logging.getLogger('My_Logger')
        self.gestionModelo = gestionModeloQ2
        self.config = Config()
        self.contador = 4
        self.conexBBDD = False

        class _cicloVisor:
            def __init__(self):
                self.listaArchivosCreados = []

        self.cicloVisor = _cicloVisor()
        self.gestionBBDD = GestionBBDD(self)
        self.gestionArchivos = GestionArchivos(self)

class ManagerCX482:
    def __init__(self):
        class Config:
            def __init__(self):
                self.cObservador = "pruebasObservador"
                self.cDestino = "pruebasObservador"

        self.logger = logging.getLogger('My_Logger')
        self.gestionModelo = gestionModeloCX482
        self.config = Config()
        self.contador = 8
        self.conexBBDD = False

        class _cicloVisor:
            def __init__(self):
                self.listaArchivosCreados = []

        self.cicloVisor = _cicloVisor()
        self.gestionBBDD = GestionBBDD(self)
        self.gestionArchivos = GestionArchivos(self)

def test_moverArchivosEnOrigen_Q2():
    manager = ManagerQ2()
    logger = manager.logger
    gestionArchivos = manager.gestionArchivos
    manager.config.cObservador = r'prueba_Fotos\Origen'
    manager.config.cDestino = r'prueba_Fotos\Destino'
    for carpeta in [manager.config.cObservador, manager.config.cDestino]:
        if os.path.exists(carpeta):
            logger.debug(f'Borrando {carpeta}')
            shutil.rmtree(carpeta) 
            if os.path.exists(carpeta):
                logger.error(f'ERROR Borrando {carpeta}')
            else:
                logger.debug(f'Borrado con exito !! {carpeta}')
        os.makedirs(carpeta)
    os.remove('bbdd_q2.db') if os.path.exists('bbdd_q2.db') else ...
    archivosCopiar = Path(r'C:\Users\tonyno\Desktop\Proyectos Python GitHub\Visor\Fotos_Prueba').glob('*')
    for archivo in archivosCopiar:
        shutil.copy(archivo, manager.config.cObservador)
    gestionArchivos.moverArchivosEnOrigen()
    assert os.path.exists(r'prueba_Fotos\Destino\2022-03-25\003\OK\00003_003_OK_25032022_082112.jpeg')
    
    logger.debug('-------------- Con BBDD OK -----------------')
    manager.conexBBDD = True
    for carpeta in [manager.config.cObservador, manager.config.cDestino]:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta) 
        os.makedirs(carpeta)
    shutil.copy(r"test\Muestra_bbdd_q2.db", "bbdd_q2.db")
    archivosCopiar = Path(r'C:\Users\tonyno\Desktop\Proyectos Python GitHub\Visor\Fotos_Prueba').glob('*')
    for archivo in archivosCopiar:
        shutil.copy(archivo, manager.config.cObservador)
    gestionArchivos.moverArchivosEnOrigen()
    assert os.path.exists(r'prueba_Fotos\Destino\2022-03-25\003\OK\00003_003_OK_25032022_082112.jpeg')
    assert os.path.exists(r'prueba_Fotos\Destino\2022-06-02\003\NG\Fotos_FOK\00111_003_NG_02062022_065639.iv2p')
    os.remove('bbdd_q2.db') if os.path.exists('bbdd_q2.db') else ...
    for carpeta in [manager.config.cObservador, manager.config.cDestino]:
        shutil.rmtree(carpeta) if os.path.exists(carpeta) else ...

    

def test_moverArchivosEnOrigen_CX482():
    manager = ManagerCX482()
    logger = manager.logger
    gestionArchivos = manager.gestionArchivos
    manager.config.cObservador = r'prueba_Fotos\Origen'
    manager.config.cDestino = r'prueba_Fotos\Destino'
    for carpeta in [manager.config.cObservador, manager.config.cDestino]:
        if os.path.exists(carpeta):
            logger.debug(f'Borrando {carpeta}')
            shutil.rmtree(carpeta) 
            if os.path.exists(carpeta):
                logger.error(f'ERROR Borrando {carpeta}')
            else:
                logger.debug(f'Borrado con exito !! {carpeta}')
        os.makedirs(carpeta)
    os.remove('bbdd_CX482.db') if os.path.exists('bbdd_CX482.db') else ...
    archivosCopiar = Path(r'C:\Users\tonyno\Desktop\Proyectos Python GitHub\Visor\Fotos_Prueba').glob('*')
    for archivo in archivosCopiar:
        shutil.copy(archivo, manager.config.cObservador)
    gestionArchivos.moverArchivosEnOrigen()
    assert os.path.exists(r'prueba_Fotos\Destino\2022-03-25\003\OK\00003_003_OK_25032022_082112.jpeg')
    
    logger.debug('-------------- Con BBDD OK -----------------')
    manager.conexBBDD = True
    for carpeta in [manager.config.cObservador, manager.config.cDestino]:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta) 
        os.makedirs(carpeta)
    shutil.copy(r"test\Muestra_bbdd_CX482.db", "bbdd_CX482.db")
    archivosCopiar = Path(r'C:\Users\tonyno\Desktop\Proyectos Python GitHub\Visor\Fotos_Prueba').glob('*')
    for archivo in archivosCopiar:
        shutil.copy(archivo, manager.config.cObservador)
    gestionArchivos.moverArchivosEnOrigen()
    assert os.path.exists(r'prueba_Fotos\Destino\2022-03-25\003\OK\00003_003_OK_25032022_082112.jpeg')
    os.remove('bbdd_CX482.db') if os.path.exists('bbdd_CX482.db') else ...
    for carpeta in [manager.config.cObservador, manager.config.cDestino]:
        shutil.rmtree(carpeta) if os.path.exists(carpeta) else ...




    # TODO : Comprobar archivos *FOK  CX482
    # TODO : Usar carpetas temporales ??




    # manager.gestionArchivos.moverArchivosExistentesV2()
    
    
        
    


