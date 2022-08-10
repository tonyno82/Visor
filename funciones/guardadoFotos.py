

#Q2
#['22/04/22 07:46:21', '90196987', '901969871DP02204220738##L3727757020861248ARA2200AA00006##', '87', True, '55', '100', '55', '100', False, '87', True, '55', '100', '55', '100', False, 'Modulo LB OK', '000', 'LED 1 LB IZQ 1', '00424_008_OK_22042022_163054.jpeg', '001', 'LED 2 LB IZQ 2', '00426_010_NG_22042022_163058.jpeg']
#['22/04/22 07:46:21', '90196989', '901969891DOW2204220733##L3727757320940135ARA1100AA00014##', '93', True, '55', '100', '55', '100', False, '88', True, '55', '100', '55', '100', False, 'Modulo HB OK', '002', 'LED 3 HB IZQ 1', '00425_009_OK_22042022_163056.jpeg', '003', 'LED 4 HB IZQ 2', '00427_011_OK_22042022_163213.jpeg']
#CX482
#['22/04/22 16:45:21', '90158113', '9015811391432204221628', '97', True, '50', '100', '50', '100', False, '91', True, '50', '100', '50', '93', False, '90', True, '50', '100', '50', '47', False, '94', True, '50', '100', '50', '100', False, '88', True, '50', '96', '50', '100', False, '81', True, '50', '100', '50', '100', False, '93', True, '50', '94', '50', '100', False, '96', True, '50', '97', '50', '100', False, 'Modulo KO', '008', 'MANO DRCH LED 1', '00424_008_OK_22042022_163054.jpeg', '009', 'MANO DRCH LED 2', '00425_009_OK_22042022_163056.jpeg', '010', 'MANO DRCH LED 3', '00426_010_NG_22042022_163058.jpeg', '011', 'MANO DRCH LED 4', '00427_011_OK_22042022_163213.jpeg', '012', 'MANO DRCH LED 5', '00428_012_OK_22042022_163216.jpeg', '013', 'MANO DRCH LED 6', '00429_013_OK_22042022_163217.jpeg', '014', 'MANO DRCH LED 7', '00430_014_OK_22042022_163220.jpeg', '015', 'MANO DRCH LED 8', '00431_015_OK_22042022_163222.jpeg']


import os
from pathlib import Path

