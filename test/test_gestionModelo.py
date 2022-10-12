from lib2to3.pytree import HUGE
import logging
from pathlib import Path
from funciones.gestionRegistros import GestionRegistros
from funciones.gestionBBDD import GestionBBDD
from config import gestionModeloQ2, gestionModeloCX482
from config import config
import logging
import pdb
import os
import shutil

class ManagerQ2:
    def __init__(self):
        self.logger = logging.getLogger('My_Logger')
        self.gestionModelo = gestionModeloQ2
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
                    'Num_Inspecciones_Obj' : 4,
                    'tiempoScanMedido' : 0,
                    'Num_Inspecciones_Interno' : 4,
                    'Pausa' : True,
                    'resetVisor' : False,
                    'cicloOk' : False,
                    'cicloInterrumpido' : False
                    }

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
    
    
def test_convertirCadena():
    
    logger = logging.getLogger('My_Logger')
    logger.error('error')
    cadena4Led = '02/03/22;17:03:30;372781590NCA2203021704##L3727757020571663ARA11##;93;TRUE;55;100;55;100;FALSE;91;TRUE;55;100;55;100;FALSE;Modulo LB OK;\r04/03/22;17:03:30;901969880NCA2203021704##L3727757020571663ARA11##;93;TRUE;55;100;55;100;FALSE;91;TRUE;55;100;55;100;FALSE;Modulo HB OK;\r'
    cadena2Led = '02/03/22;17:03:30;372781590NCA2203021704##L3727757020571663ARA11##;93;TRUE;55;100;55;100;FALSE;91;TRUE;55;100;55;100;FALSE;Modulo LB OK;\r'
    cadenaKO = '02/03/22;17:03:30;372781610NCA2203021704##L3727'
    esperado =[
        ['02/03/22 17:03:30', 37278159,'372781590NCA2203021704##L3727757020571663ARA11##'],
        ['04/03/22 17:03:30', 90196988,'901969880NCA2203021704##L3727757020571663ARA11##']
    ]
    # Cadena 4 LED OK
    cadena = gestionModeloQ2.convertirCadena(cadena4Led, logger, 4)
    assert cadena[0][0] == esperado[0][0]
    assert cadena[0][1] == esperado[0][1]
    assert cadena[0][2] == esperado[0][2]
    assert cadena[1][0] == esperado[1][0]
    assert cadena[1][1] == esperado[1][1]
    assert cadena[1][2] == esperado[1][2]
    assert cadena[0][-1] == 'Modulo LB OK'
    assert cadena[1][-1] == 'Modulo HB OK'
    assert len(cadena) == 2
    assert len(cadena[0]) == 18
    assert len(cadena[1]) == 18

    # Cadena 2 LED OK
    cadena = gestionModeloQ2.convertirCadena(cadena2Led, logger, 2)
    assert len(cadena) == 1
    assert len(cadena[0]) == 18

def test_gestionRegistro_2_Inspecciones_Q2():
    shutil.copy(r"test\Muestra_bbdd_q2.db", "bbdd_q2.db")
    registroPLC_2Led = '02/03/22;17:03:30;372781610NCA2203021704##L3727757020571663ARA11##;93;TRUE;55;100;55;100;FALSE;91;TRUE;55;100;55;100;FALSE;Modulo LB OK;\r'
    managerQ2 = ManagerQ2()
    gestionBBDD = managerQ2.gestionBBDD
    managerQ2.conexionPLC.valoresPLC['Num_Inspecciones_Obj'] = 2
    managerQ2.conexionPLC.valoresPLC['Num_Inspecciones_Interno'] = 2
    managerQ2.conexionPLC.valoresPLC['Datos_Registro'] = registroPLC_2Led
    managerQ2.conexBBDD = True
    managerQ2.cicloVisor.listaArchivosCreados = [
            Path('00001_006_OK_01042022_133341.jpeg'),
            Path('00001_007_OK_01042022_133341.jpeg'),
            ]
    # pdb.set_trace()
    cantidad = gestionBBDD.cantidadRegistros()
    gestionRegistro = GestionRegistros(managerQ2)
    gestionRegistro.gestionRegistro()
    assert len(gestionRegistro.registroProcesado) == 1
    # assert registroFinal[0][-6:] == ['006', 'LED 3 LB DRCH 1', '00001_006_OK_01042022_133341.jpeg', '007', 'LED 4 LB DRCH 2', '00001_007_OK_01042022_133341.jpeg']
    assert cantidad + 1 == gestionBBDD.cantidadRegistros()
    os.remove('bbdd_q2.db') if os.path.exists('bbdd_q2.db') else ...

