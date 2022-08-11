# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 17:19:35 2022

@author: tonyno
"""
# Fecha ; Hora; Referencia; % de Busqueda;Busqueda OK;Min ribbon 1;Valor Medido ribbon 1;Minimo ribbon 2;
# Valor medido ribbon 2;Validado Operario?;% de Busqueda 2º Led;Busqueda OK 2 led;
# Min ribbon 1 - 2 led;Valor Medido ribbon 1 - 2 led;Minimo ribbon 2 - led ;
# Valor medido ribbon 2 - 2 led;Validado Operario? 2 led;


#2022-03-04 08:34:15,476 - INFO - Registro 1 : ['04/03/22 08:35:29', '9019698917WW2203040839##L3727757320600351ARA11##', '98', True, '55', '97', '55', '99', False, '90', True, '55', '100', '55', '100', False, 'Modulo HB OK', 
# '002', 'LED 3 HB IZQ 1', '00467_002_OK_04032022_083156.jpeg', '003', 'LED 4 HB IZQ 2', '00468_003_OK_04032022_083159.jpeg']


import sqlite3 as sql
from datetime import datetime
from pathlib import Path
import pdb
import os
 
class GestionBBDD:
    def __init__(self, manager):
        self.manager = manager
        self.logger = self.manager.logger
        self.gestionModelo = self.manager.gestionModelo
        self.nombreBBDD = self.manager.gestionModelo.nombreBBDD
        self.consultaCreacion = self.manager.gestionModelo.consultaCreacion
        self.consultaGrabar = self.manager.gestionModelo.consultaGrabar

    def comprobarConexBBDD(self):
        self.logger.debug(f"Conectando con BBDD ({self.nombreBBDD})")
        conn = sql.connect(self.nombreBBDD)
        cursor = conn.cursor()
        try:   
            cursor.execute('select * from datosInspeccion')
        except Exception as e:
            self.logger.error('Error al conectar con BBDD')
            self.logger.error(e)
        else:
            self.manager.conexBBDD = True
            self.logger.debug('Conexion a BBDD ... OK')
        finally:
            conn.close()

        

    def comprobarFOK(self, fotoJPEG):
        if self.manager.conexBBDD == False:
            self.logger.error('BBDD No disponible, no se puede comprobarFOK()')
            return False
        resultadoFinal = []
        conn = sql.connect(self.nombreBBDD)
        cursor = conn.cursor()
        infoKeyence = self.manager.gestionModelo.infoKeyence
        # cantidad de registros que hay en cada ref, creada una lista y depues buscar el valor mas alto
        nLed = max([len(infoKeyence[ref].keys()) for ref in infoKeyence])
        for numeroled in range(1, nLed+1):
            cursor.execute(f'select Val_oper_L{numeroled} from datosInspeccion where FotoLed{numeroled} = "{fotoJPEG}"')
            resultado = cursor.fetchall()
            if resultado:
                resultadoFinal = resultado[0][0]
        conn.close()
        if resultadoFinal not in [0, 1]:
            return False
        return 'OK' if resultadoFinal == 0 else 'FKO'
    


    def createDB(self):
        conn = sql.connect(self.nombreBBDD)
        conn.commit()
        conn.close()

    def crearTablas(self):
        conn = sql.connect(self.nombreBBDD)
        cursor = conn.cursor()
        cursor.execute(self.consultaCreacion)
        conn.commit()
        conn.close()

    def insertarEnBBDD(self, registro):
        self.logger.debug(f'Cantidad de registros {len(registro)}')
        if len(registro) > 1:
            for l in range(0, len(registro)):
                self.logger.debug(f'Registro Nº{l}:')
                self.logger.debug(f'Cantidad de campo: {len(registro[l])}')
                self.logger.debug(f'Registro : {registro[l]}')
        try:
            conn = sql.connect(self.nombreBBDD)
            cursor = conn.cursor()
            instruccion = self.consultaGrabar
            cursor.executemany(instruccion, registro)
            conn.commit()
            conn.close()
            self.logger.debug('Registros introducidos con exito en BBDD')
        except Exception as e:
            self.logger.error('Ha ocurrido un error al introducir en BBDD')
            self.logger.error(e)

    def cantidadRegistros(self):
        conn = sql.connect(self.nombreBBDD)
        cursor = conn.cursor()
        cursor.execute('select count(*) from datosInspeccion')
        cantidad = cursor.fetchone()
        conn.close()
        return cantidad[0]
    
    def comprobarCampoErroneoCX482(self):
        conn = sql.connect(self.nombreBBDD) 
        cursor = conn.cursor()
        cursor.execute('ALTER TABLE datosInspeccion RENAME COLUMN Med_oper_L7 to Val_oper_L7')
        conn.commit()
        conn.close()
    
    def listadoColumnas(self):
        """Devuelve una lista de columnas de la tabla datosInspeccion"""
        conn = sql.connect(self.nombreBBDD)
        cursor = conn.cursor()
        lista = []
        for row in cursor.execute("SELECT name FROM pragma_table_info('datosInspeccion')"):
            lista.append(row[0])
        conn.close()
        return lista
    
    def encuentraReferencia(self, ref):
        """Devuelve una tuppla anidada con todas las coincidencias de una referencia"""
        conn = sql.connect(self.nombreBBDD)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM datosInspeccion WHERE RefCompleta LIKE '%{ref}%'")
        lista = cursor.fetchall()
        conn.close()
        return lista
