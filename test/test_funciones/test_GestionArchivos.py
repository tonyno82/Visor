import pytest
from setuptools import SetuptoolsDeprecationWarning
from funciones import gestionArchivos
from funciones.gestionArchivos import GestionArchivos
from pathlib import Path
from tempfile import TemporaryDirectory

@pytest.fixture(scope="module")
def objetoGestionArchivos(logger, carpeta_origen, carpeta_destino):
    gestioArchivos = GestionArchivos(logger, carpeta_origen, carpeta_destino)
    yield gestioArchivos

def test_GestionArchivos_buscaArchivos_listavacio(objetoGestionArchivos):
    gestionArchivo = objetoGestionArchivos
    listado = gestionArchivo.buscaArchivos([])
    assert listado == {}
    
def test_GestionArchivos_buscaArchivos_listaOk_noexistenArchivos(objetoGestionArchivos):
    gestionArchivo = objetoGestionArchivos
    listado = gestionArchivo.buscaArchivos(
        [
            "1.txt",
            "2.txt",
            "3.txt",
            "4.txt",
            ]
    )
    assert listado == {}

def test_GestionArchivos_buscaArchivos_listaOk_SiExistenArchivos(objetoGestionArchivos):
    gestionArchivo = objetoGestionArchivos

    listaArchivos = []
    for n in range(5):
        dirDestino = objetoGestionArchivos.cDestino
        archivo = Path(dirDestino, f"archivo_{n}.txt")
        listaArchivos.append(archivo.name)
        with open(archivo, "w") as archivo:
            archivo.write(str(n))

    lista = gestionArchivo.buscaArchivos(listaArchivos)

    assert isinstance(lista, dict)
    assert len(lista) == 5
    assert isinstance(lista[listaArchivos[0]], Path)

def test_GestionArchivos_buscaArchivos_listaKO(objetoGestionArchivos):
    gestionArchivo = objetoGestionArchivos
    
    bateria_Pruebas = {
    "listaINT" : [1,2,3],
    "listaNone" : [None, None, None],
    "listaDic" : [
        {1: 0, 2: 0, 3: 0},
        {5: 0, 6: 0, 7: 0},
        ],
    "SoloNone" : None,
    "SoloString" : "text.py",
    "soloDic" : {1: 0, 2: 0, 3: 0},
    }

    for prueba in bateria_Pruebas:
        listado = gestionArchivo.buscaArchivos(bateria_Pruebas[prueba])
        assert listado == {}


def test_GestionArchivos_moverListaArchivosInpeccionados_BBDD_KO(objetoGestionArchivos):
    gestionArchivo = objetoGestionArchivos

    


    