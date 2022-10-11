# 29-7-2022 -> Cambiada la gestion de keyence y el int de la referencia
# metido lambda para simplifcar
# No devuelvo False, sino ValueError

################### GESTION DE MODELOS ################
### Q2 - 5/03/2022 ###

### INFORMECION SOBRE LED Y REGISTROS
# Diccionario que se bases en el nº led y da toda la info a partir de ese dato
# cRegObj = cantidad lineas de registros retornadas por el PLC
# cRegCampPLC = cantidad de campos recibido del PLC y tratados
# cRegCamp = Cantidad de campos en cada linea de registro que debe recibir la BBDD
# cFotoJPG = cantidad de fotos JPG
# cFotoTotal = cantidad de fotos totales a mover

### Muestra cadena del PLC:
## 0: 02/03/22;17:03:30;372781610NCA2203021704##L3727757020571663ARA11##;93;TRUE;55;100;55;100;FALSE;91;TRUE;55;100;55;100;FALSE;Modulo LB OK;
## 1: 02/03/22;17:03:30;372781610NCA2203021704##L3727757020571663ARA11##;93;TRUE;55;100;55;100;FALSE;91;TRUE;55;100;55;100;FALSE;Modulo HB OK;
nombreVisor = 'Audi Q2'

infoModelo = {
    # Numero de led objetivo
    2 : {
        'cRegObj' : 1,
        'cRegCampPLC' : 18,
        'cRegCamp' : 24,
        'cFotoJPG' : 2,

    },
    4 : {
        'cRegObj' : 2,
        'cRegCampPLC' : 18,
        'cRegCamp' : 24,
        'cFotoJPG' : 4,
    }
}

### Funcion convertir convertir cadena convierte la cadena para siga la siguiente estructura :
# ['Fecha Hora', 'Referencia Corta', 'Referencia completa', '% Busqueda L1, 'True o False Busqueda L1', 'Valor corte R1L1'. 'Valor medido R1L1', 'Valor corte R1L1'. 'Valor medido R2L1' .... cada Led  ... 'Juicio OK o KO'

# Cambia campos string True y False por True y False Real (no se si es necesario)
# Une Fecha y hora en un solo campo
# inserta la referencia corta de 8 digitos despues de la fecha
# Devuelve una lista compuesa de listas de cada reguistro del PLC
def convertirCadena(cadenas, logger, nled):
    logger.debug('Conviertiendo cadena:')
    cadenas = cadenas.split('\r')
    cadenas.pop()
    logger.debug(cadenas)
    listaCadena = []
    for cadena in cadenas:
        cadena = cadena.split(';')
        cadena = list(map(lambda x: False if x =='FALSE' else x, cadena))
        cadena = list(map(lambda x: True if x =='TRUE' else x, cadena))
        cadena.pop()
        cadena[0] = cadena[0] + ' ' + cadena[1]
        cadena.pop(1)
        cadena.insert(1, cadena[1][:8])
        # Convirtiendo a int la referencia
        cadena[1] = int(cadena[1])

        #cadena = tuple(cadena)
        listaCadena.append(cadena)
    if nled in infoModelo:
        # pdb.set_trace()
        if infoModelo[nled]['cRegObj'] == len(listaCadena):
            logger.debug(f'Cantidad de cadenas esperada ({len(listaCadena)}) Correcta !! ')
            for linea in listaCadena:
                if len(linea) != infoModelo[nled]['cRegCampPLC']:
                    # logger.error(f"La cantidad de campos resultante ({len(linea)}) no coincide con la esperada ({infoModelo[nled]['cRegCampPLC']})")
                    # logger.error(linea)
                    raise ValueError(f"La cantidad de campos resultante ({len(linea)}) no coincide con la esperada ({infoModelo[nled]['cRegCampPLC']})")
                    return False
        else:
            # logger.error(f"No coinciden las lineas esperadas ({infoModelo[nled]['cRegObj']}) con las reales ({len(listaCadena)})")
            # logger.error(listaCadena)
            raise ValueError(f"No coinciden las lineas esperadas ({infoModelo[nled]['cRegObj']}) con las reales ({len(listaCadena)})")
            return False
        logger.debug(f'cadena tratada correctamente !! ({infoModelo[nled]["cRegObj"]} cadenas de {infoModelo[nled]["cRegCampPLC"]} registro cada uno)')
        return listaCadena
    else:
        # logger.error(f'No existe cantidad ({nled}) de led en gestion modelo')
        raise ValueError(f'No existe cantidad ({nled}) de led en gestion modelo')
        return False