def test_gestionRegistro_4_Inspecciones_Q2():
    shutil.copy(r"test\Muestra_bbdd_q2.db", "bbdd_q2.db")
    registroPLC_4Led = '02/03/22;17:03:30;372781610NCA2203021704##L3727757020571663ARA11##;93;TRUE;55;100;55;100;FALSE;91;TRUE;55;100;55;100;FALSE;Modulo LB OK;\r02/03/22;17:03:30;372781590NCA2203021704##L3727757020571663ARA11##;93;TRUE;55;100;55;100;FALSE;91;TRUE;55;100;55;100;FALSE;Modulo HB OK;\r'
    managerQ2 = ManagerQ2()
    gestionBBDD = managerQ2.gestionBBDD
    managerQ2.conexionPLC.valoresPLC['Num_Inspecciones_Obj'] = 4
    managerQ2.conexionPLC.valoresPLC['Num_Inspecciones_Interno'] = 4
    managerQ2.conexionPLC.valoresPLC['Datos_Registro'] = registroPLC_4Led
    managerQ2.conexBBDD = True
    managerQ2.cicloVisor.listaArchivosCreados = [
            Path('00001_000_OK_01042022_133341.jpeg'),
            Path('00001_001_OK_01042022_133341.jpeg'),
            Path('00001_007_OK_01042022_133341.jpeg'),
            Path('00001_006_OK_01042022_133341.jpeg')
            ]
    
    cantidad = gestionBBDD.cantidadRegistros()
    gestionRegistro = GestionRegistros(managerQ2)
    gestionRegistro.gestionRegistro()
    # pdb.set_trace()
    assert len(gestionRegistro.registroProcesado) == 2
    assert len(gestionRegistro.registroProcesado[0]) == 24
    assert len(gestionRegistro.registroProcesado[1]) == 24
    assert cantidad + 2 == gestionBBDD.cantidadRegistros()
    os.remove('bbdd_q2.db') if os.path.exists('bbdd_q2.db') else ...
    # assert registroFinal[0][-6:] == ['007', 'LED 4 LB DRCH 2', '00001_007_OK_01042022_133341.jpeg', '006', 'LED 3 LB DRCH 1', '00001_006_OK_01042022_133341.jpeg']
    # assert registroFinal[1][-6:] == ['000', 'LED 1 LB IZQ 1', '00001_000_OK_01042022_133341.jpeg', '001', 'LED 2 LB IZQ 2', '00001_001_OK_01042022_133341.jpeg']

def test_gestionRegistro_Inspecciones_CX482():
    shutil.copy(r"test\Muestra_bbdd_CX482.db", "bbdd_CX482.db")
    registroPLC = '07/03/22;15:56:32;9015808041670703221543;93;TRUE;50;100;50;100;FALSE;96;TRUE;50;92;50;50;FALSE;92;TRUE;50;100;50;99;FALSE;97;TRUE;50;92;50;100;FALSE;99;TRUE;50;99;50;98;FALSE;99;TRUE;50;100;50;100;FALSE;68;TRUE;50;96;50;97;FALSE;99;TRUE;50;100;50;98;FALSE;Modulo OK;\r'
    managerCX482 = ManagerCX482()
    gestionBBDD = managerCX482.gestionBBDD
    managerCX482.conexionPLC.valoresPLC['Num_Inspecciones_Obj'] = 8
    managerCX482.conexionPLC.valoresPLC['Num_Inspecciones_Interno'] = 8
    managerCX482.conexionPLC.valoresPLC['Datos_Registro'] = registroPLC
    managerCX482.conexBBDD = True
    managerCX482.cicloVisor.listaArchivosCreados = [
            Path('00001_008_OK_01042022_133341.jpeg'),
            Path('00001_009_OK_01042022_133341.jpeg'),
            Path('00001_010_OK_01042022_133341.jpeg'),
            Path('00001_011_OK_01042022_133341.jpeg'),
            Path('00001_012_OK_01042022_133341.jpeg'),
            Path('00001_013_OK_01042022_133341.jpeg'),
            Path('00001_014_OK_01042022_133341.jpeg'),
            Path('00001_015_OK_01042022_133341.jpeg')
            ]
    # pdb.set_trace()
    cantidad = gestionBBDD.cantidadRegistros()
    gestionRegistro = GestionRegistros(managerCX482)
    try:
        gestionRegistro.gestionRegistro()
    except Exception as e:
        managerCX482.logger.error('Error')
        managerCX482.logger.error(e)
    assert len(gestionRegistro.registroProcesado) == 1
    # assert registroFinal[0][-6:] == ['006', 'LED 3 LB DRCH 1', '00001_006_OK_01042022_133341.jpeg', '007', 'LED 4 LB DRCH 2', '00001_007_OK_01042022_133341.jpeg']
    assert cantidad + 1 == gestionBBDD.cantidadRegistros()
    os.remove('bbdd_CX482.db') if os.path.exists('bbdd_CX482.db') else ...
