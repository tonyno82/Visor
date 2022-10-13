### Funciones Visor
import pyads
import time

class ConexPLC:
    def __init__(self, manager):
        self.manager = manager
        self.logger = self.manager.logger
        self.config = self.manager.config
        self.gestionModelo = self.manager.gestionModelo
        self.contador = self.manager.contador
        self.conex = pyads.Connection(self.config.dirAds, self.config.portAds)
        self.conexOk = False
        self.valoresPLC = {
            'Etapa_Principal' : 0, 
            'Marcha_Inspeccion' : 0,
            'Datos_Registro' : 0,
            'Num_Inspecciones_Obj' : 0,
            'tiempoScanMedido' : 0,
            'Num_Inspecciones_Interno' : 0,
            'Pausa' : True,
            'resetVisor' : False,
            'cicloOk' : False,
            'cicloInterrumpido' : False
            }
        self.stopHilo = False

        # Tiempo de espera para que una vez finalizado el scan comience el siguiente
        # En pruebas, si se pone a 0 el tiempo de ejecucion mas rapido es 45ms
        self.tiempoScan = 250
        self.tiempoRealMedidoScan = 0


    def probarConex(self):
        with self.conex as plc:
            try:
                plc.read_by_name(".Etapa_Principal", pyads.PLCTYPE_INT)
                self.conexOk = True
            except Exception as e:
                self.logger.error('Error de Conexion')
                self.conexOk = False

    def iniciarScan(self):
        self.logger.debug('Intentando iniciar ScanPLC')
        time.sleep(3)
        while not self.conexOk:
            with self.conex as plc:
                try:
                    plc.read_by_name(".Etapa_Principal", pyads.PLCTYPE_INT)
                    if self.stopHilo:
                        break
                except pyads.ADSError:
                    self.conexOk = False
                    self.logger.error('Error de conexion')
                    # time.sleep(3)
                    if self.stopHilo:
                        break
                else:
                    self.logger.info('Conexion realizada con EXITO')
                    time.sleep(3)
                    self.conexOk = True
                    if self.manager.observadorOK:
                        self.manager.show_frame(self.manager.frameVisor)
                    if self.stopHilo:
                        break
        while self.conexOk:
            with self.conex as plc:
                try:
                    inicioCicloScan = time.time()
                    self.valoresPLC['Etapa_Principal'] = plc.read_by_name(".Etapa_Principal", pyads.PLCTYPE_INT)
                    self.valoresPLC['Marcha_Inspeccion'] = plc.read_by_name(".Marcha_Inspeccion")
                    self.valoresPLC['Datos_Registro'] = plc.read_by_name(".Datos_Registro", pyads.PLCTYPE_STRING)
                    self.valoresPLC['Num_Inspecciones_Obj'] = plc.read_by_name(".Num_Inspecciones_Obj", pyads.PLCTYPE_INT)
                    self.valoresPLC['Num_Inspecciones_Interno'] = self.manager.contador
                    self.valoresPLC['Pausa'] = self._comprobarPausa()
                    # self.valoresPLC['cicloOk'] = self._comprobarCicloOK()
                    self.valoresPLC['cicloInterrumpido'] = self._comprobarCicloInterrumpido()
                    self.valoresPLC['resetVisor'] = self._comprobarReset()
                    while (time.time() - inicioCicloScan)*1000 <= self.tiempoScan:
                        pass
                    self.valoresPLC['tiempoScanMedido'] = round((time.time() - inicioCicloScan)*1000, 3)
                    if self.stopHilo:
                        break   
                except Exception as e:
                    self.logger.error('Error de conexion durante la ejecucion')
                    self.logger.error(e)
                    self.conexOk = False
                    self.manager.show_frame(self.manager.frameEventos)
                    time.sleep(1)
                    if self.stopHilo:
                        break
        if not self.conexOk and not self.stopHilo:
            self.iniciarScan()

    def _comprobarPausa(self):
        if self.valoresPLC['Marcha_Inspeccion'] and self.valoresPLC['Pausa']:
            self.logger.debug('Marcha_Inspeccion, Activando Observador')
            # self.valoresPLC['Pausa'] = False
            return False
        elif not self.valoresPLC['Marcha_Inspeccion'] \
                and self.valoresPLC['Num_Inspecciones_Interno'] == self.valoresPLC['Num_Inspecciones_Obj'] \
                and not self.valoresPLC['Pausa']:
            self.logger.debug('Marcha_Inspeccion False y Numero de inspecciones OK,  Desactivando Observador')
            # self.valoresPLC['Pausa'] = True
            return True
        else:
            return self.valoresPLC['Pausa']
            

    def _comprobarReset(self):
        if self.valoresPLC['Etapa_Principal'] in self.gestionModelo.listaEtapasReseteo and self.valoresPLC['Num_Inspecciones_Interno'] != 0 and not self.valoresPLC['resetVisor']:
            self.logger.info(f'Marcando Reset en etapa: {self.valoresPLC["Etapa_Principal"]}')
            # self.valoresPLC['resetVisor'] = True
            return True
        else:
            return self.valoresPLC['resetVisor']

    def _comprobarCicloOK(self):
        if not self.valoresPLC['Marcha_Inspeccion'] and self.valoresPLC['Num_Inspecciones_Interno'] == self.valoresPLC['Num_Inspecciones_Obj']:
            return True
        else:
            return self.valoresPLC['cicloOk']

    def _comprobarCicloInterrumpido(self):
        return False
        # No funciona ... ¿Probar con lectura Codigo de barras y si tenemos codigo de barras y perdemos ciclo?
        # Y si creamos variable inicio ciclo y si perdemos el marcha inspeccion mientras inicio ciclo ok y nºinpeccion no ok?
        """ if not self.valoresPLC['Marcha_Inspeccion'] and self.valoresPLC['Num_Inspecciones_Interno'] != self.valoresPLC['Num_Inspecciones_Obj'] and self.valoresPLC['Pausa']:
            return True
        else:
            return self.valoresPLC['cicloInterrumpido'] """


