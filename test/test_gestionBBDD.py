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

def test_comprobarConexBBDD():
    os.remove('bbdd_CX482.db') if os.path.exists('bbdd_CX482.db') else ...
    os.remove('bbdd_q2.db') if os.path.exists('bbdd_q2.db') else ...

    manager = ManagerQ2()
    gestionBBDD  = manager.gestionBBDD
    gestionBBDD.comprobarConexBBDD()
    assert manager.conexBBDD == False

    shutil.copy(r"test\Muestra_bbdd_q2.db", "bbdd_q2.db")
    gestionBBDD.comprobarConexBBDD()
    assert manager.conexBBDD == True

    manager = ManagerCX482()
    gestionBBDD  = manager.gestionBBDD  
    gestionBBDD.comprobarConexBBDD()
    assert manager.conexBBDD == False

    shutil.copy(r"test\Muestra_bbdd_CX482.db", "bbdd_CX482.db")
    gestionBBDD.comprobarConexBBDD()
    assert manager.conexBBDD == True

    os.remove('bbdd_CX482.db') if os.path.exists('bbdd_CX482.db') else ...
    os.remove('bbdd_q2.db') if os.path.exists('bbdd_q2.db') else ...
    


def test_BBDD_comprobarFOK_Q2():
    shutil.copy(r"test\Muestra_bbdd_q2.db", "bbdd_q2.db")
    fotoOK = '00001_001_OK_08062022_175039.jpeg'
    fotoFKO = '00272_007_OK_04032022_234201.jpeg'
    fotoNoEstaEnBBDD = '00001_001_OK_08062022_1750391.jpeg'
    manager = ManagerQ2()
    gestionBBDD  = manager.gestionBBDD
    try: 
        gestionBBDD.comprobarConexBBDD()
    except Exception as e:
        print(e)
    assert gestionBBDD.comprobarFOK(fotoFKO) == 'FKO'
    assert gestionBBDD.comprobarFOK(fotoOK) == 'OK'
    assert gestionBBDD.comprobarFOK(fotoNoEstaEnBBDD) == False
    os.unlink("bbdd_q2.db")

def test_BBDD_comprobarFOK_CX482():
    shutil.copy(r"test\Muestra_bbdd_CX482.db", "bbdd_CX482.db")
    fotoOK = '00496_000_OK_15032022_121256.jpeg'
    fotoFKO = '00002_006_NG_15032022_121310.jpeg'
    fotoNoEstaEnBBDD = '00003_003_OK_06052022_1224131.jpeg'
    manager = ManagerCX482()
    gestionBBDD  = manager.gestionBBDD
    try: 
        gestionBBDD.comprobarConexBBDD()
    except Exception as e:
        print(e)
    assert gestionBBDD.comprobarFOK(fotoFKO) == 'FKO'
    assert gestionBBDD.comprobarFOK(fotoOK) == 'OK'
    assert gestionBBDD.comprobarFOK(fotoNoEstaEnBBDD) == False
    os.unlink("bbdd_CX482.db")
    
    # ('15/03/22 11:24:47', 90158082, '9015808270201503221113', 97, 1, 50, 100, 50, 100, 0, 95, 1, 50, 98, 50, 92, 0, 96, 1, 50, 99, 50, 98, 0, 96, 1, 50, 88, 50, 100, 0, 90, 1, 50, 55, 50, 60, 0, 93, 1, 50, 97, 50, 96, 0, 69, 1, 50, 94, 50, 16, 1, 66, 1, 50, 15, 50, 0, 1, 'Modulo OK', 0, 'MANO IZQ LED 1', '00496_000_OK_15032022_121256.jpeg', 1, 'MANO IZQ LED 2', '00497_001_OK_15032022_121258.jpeg', 2, 'MANO IZQ LED 3', '00498_002_OK_15032022_121301.jpeg', 3, 'MANO IZQ LED 4', '00499_003_OK_15032022_121303.jpeg', 4, 'MANO IZQ LED 5', '00000_004_OK_15032022_121305.jpeg', 5, 'MANO IZQ LED 6', '00001_005_OK_15032022_121307.jpeg', 6, 'MANO IZQ LED 7', '00002_006_NG_15032022_121310.jpeg', 7, 'MANO IZQ LED 8', '00003_007_NG_15032022_121429.jpeg', None, None, None, None, None, None, None, None, 0, 0) 