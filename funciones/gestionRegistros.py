from pathlib import Path
import pdb

class GestionRegistros():
    """Recupera un registro del PLC, modifica los campos, lo convierte en una lista y lo graba en la BBDD"""
    def __init__(self, manager):
        self.manager = manager
        self.logger = self.manager.logger
        self.gestionBBDD = self.manager.gestionBBDD
        self.convertirCadena = self.manager.gestionModelo.convertirCadena
        self.infoKeyence = self.manager.gestionModelo.infoKeyence

    def gestionRegistro(self):
        self.listaFotosVisualizadas = self.manager.cicloVisor.listaArchivosCreados
        self.nInspeccionesObjetivo = self.manager.conexionPLC.valoresPLC['Num_Inspecciones_Obj']
        self.logger.debug('Gestionando Registro ...')
        registro = self.manager.conexionPLC.valoresPLC['Datos_Registro']
        self.logger.debug(f'Registro a Gestionar : {registro}')
        try:
            self.nFotosObjetivo = self.manager.gestionModelo.infoModelo[self.nInspeccionesObjetivo]['cFotoJPG']
            self.logger.debug(f"Nº de inspecciones objetivo para convertir cadena {self.nInspeccionesObjetivo}")
            self.registroProcesado = self.convertirCadena(registro, self.logger, self.nInspeccionesObjetivo)
            self._imprimirRegistroEnLog()
            self._comprobarFotos()
            registroFinal = self._agregaInfoFoto()
            if self.manager.conexBBDD == True:
                self.gestionBBDD.insertarEnBBDD(registroFinal)
            else:
                self.logger.error('BBDD No conectada, registro no introducido')
                self.manager.gestionBBDD.comprobarConexBBDD()
        except KeyError as e:
            self.logger.error('Error en configModelo, gestionModelo.infoModelo[self.nInspeccionesObjetivo]["cFotoJPG"]')
            self.logger.error(f'No existe la Key:{e} en la conf.')

        except ValueError as e:
            self.logger.error('Error al procesar registro')
            self.logger.error(e)
        
        except Exception as e:
            self.logger.error('Error general de gestinRegistro')
            self.logger.error(e)
        
        finally:
            self.manager.conexionPLC.valoresPLC['cicloOk'] = True
            

        
    def _agregaInfoFoto(self):
        registroProcesado = self.registroProcesado
        ListadeFotos = self.listaFotosVisualizadas
        infoKeyence = self.infoKeyence
        registroFinal = []
        comprobarRepetidas = []

        for cadena in registroProcesado:
            referencia = cadena[1]
            fotos = ListadeFotos
            fotos = list(filter(lambda x: x.stem[6:9] in infoKeyence[referencia], fotos))
            cadenaAAgregar = []
            for numeroDeFoto in range(0, len(fotos)):
                foto = fotos[numeroDeFoto]
                nProgramadeFoto = foto.stem[6:9]
                if nProgramadeFoto not in comprobarRepetidas:
                    comprobarRepetidas.append(nProgramadeFoto)
                else:
                    self.logger.warning(f'OJO, Escena {nProgramadeFoto} Repetida !!')
                    self.logger.warning(list(map(lambda x: x.name ,ListadeFotos)))
                try:
                    cadenaAAgregar.extend([nProgramadeFoto, infoKeyence[referencia][nProgramadeFoto], foto.name])
                except Exception as e:
                    self.logger.error('Se ha producido un error en _agregaInfoFoto()')
                    self.logger.error(f"cadenaAAgregar.append({nProgramadeFoto}, infoKeyence[{referencia}][{nProgramadeFoto}],[{foto}])")
                    self.logger.error(e)
                    return False
            cadena.extend(cadenaAAgregar)
            registroFinal.append(cadena)
        return registroFinal
   
            
    def _comprobarFotos(self):
        self.logger.debug('Revisando cantidad de fotos ...')
        if len(self.listaFotosVisualizadas) != self.nFotosObjetivo:
            raise ValueError(f"cantidad de fotos ({len(self.listaFotosVisualizadas)}) diferentes de la esperada ({self.nFotosObjetivo}) erronea !!")
        else:
            self.logger.debug(f'Cantidad de fotos ({len(self.listaFotosVisualizadas)}) Ok')

        
    def _imprimirRegistroEnLog(self):
        for a in self.registroProcesado:
            self.logger.debug('Referencia guardada :')
            self.logger.debug(a[1])

