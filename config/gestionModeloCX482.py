################### GESTION DE MODELOS ################
### CX482 - 5/03/2022 ###
# 29-7-2022 -> Cambiada la gestion de keyence y el int de la referencia
# metido lambda para simplifcar
# No devuelvo False, sino ValueError

### INFORMECION SOBRE LED Y REGISTROS
# Diccionario que se bases en el nº led y da toda la info a partir de ese dato
# cRegObj = cantidad lineas de registros retornadas por el PLC
# cRegCampPLC = cantidad de campos recibido del PLC y tratados
# cRegCamp = Cantidad de campos en cada linea de registro que debe recibir la BBDD
# cFotoJPG = cantidad de fotos JPG
# cFotoTotal = cantidad de fotos totales a mover

### Muestra cadena del PLC:
## reg = '07/03/22;15:56:32;9015808041670703221543;93;TRUE;50;100;50;100;FALSE;96;TRUE;50;92;50;50;FALSE;92;TRUE;50;100;50;99;FALSE;97;TRUE;50;92;50;100;FALSE;99;TRUE;50;99;50;98;FALSE;99;TRUE;50;100;50;100;FALSE;68;TRUE;50;96;50;97;FALSE;99;TRUE;50;100;50;98;FALSE;Modulo OK;$R'

nombreVisor = 'Ford CX482'

infoModelo = {
    # Numero de led objetivo
    8 : {
        'cRegObj' : 1,
        'cRegCampPLC' : 60,
        'cRegCamp' : 24,
        'cFotoJPG' : 8,

    }
}

### Funcion convertir convertir cadena convierte la cadena para siga la siguiente estructura :
# ['Fecha Hora', 'Referencia Corta', 'Referencia completa', '% Busqueda L1, 'True o False Busqueda L1', 'Valor corte R1L1'. 'Valor medido R1L1', 'Valor corte R1L1'. 'Valor medido R2L1' .... cada Led  ... 'Juicio OK o KO'
## muestra = '07/03/22;15:56:32;9015808041670703221543;93;TRUE;50;100;50;100;FALSE;96;TRUE;50;92;50;50;FALSE;92;TRUE;50;100;50;99;FALSE;97;TRUE;50;92;50;100;FALSE;99;TRUE;50;99;50;98;FALSE;99;TRUE;50;100;50;100;FALSE;68;TRUE;50;96;50;97;FALSE;99;TRUE;50;100;50;98;FALSE;Modulo OK;$R'

# Cambia campos string True y False por True y False Real (no se si es necesario)
# Une Fecha y hora en un solo campo
# inserta la referencia corta de 8 digitos despues de la fecha
# Devuelve una lista compuesa de listas de cada reguistro del PLC
def convertirCadena(cadenas, logger, nled):
    logger.debug('Conviertiendo cadena')
    cadenas = cadenas.split('\r')
    cadenas.pop()
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
        raise ValueError(f"No coinciden las lineas esperadas ({infoModelo[nled]['cRegObj']}) con las reales ({len(listaCadena)})")
        return False

###0,1,2,3,4,5,6,7 -> Mano IZQ (LED 1,2,3,4,5,6,7 y 8 Respectivamente)
###8,9,10,11,12,13,14,15 -> Mano DCH (LED 1,2,3,4,5,6,7 y 8 Respectivamente)

"""
(***REFERENCIAS***)
	IF Mano_Izq AND TD THEN
		Ref_Producto:='90158114';
		Descripcion:='CX482 LHD L';
		Modelo_produccion:=1;		(*Modelo enviado al robot*)
	ELSIF Mano_Drc AND TD THEN
		Ref_Producto:='90158113';
		Descripcion:='CX482 LHD R';
		Modelo_produccion:=2;		(*Modelo enviado al robot*)
	ELSIF Mano_Izq AND TI THEN
		Ref_Producto:='90158082';
		Descripcion:='CX482 RHD L';
		Modelo_produccion:=1;		(*Modelo enviado al robot*)
	ELSIF Mano_Drc AND TI THEN
		Ref_Producto:='90158080';
		Descripcion:='CX482 RHD R';
		Modelo_produccion:=2;		(*Modelo enviado al robot*)
	ELSIF Mano_Izq AND USA THEN
		Ref_Producto:='90158085';
		Descripcion:='CX482 USA L';
		Modelo_produccion:=1;		(*Modelo enviado al robot*)
	ELSIF Mano_Drc AND USA THEN
		Ref_Producto:='90158083';
		Descripcion:='CX482 USA R';
		Modelo_produccion:=2;		(*Modelo enviado al robot*)
	END_IF;
"""