infoKeyence = {
    37278159 : {'000' : 'LED 1 LB IZQ 1', '001' : 'LED 2 LB IZQ 2'},
    90196987 : {'000' : 'LED 1 LB IZQ 1', '001' : 'LED 2 LB IZQ 2'},
    90196988 : {'006' : 'LED 3 LB DRCH 1', '007' : 'LED 4 LB DRCH 2'},
    37278161 : {'006' : 'LED 3 LB DRCH 1', '007' : 'LED 4 LB DRCH 2'},
    90196989 : {'002' : 'LED 3 HB IZQ 1', '003' : 'LED 4 HB IZQ 2'},
    90196990 : {'004' : 'LED 1 HB DRCH 1', '005' : 'LED 2 HB DRCH 2'}
}

""" ### RELACION REFERENCIA CODIGO DE PROGRAMA
progKeyence = {37278159 : ['000', '001'],
            90196987 : ['000', '001'],
            90196988 : ['006', '007'],
            37278161 : ['006', '007'],
            90196989 : ['002', '003'],
            90196990 : ['004', '005']
            }

### PROGRAMA KEYENCE Y NOMBRE (SOLO SE USA PARA INFORMAR)
nombreProgKeyence = {
    '000' : 'LED 1 LB IZQ 1',
    '001' : 'LED 2 LB IZQ 2',
    '002' : 'LED 3 HB IZQ 1',
    '003' : 'LED 4 HB IZQ 2',
    '004' : 'LED 1 HB DRCH 1',
    '005' : 'LED 2 HB DRCH 2',
    '006' : 'LED 3 LB DRCH 1',
    '007' : 'LED 4 LB DRCH 2',
} """

# Listado de etapas por la que si pasa resetea variables y borra pantala
listaEtapasReseteo = [0,3,4,5,6,7,8,9]

# Nombre BBDD
# nombreBBDD = 'D:\\Python\\Visor_Q2\\bbdd_q2.db'
nombreBBDD = 'bbdd_q2.db'

# consulta SQL de grabado
consultaGrabar = 'INSERT INTO datosInspeccion VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, Null, Null, 0, 0)'

#Consulta creacion BBDD
consultaCreacion = """CREATE TABLE datosInspeccion (
    datetime text,
    refCorta integer,
    RefCompleta text,
    Busqueda_L1 integer,
    Busqueda_OK_L1 BOOLEAN,
    Min_Ribbon_1_L1 integer,
    Med_Ribbon_1_L1 integer,
    Min_Ribbon_2_L1 integer,
    Med_Ribbon_2_L1 integer,
    Val_oper_L1 BOOLEAN,
    Busqueda_L2 integer,
    Busqueda_OK_L2 BOOLEAN,
    Min_Ribbon_1_L2 integer,
    Med_Ribbon_1_L2 integer,
    Min_Ribbon_2_L2 integer,
    Med_Ribbon_2_L2 integer,
    Val_oper_L2 BOOLEAN,
    JuicioFinal text,
    NoKeyenceL1 integer,
    NombreKeyenceL1 text,
    FotoLed1 text,
    NoKeyenceL2 integer,
    NombreKeyenceL2 text,
    FotoLed2 text,
    linkDropboxFotoL1 text,
    linkDropboxFotoL2 text,
    syncGoogle BOOLEAN,
    syncSqlite_ext BOOLEAN
    )"""

# Campos de validacion operario (FKO's)
# Campo de validacion operario : campo de nombre de foto
camposValOper = {
    9 : 20,
    16 : 23,
}