import config_Prueba
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def guardarFoto(cadena, listaArchivosJPEG, nLed):
    listadoValoresFoto = {}
    inicial = 0
    for nled in range(0, nLed):
        inicial = 3 + (nled * 7)
        listadoValoresFoto[nled] = {}
        listadoValoresFoto[nled]['Busqueda de Forma'] = cadena[inicial]
        listadoValoresFoto[nled]['Busqueda OK?'] = cadena[inicial+1]
        listadoValoresFoto[nled]['Limite Ribbon 1'] = cadena[inicial+2]
        listadoValoresFoto[nled]['Valor leido Ribbon 1'] = cadena[inicial+3]
        listadoValoresFoto[nled]['Limite Ribbon 2'] = cadena[inicial+4]
        listadoValoresFoto[nled]['Valor leido Ribbon 2'] = cadena[inicial+5]
        listadoValoresFoto[nled]['Validado Operario?'] = cadena[inicial+6]
    inicial = inicial + 8
    for nled in range(0, nLed):
        inicialProg = inicial + (nled * 3)
        listadoValoresFoto[nled]['Nº Prog Keyence'] = cadena[inicialProg]
        listadoValoresFoto[nled]['Descripcion Prog Keyence'] = cadena[inicialProg+1]
        listadoValoresFoto[nled]['JPEG Foto'] = cadena[inicialProg+2]
        for n, archivo in enumerate(listaArchivosJPEG):
            if listadoValoresFoto[nled]['JPEG Foto'] == archivo.name:
                listadoValoresFoto[nled]['Ruta completa JPEG'] = archivo
                del listaArchivosJPEG[n]
    if len(listaArchivosJPEG) != 0:
        print(f'Han sobrado fotos ({len(listaArchivosJPEG)}) por colocar en el mosaico (listaArchivosJPEG != 0)')

    listaFotosMosaico = {}
    for nled in listadoValoresFoto:
        image = Image.open(listadoValoresFoto[nled]['Ruta completa JPEG'])
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 15)
        contador = 0
        for clave, valor in listadoValoresFoto[nled].items():
            if clave != 'Ruta completa JPEG':
                draw.text((0, contador), f"{clave} = {valor}", font=font, fill="black")
                contador += 15
        listaFotosMosaico[nled] = image
    
    ahora = datetime.now()
    ahora = ahora.strftime('%d-%m-%Y_%H%M%S_')

    if len(listaFotosMosaico) == 2:
        x, y = listaFotosMosaico[0].size
        image =  Image.new("RGB", (x*2, y), "white")
        numeroImagen = 0
        for nimage in listaFotosMosaico:
            posicionX = numeroImagen*x
            image.paste(listaFotosMosaico[nimage], (posicionX,0))
            numeroImagen += 1
        nombreArchivo = ahora + cadena[1] + ' ' + cadena[17] + '.jpeg'
        image.save(nombreArchivo)
        return nombreArchivo


    elif len(listaFotosMosaico) == 8:
        x, y = listaFotosMosaico[0].size
        image =  Image.new("RGB", (x*3, y*3), "white")
        numeroImagen = 1
        for nimage in listaFotosMosaico:
            if numeroImagen <= 3:
                posicionX = (numeroImagen-1)*x
                image.paste(listaFotosMosaico[nimage], (posicionX,0))
                numeroImagen += 1
            elif numeroImagen <= 6:
                posicionX = (numeroImagen - 4)*x
                image.paste(listaFotosMosaico[nimage], (posicionX,y))
                numeroImagen += 1
            elif numeroImagen <= 9:
                posicionX = (numeroImagen - 7)*x
                image.paste(listaFotosMosaico[nimage], (posicionX,y*2))
                numeroImagen += 1
        nombreArchivo = ahora + cadena[1] + ' ' + cadena[59] + '.jpeg'
        image.save(nombreArchivo)
        return nombreArchivo
    else:
        print(f'ERROR, cantidad de fotos ({len(listaFotosMosaico)}) no configurada para hacer mosaico')
        return False



            

if __name__ == '__main__':
    cadenaCompleta = ['22/04/22 16:45:21', '90158113', '9015811391432204221628', '85', True, '50', '25', '50', '35', True, '91', True, '50', '100', '50', '93', False, '90', True, '50', '100', '50', '47', False, '94', True, '50', '100', '50', '100', False, '88', True, '50', '96', '50', '100', False, '81', True, '50', '100', '50', '100', False, '93', True, '50', '94', '50', '100', False, '96', True, '50', '97', '50', '100', False, 'Modulo KO', '008', 'MANO DRCH LED 1', '00424_008_OK_22042022_163054.jpeg', '009', 'MANO DRCH LED 2', '00425_009_OK_22042022_163056.jpeg', '010', 'MANO DRCH LED 3', '00426_010_NG_22042022_163058.jpeg', '011', 'MANO DRCH LED 4', '00427_011_OK_22042022_163213.jpeg', '012', 'MANO DRCH LED 5', '00428_012_OK_22042022_163216.jpeg', '013', 'MANO DRCH LED 6', '00429_013_OK_22042022_163217.jpeg', '014', 'MANO DRCH LED 7', '00430_014_OK_22042022_163220.jpeg', '015', 'MANO DRCH LED 8', '00431_015_OK_22042022_163222.jpeg']
    #cadenaCompleta = ['22/04/22 07:46:21', '90196987', '901969871DP02204220738##L3727757020861248ARA2200AA00006##', '65', True, '55', '15', '55', '125', False, '87', True, '55', '100', '55', '100', False, 'Modulo LB OK', '000', 'LED 1 LB IZQ 1', '00424_008_OK_22042022_163054.jpeg', '001', 'LED 2 LB IZQ 2', '00426_010_NG_22042022_163058.jpeg']
    #for a, b in enumerate(cadenaCompleta):
        #print(f'{a} - {b}')


    ruta = Path(r'C:\Users\tonyno\Qsync\9 Python\Programas\GitHub_VisorImagenesQ2\VisorImagenesQ2\Reestructuracion VISOR\Fotos_Prueba')
    listaArchivosCreados = sorted(list(ruta.glob('*.jpeg'))) 

    listado = guardarFoto(cadenaCompleta,listaArchivosCreados, 8)
    print(listado)



