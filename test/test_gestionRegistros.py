import logging
from pathlib import Path
from unittest.mock import MagicMixin
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
                self.listaArchivosCreados = [Path('Foto{x}.jpeg') for x in range(4)]
        class _conexionPLC:
            def __init__(self):
                self.valoresPLC = {
                    'Etapa_Principal' : 2, 
                    'Marcha_Inspeccion' : 0,
                    'Datos_Registro' : '02/03/22;17:03:30;372781590NCA2203021704##L3727757020571663ARA11##;93;TRUE;55;100;55;100;FALSE;91;TRUE;55;100;55;100;FALSE;Modulo LB OK;\r04/03/22;17:03:30;901969880NCA2203021704##L3727757020571663ARA11##;93;TRUE;55;100;55;100;FALSE;91;TRUE;55;100;55;100;FALSE;Modulo HB OK;\r',
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

def test_init_GestionRegistros():
    manager = ManagerQ2()
    gestionRegistro = GestionRegistros(manager)
    isinstance(gestionRegistro, GestionRegistros)

def test_GestionRegistros():
    manager = ManagerQ2()
    gestionRegistro = GestionRegistros(manager)
    gestionRegistro.gestionRegistro()
    ### TODO: Generar BBDD correctamente en una carpeta temporal y crear el registro y compribar que el registro está
    ### TODO: Crear parametros de fixture para hacer pruebas de q2 y del cx482
