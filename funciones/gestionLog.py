import logging
from pathlib import Path
import os
from logging.handlers import RotatingFileHandler, QueueHandler

def generadorDeLogs(ubicacionLog, nombreLog, cola):
    # ubicacionLog = ubicacionLog
    # nombreLog = nombreLog
    logger = logging.getLogger('My_Logger')
    formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    if not Path(ubicacionLog).exists():
        os.makedirs(ubicacionLog)
    archivoLog = Path(ubicacionLog, nombreLog)
    handlerArchivo = RotatingFileHandler(str(archivoLog), maxBytes=5242880, backupCount=10)
    handlerArchivo.setFormatter(formato)
    handlerPantalla = logging.StreamHandler()
    handlerPantalla.setFormatter(formato)
    handlerCola = QueueHandler(cola)
    handlerCola.setFormatter(formato)

    logger.addHandler(handlerArchivo)
    logger.addHandler(handlerPantalla)
    logger.addHandler(handlerCola)
    logger.setLevel(logging.DEBUG)
    return logger
    ###

    