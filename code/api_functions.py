# Conjunto de funciones de soporte

def obtener_mes_dos_digitos(mes_en_espanol: str) -> str:
    '''Recibe un nombre de mes en espanol y devuelve un string de dos posiciones
    indicando el numero de mes. En caso en que el nombre del mes no exista, devuelve 00'''

    meses = {'enero' : '01', 'ene' : '01',
             'febrero' : '02', 'feb' : '02',
             'marzo' : '03', 'mar' : '03',
             'abril' : '04', 'abr' : '04',
             'mayo' : '05', 'may' : '05',
             'junio' : '06', 'jun' : '06',
             'julio' : '07', 'jul' : '07',
             'agosto' : '08', 'ago' : '08',
             'setiembre' : '09', 'septiembre' : '09', 'set' : '09', 'sep' : '09',
             'octubre' : '10', 'oct' : '10',
             'noviembre' : '11', 'nov' : '11',
             'diciembre' : '12', 'dic' : '12'}
    mes_dos_digitos = "00"
    mes_en_espanol = mes_en_espanol.lower()
    if mes_en_espanol in meses.keys():
        mes_dos_digitos = meses[mes_en_espanol]
    return mes_dos_digitos

def obtener_dia_ingles(dia_en_espanol: str):
    '''Recibe un nombre de dia en espanol y devuelve un string con el nombre del dia en ingles
    En caso en que el nombre del dia no exista, devuelve "None"'''

    dias = {'lunes' : 'Monday',
            'martes' : 'Tuesday',
            'miercoles' : 'Wednesday', 'miércoles' : 'Wednesday',
            'jueves' : 'Thursday',
            'viernes' : 'Friday',
            'sabado' : 'Saturday', 'sábado' : 'Saturday',
            'domingo' : 'Sunday'}
    
    dia_en_ingles = "None"
    dia_en_espanol = dia_en_espanol.lower()
    if dia_en_espanol in dias.keys():
        dia_en_ingles = dias[dia_en_espanol]
    return dia_en_ingles

