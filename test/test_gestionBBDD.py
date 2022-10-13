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
import pytest
from tempfile import TemporaryDirectory



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

@pytest.fixture(scope='module')
def tmp_dir():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        yield db_path

@pytest.fixture(scope='function')
def tmp_dir_funcion():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        yield db_path

@pytest.fixture(scope='module')
def BBDD_Q2(tmp_dir, logger):
    dest = Path(tmp_dir, 'bbdd_q2.db')
    orig = Path('test', 'Muestra_bbdd_q2.db')
    print(orig)
    shutil.copy(orig, dest)
    gestionBBDD = GestionBBDD(gestionModeloQ2, dest, logger)
    yield gestionBBDD

@pytest.fixture(scope='module')
def BBDD_CX482(tmp_dir, logger):
    dest = Path(tmp_dir, 'bbdd_CX482.db')
    orig = Path('test', 'Muestra_bbdd_CX482.db')
    shutil.copy(orig, dest)
    gestionBBDD = GestionBBDD(gestionModeloCX482, dest, logger)
    yield gestionBBDD

@pytest.fixture(scope='module')
def logger():
    logger = logging.getLogger('My_Logger')
    yield logger


def test_creacion_BBDD_Q2(tmp_dir_funcion, logger):
    ruta = Path(tmp_dir_funcion, 'bbdd_q2.db')
    # os.remove(ruta) if ruta.exists() else ...
    assert not ruta.exists()
    GestionBBDD(gestionModeloQ2, ruta, logger)
    assert ruta.exists()

def test_creacion_BBDD_CX482(tmp_dir_funcion, logger):
    ruta = Path(tmp_dir_funcion, 'bbdd_CX482.db')
    # os.remove(ruta) if ruta.exists() else ...
    assert not ruta.exists()
    GestionBBDD(gestionModeloCX482, ruta, logger)
    assert ruta.exists()

def test_abrir_BBDD_existente_Q2(BBDD_Q2):
    gestionBBDD = BBDD_Q2
    ruta = gestionBBDD.db_path
    assert ruta.exists()

def test_abrir_BBDD_existente_CX482(BBDD_CX482):
    gestionBBDD = BBDD_CX482
    ruta = gestionBBDD.db_path
    assert ruta.exists()

def test_gestionBBDD_comprobarFKO_Q2_NOEXISTE(BBDD_Q2):
    resultado = BBDD_Q2.comprobarFOK('NOEXISTE')
    assert not resultado

def test_gestionBBDD_comprobarFKO_Q2_OK(BBDD_Q2):
    resultado = BBDD_Q2.comprobarFOK('00135_006_OK_04032022_223459.jpeg')
    assert resultado == 'OK'

def test_gestionBBDD_comprobarFKO_Q2_KO(BBDD_Q2):
    '''No es un error, la funcion solo busca FOK'''
    resultado = BBDD_Q2.comprobarFOK('00233_000_NG_08032022_061859.jpeg')
    assert resultado == 'OK'

def test_gestionBBDD_comprobarFKO_Q2_Falso_KO(BBDD_Q2):
    resultado = BBDD_Q2.comprobarFOK('00272_007_OK_04032022_234201.jpeg')
    assert resultado == 'FKO'

def test_gestionBBDD_comprobarFKO_CX482_NOEXISTE(BBDD_CX482):
    resultado = BBDD_CX482.comprobarFOK('NOEXISTE')
    assert not resultado

def test_gestionBBDD_comprobarFKO_CX482_OK(BBDD_CX482):
    resultado = BBDD_CX482.comprobarFOK('00244_008_OK_08032022_070923.jpeg')
    assert resultado == 'OK'

def test_gestionBBDD_comprobarFKO_CX482_KO(BBDD_CX482):
    '''No es un error, la funcion solo busca FOK'''
    resultado = BBDD_CX482.comprobarFOK('00129_013_NG_14032022_115348.jpeg')
    assert resultado == 'OK'

def test_gestionBBDD_comprobarFKO_CX482_Falso_KO(BBDD_CX482):
    resultado = BBDD_CX482.comprobarFOK('00171_007_NG_14032022_144949.jpeg')
    assert resultado == 'FKO'


@pytest.mark.skip
def otracosa():
    ruta = Path('test', 'Muestra_bbdd_q2.db')
    shutil.copy(ruta, "bbdd_q2.db")
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
    

@pytest.mark.skip
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

@pytest.mark.skip
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