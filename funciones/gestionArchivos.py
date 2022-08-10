from datetime import datetime
import shutil
from pathlib import Path
import os
import re
import pdb
import sqlite3

class GestionArchivos:
    """Gestiona el movimiento de archivos entre carpetas y ordenacion"""
    def __init__(self, manager):
        self.manager = manager
        self.logger = self.manager.logger
        self.config = self.manager.config
        self.gestionModelo = self.manager.gestionModelo
        self.gestionBBDD = self.manager.gestionBBDD
    
    def moverListaArchivosInpeccionados(self, listaArchivos):
        """Recibe una Lista de archivos pathlib.Path y Mueve todos a carpeta config.cDestino clasificando con BBDD"""
        logger = self.logger
        for archivo in listaArchivos:
            try:
                self._mueveArchivosClasificados(archivo)
            except Exception as e:
                logger.error('Error al moverArchivosEnOrigen')
                logger.error(e)
        logger.info(f'Archivos Movido con exito!')



    def moverArchivosEnOrigen(self):
        """Mueve todos los archivos existentes en config.cObservador con extension ['.jpeg', '.bmp', '.iv2p'] a carpeta config.cDestino clasificando con BBDD"""
        cObservador = self.config.cObservador
        cDestino = self.config.cDestino
        logger = self.logger
        logger.debug(f'Moviendo archivos {cObservador} a {cDestino}  ..... ')
        for folderName, subfolders, filenames in os.walk(cObservador):
            for filename in filenames:
                if Path(filename).suffix in ['.jpeg', '.bmp', '.iv2p']:
                    archivo = Path(folderName, filename)
                    self._mueveArchivosClasificados(archivo)
                    
        logger.info(f'Archivos Movido con exito!')


    def _mueveArchivosClasificados(self, archivo):
        """ Recibe una ruta completa con archivo tipo pathlib.Path y mueve el archivo clasificado [config.cDestino][Fecha(2022-06-31)][Escena][OK o NG][Fotos_FOK]"""
        # 00111_003_NG_02062022_065639.iv2p
        logger = self.logger
        cDestino = self.config.cDestino
        validacion = re.compile(r'^\d{5}_\d{3}_[NnOo][GgKk]')
        if not isinstance(archivo, Path) or not validacion.search(archivo.stem):
            raise ValueError(f'Archivo no valido {archivo}')

        fecha, escena, juicio = self._encuentraDia_Escena_Juicio(archivo.name)
        fecha = fecha.strftime('%Y-%m-%d')
        try:
            fok = self.gestionBBDD.comprobarFOK(archivo.stem + '.jpeg')
        except sqlite3.OperationalError as e:
            logger.error('Error al comprobarFOK en BBDD')
            if str(e).find('Val_oper_L7'):
                logger.warning('Detectada Val_oper_L7, Corrigiendo')
                self.gestionBBDD.comprobarCampoErroneoCX482()
                fok = False
            else:
                logger.error(e)
        except Exception as e:
            logger.error('Error al comprobarFOK en BBDD')
            logger.error(e)
            fok = False
        
        if not fok:
            # logger.warning(f'Foto no encontrada en BBDD {archivo.name}')
            destino = Path(cDestino, fecha, escena, juicio, archivo.name)
        elif fok == 'OK':
            # logger.debug(f'Foto encontrada en BBDD')
            destino = Path(cDestino, fecha, escena, juicio, archivo.name)
        elif fok == 'FKO':
            # logger.debug(f'Foto encontrada en BBDD')
            destino = Path(cDestino, fecha, escena, juicio, 'Fotos_FOK', archivo.name)
        else:
            raise ValueError(f'Error de comprobado BBDD, {archivo.name}')
        try:
            if not destino.parent.exists():
                os.makedirs(destino.parent)
            shutil.move(archivo, destino)
        except Exception as e:
            logger.error(f'Error creando carpetas {destino.parent}')
            logger.error(e)

        # listaImagenes = list(filter(lambda x: x.suffix in ['.jpeg', '.bmp', '.iv2p'], listaArchivo))

    def _encuentraDia_Escena_Juicio(self, dateString):
        """Encuentra la fecha, escena y juicio y devuelve una tupla (datetime, '000', 'NG' o 'OK') probado sobre fechas : 00000_000_NG_Jun202022_180740 o 00003_007_OK_31032022_172842"""
        fechaNumero = re.compile(r'\d{8}')
        fechaConLetra = re.compile(r'[a-zA-Z]{3}\d{6}')
        juicio = re.compile(r'[NnOo][GgKk]').search(dateString).group(0)
        escena = str(dateString)[6:9]
        if fechaNumero.search(dateString):
            dia = (fechaNumero.search(dateString)).group(0)
            return datetime.strptime(dia, '%d%m%Y'), escena, juicio
        elif fechaConLetra.search(dateString):  
            dia = (fechaConLetra.search(dateString)).group(0)
            return datetime.strptime(dia, '%b%d%Y'), escena, juicio
        else:
            raise ValueError(f'Error sacando fecha {dateString}')



    """ def mueveTodoFtpToSubir(logger, cObservador):
        for folderName, subfolders, filenames in os.walk(cObservador):
                for filename in filenames:
                    archivo = Path(folderName, filename)
                    if archivo.suffix in ('.iv2p', '.jpeg', '.bmp'):
                            logger.info(f'Moviendo Archivo {archivo}')
                            try:
                                dia = f"{str(archivo.name)[13:15]}-{str(archivo.name)[15:17]}-{str(archivo.name)[17:21]}"
                                carpetaDestino = Path(cObservador, dia)
                                if not carpetaDestino.is_dir():
                                    logger.debug(f'creando carpeta Destino : {carpetaDestino}')
                                    os.mkdir(carpetaDestino)
                                if archivo.is_file():
                                    logger.debug(f'Archivo existente, Moviendo archivo {archivo} a {carpetaDestino}')
                                try:
                                    shutil.move(archivo, Path(carpetaDestino, archivo.name))
                                    logger.info(f'Archivo {archivo} Movido con exito!')
                                except Exception as e :
                                    logger.error(f'Error en la copia : {e}')
                            except:
                                logger.error(f'Imposible mover el archivo {archivo}')
                                pass """   