### RELACION REFERENCIA CODIGO DE PROGRAMA
infoKeyence = {
    90158114 : {
        '000' : 'MANO IZQ LED 1',
        '001' : 'MANO IZQ LED 2', 
        '002' : 'MANO IZQ LED 3', 
        '003' : 'MANO IZQ LED 4',
        '004' : 'MANO IZQ LED 5', 
        '005' : 'MANO IZQ LED 6', 
        '006' : 'MANO IZQ LED 7', 
        '007' : 'MANO IZQ LED 8'
        },
    90158082 : {
        '000' : 'MANO IZQ LED 1',
        '001' : 'MANO IZQ LED 2', 
        '002' : 'MANO IZQ LED 3', 
        '003' : 'MANO IZQ LED 4',
        '004' : 'MANO IZQ LED 5', 
        '005' : 'MANO IZQ LED 6', 
        '006' : 'MANO IZQ LED 7', 
        '007' : 'MANO IZQ LED 8'
        },
    90158085 : {
        '000' : 'MANO IZQ LED 1',
        '001' : 'MANO IZQ LED 2', 
        '002' : 'MANO IZQ LED 3', 
        '003' : 'MANO IZQ LED 4',
        '004' : 'MANO IZQ LED 5', 
        '005' : 'MANO IZQ LED 6', 
        '006' : 'MANO IZQ LED 7', 
        '007' : 'MANO IZQ LED 8'
    },
    90158113 : {
        '008' : 'MANO DRCH LED 1',
        '009' : 'MANO DRCH LED 2',
        '010' : 'MANO DRCH LED 3',
        '011' : 'MANO DRCH LED 4',
        '012' : 'MANO DRCH LED 5',
        '013' : 'MANO DRCH LED 6',
        '014' : 'MANO DRCH LED 7',
        '015' : 'MANO DRCH LED 8'
    },
    90158080 : {
        '008' : 'MANO DRCH LED 1',
        '009' : 'MANO DRCH LED 2',
        '010' : 'MANO DRCH LED 3',
        '011' : 'MANO DRCH LED 4',
        '012' : 'MANO DRCH LED 5',
        '013' : 'MANO DRCH LED 6',
        '014' : 'MANO DRCH LED 7',
        '015' : 'MANO DRCH LED 8'
    },
    90158083 : {
        '008' : 'MANO DRCH LED 1',
        '009' : 'MANO DRCH LED 2',
        '010' : 'MANO DRCH LED 3',
        '011' : 'MANO DRCH LED 4',
        '012' : 'MANO DRCH LED 5',
        '013' : 'MANO DRCH LED 6',
        '014' : 'MANO DRCH LED 7',
        '015' : 'MANO DRCH LED 8'
    }
}


""" progKeyence = {
    90158114 : ['000', '001', '002', '003','004', '005', '006', '007'],
    90158082 : ['000', '001', '002', '003','004', '005', '006', '007'],
    90158085 : ['000', '001', '002', '003','004', '005', '006', '007'],
    90158113 : ['008', '009', '010', '011','012', '013', '014', '015'],
    90158080 : ['008', '009', '010', '011','012', '013', '014', '015'],
    90158083 : ['008', '009', '010', '011','012', '013', '014', '015']
            }

### PROGRAMA KEYENCE Y NOMBRE (SOLO SE USA PARA INFORMAR)
nombreProgKeyence = {
    '000' : 'MANO IZQ LED 1',
    '001' : 'MANO IZQ LED 2',
    '002' : 'MANO IZQ LED 3',
    '003' : 'MANO IZQ LED 4',
    '004' : 'MANO IZQ LED 5',
    '005' : 'MANO IZQ LED 6',
    '006' : 'MANO IZQ LED 7',
    '007' : 'MANO IZQ LED 8',
    '008' : 'MANO DRCH LED 1',
    '009' : 'MANO DRCH LED 2',
    '010' : 'MANO DRCH LED 3',
    '011' : 'MANO DRCH LED 4',
    '012' : 'MANO DRCH LED 5',
    '013' : 'MANO DRCH LED 6',
    '014' : 'MANO DRCH LED 7',
    '015' : 'MANO DRCH LED 8',
} """

