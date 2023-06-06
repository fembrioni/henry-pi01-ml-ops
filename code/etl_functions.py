# Archivo python con las funciones utilizadas en el ETL

import json
import ast

def obtener_dicc(cadena_json) -> dict:
    '''Esta funcion permite obtener un diccionario que se corresponde con la cadena json enviada como valor'''

    # El siguiente diccionario se utiliza para reemplazar caracteres que
    # pudieran confundirse con un fin de texto
    replacement_dict = {
        "'s" : "s",
        "Nuke 'Em" : "Nuke Em",
        "Breakin' Collection" : "Breakin Collection",
        "Happily N'Ever" : "Happily N Ever",
        "Smokin' Aces" : "Smokin Aces",
        "Puss 'n" : "Puss n",
        "Les Mystères de l'o" : "Les Mysteres de l o",
        "Manuale d'amore" : "Manuale d amore",
        "We're" : "We re",
        "China O'Brien" : "China O Brien",
        "Don't" : "Dont",
        "n' Angels" : "n Angels",
        "L'allenatore" : "L allenatore",
        "Spirits' Home" : "Spirits Home",
        ": None" : ": 'None'"
    }

    casos_especiales = ['0.065736', '1.931659', '2.185485']

    if cadena_json in casos_especiales:
        return json.loads('{}')
    elif type(cadena_json) == float: # La celda es un nan
        return json.loads('{}')
    else:
        cadena = cadena_json
        for dict_key in replacement_dict.keys():
            if dict_key in cadena:
                cadena = cadena.replace(dict_key, replacement_dict[dict_key])
        cadena = cadena.replace("\"", "\'")
        cadena = cadena.replace("\'", "\"")
        return json.loads(cadena)

def obtener_valor(diccionario: dict, clave: str, none_como_string_vacio=True):
    '''Esta funcion permite recuperar el valor de la clave en el diccionario'''
    if len(diccionario.keys()) == 0:
        if none_como_string_vacio:
            return ''
        else:
            return None
    else:
        if clave in diccionario.keys():
            return diccionario[clave]
        else:
            if none_como_string_vacio:
                return ''
            else:
                return None

def obtener_valores(lista: str, clave: str, none_como_string_vacio=True, separador=', '):
    '''Esta funcion permite recuperar los valores de un string que encapsula una lista de diccionarios'''
    lista = ast.literal_eval(lista)
    if type(lista) != list:
        if none_como_string_vacio:
            return ''
        else:
            return None
    elif len(lista) == 0:
        if none_como_string_vacio:
            return ''
        else:
            return None
    else:
        salida = []
        for d in lista:
            salida.append(obtener_valor(diccionario=d, clave=clave, none_como_string_vacio=none_como_string_vacio))
        return separador.join(salida)

if __name__ == '__main__':
    # Testeo las funciones

    # test obtener_dicc(cadena_json)
    cadena_json = "{'id': 10194, 'name': 'Toy Story Collection', 'poster_path': '/7G9915LfUQ2lVfwMEEhDsn3kT4B.jpg', 'backdrop_path': '/9FBwqcd9IRruEDUrTdcaafOMKUq.jpg'}"
    dicc = obtener_dicc(cadena_json)
    print(dicc['name'], dicc['id'])
