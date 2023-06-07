# Este es el archivo principal de procesamiento del proyecto
# PI01-MLOPS de Henry

# Imports
import pandas as pd
from fastapi import FastAPI
import uvicorn
import etl_flow as etlf
import api_functions as apif

# Declaro la App de FastAPI
fastAPIApp = FastAPI()

# Obtengo los dataframes procesados luego del ETL
dataframes_d = etlf.obtener_dataframes()

# Endpoints

# Endpoint de prueba
@fastAPIApp.get("/inicio")
async def ruta_prueba():
    return "Hola"

# Endpoint 1
@fastAPIApp.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    '''Se ingresa un mes en idioma Español.
    Devuelve la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.
    Ejemplo de retorno: X cantidad de películas fueron estrenadas en el mes de X'''

    # Valido el nombre del mes y obtengo su representacion de dos digitos
    mes_num = apif.obtener_mes_dos_digitos(mes_en_espanol=mes)

    # Si el mes no es valido devuelvo un mensaje de error
    if mes_num == '00':
        return 'El nombre de mes ingresado: {} no es valido'.format(mes)
    else:
        # Devuelvo la cantidad de peliculas que fueron estrenadas en ese mes
        m_df = dataframes_d['m_df']
        q = m_df[m_df['release_month'] == mes_num].release_month.count()
        return '{} cantidad de películas fueron estrenadas en el mes de {}'.format(str(q), mes)

# Endpoint 2
@fastAPIApp.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    '''Se ingresa un día en idioma Español. Devuelve la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.
    Ejemplo de retorno: X cantidad de películas fueron estrenadas en los días X'''

    # Valido el nombre del dia y obtengo su representacion en ingles
    dia_ingles = apif.obtener_dia_ingles(dia_en_espanol=dia)

    # Si el dia no es valido devuelvo un mensaje de error
    if dia_ingles == 'None':
        return 'El nombre de dia ingresado: {} no es valido'.format(dia)
    else:
        # Devuelvo la cantidad de peliculas que fueron estrenadas ese dia
        m_df = dataframes_d['m_df']
        q = m_df[m_df['release_day_of_week'] == dia_ingles].release_day_of_week.count()
        return '{} cantidad de películas fueron estrenadas en los dias {}'.format(str(q), dia)

if __name__ == "__main__":
    uvicorn.run(fastAPIApp, host="0.0.0.0", port=8000)