# Listado de etapas por la que si pasa resetea variables y borra pantala
listaEtapasReseteo = [3,4,5,6,7,8,9]

# Nombre BBDD
# nombreBBDD = 'D:\\Python\\bbdd_CX482.db'
nombreBBDD = 'bbdd_CX482.db'

# consulta SQL de grabado
consultaGrabar = 'INSERT INTO datosInspeccion VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,\
     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,\
         ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,\
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, Null, Null, Null, Null, Null, Null, Null, Null, 0, 0)'

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
    Busqueda_L3 integer,
    Busqueda_OK_L3 BOOLEAN,
    Min_Ribbon_1_L3 integer,    
    Med_Ribbon_1_L3 integer,
    Min_Ribbon_2_L3 integer,
    Med_Ribbon_2_L3 integer,
    Val_oper_L3 BOOLEAN,
    Busqueda_L4 integer,
    Busqueda_OK_L4 BOOLEAN,
    Min_Ribbon_1_L4 integer,
    Med_Ribbon_1_L4 integer,
    Min_Ribbon_2_L4 integer,
    Med_Ribbon_2_L4 integer,
    Val_oper_L4 BOOLEAN,
    Busqueda_L5 integer,
    Busqueda_OK_L5 BOOLEAN,
    Min_Ribbon_1_L5 integer,    
    Med_Ribbon_1_L5 integer,
    Min_Ribbon_2_L5 integer,
    Med_Ribbon_2_L5 integer,
    Val_oper_L5 BOOLEAN,
    Busqueda_L6 integer,
    Busqueda_OK_L6 BOOLEAN,
    Min_Ribbon_1_L6 integer,
    Med_Ribbon_1_L6 integer,
    Min_Ribbon_2_L6 integer,
    Med_Ribbon_2_L6 integer,
    Val_oper_L6 BOOLEAN,
    Busqueda_L7 integer,
    Busqueda_OK_L7 BOOLEAN,
    Min_Ribbon_1_L7 integer,    
    Med_Ribbon_1_L7 integer,
    Min_Ribbon_2_L7 integer,
    Med_Ribbon_2_L7 integer,
    Val_oper_L7 BOOLEAN,
    Busqueda_L8 integer,
    Busqueda_OK_L8 BOOLEAN,
    Min_Ribbon_1_L8 integer,
    Med_Ribbon_1_L8 integer,
    Min_Ribbon_2_L8 integer,
    Med_Ribbon_2_L8 integer,
    Val_oper_L8 BOOLEAN,
    JuicioFinal text,
    NoKeyenceL1 integer,
    NombreKeyenceL1 text,
    FotoLed1 text,
    NoKeyenceL2 integer,
    NombreKeyenceL2 text,
    FotoLed2 text,
    NoKeyenceL3 integer,
    NombreKeyenceL3 text,
    FotoLed3 text,
    NoKeyenceL4 integer,
    NombreKeyenceL4 text,
    FotoLed4 text,
    NoKeyenceL5 integer,
    NombreKeyenceL5 text,
    FotoLed5 text,
    NoKeyenceL6 integer,
    NombreKeyenceL6 text,
    FotoLed6 text,
    NoKeyenceL7 integer,
    NombreKeyenceL7 text,
    FotoLed7 text,
    NoKeyenceL8 integer,
    NombreKeyenceL8 text,
    FotoLed8 text,
    linkDropboxFotoL1 text,
    linkDropboxFotoL2 text,
    linkDropboxFotoL3 text,
    linkDropboxFotoL4 text,
    linkDropboxFotoL5 text,
    linkDropboxFotoL6 text,
    linkDropboxFotoL7 text,
    linkDropboxFotoL8 text,
    syncGoogle BOOLEAN,
    syncSqlite_ext BOOLEAN
    )"""

# 94 columnas

# Campos de validacion operario (FKO's)
# Campo de validacion operario : campo de nombre de foto
camposValOper = {
    9 : 62,
    16 : 65,
    23 : 68,
    30 : 71,
    37 : 74,
    44 : 77,
    51 : 80,
    58 : 83
}