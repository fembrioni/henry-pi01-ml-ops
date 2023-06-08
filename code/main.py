# Este es el archivo principal de procesamiento del proyecto
# PI01-MLOPS de Henry

# Imports
import os
import pandas as pd
from fastapi import FastAPI
import uvicorn
import etl_flow as etlflow
import api_functions as apif

# Declaro la App de FastAPI
fastAPIApp = FastAPI()

# Si estoy en el ambiente de desarrollo, preproceso los dataframes (ETL)
# En produccion simplemente utilizo los archivos ya preprocesados
# Esto es para evitar problemas de memoria con Render
ambiente = os.getenv("AMBIENTE")
if ambiente = 'DEV':
    etlflow.preprocesar_credits_dataframes()
    etlflow.preprocesar_dataframes()

# Endpoints

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
        m_df = etlflow.obtener_df_preprocesado('m_df')
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
        m_df = etlflow.obtener_df_preprocesado('m_df')
        q = m_df[m_df['release_day_of_week'] == dia_ingles].release_day_of_week.count()
        return '{} cantidad de películas fueron estrenadas en los dias {}'.format(str(q), dia)

# Endpoint 3
@fastAPIApp.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
    Ejemplo de retorno: La película X fue estrenada en el año X con un score/popularidad de X
    Se asume: 
     a) el título será ingresado completo
     b) el score se corresponde con el campo popularity'''

    # Evaluo la cantidad de registros con ese nombre de pelicula
    m_df = etlflow.obtener_df_preprocesado('m_df')
    q = m_df[m_df['title'] == titulo_de_la_filmacion].title.count()

    # Si no hay registros se informa tal situacion
    if q < 1:
        return 'No se encuentran registros con el siguiente nombre de filmación: {}'.format(titulo_de_la_filmacion)
    else:
        # Existe al menos un registro. Me quedo con el primero de ellos
        registros = m_df[m_df['title'] == titulo_de_la_filmacion]
        registro = registros.head(1)

        # Obtengo los valores de release_year y popularity
        release_year = registro['release_year'].values[0]
        popularity = registro['popularity'].values[0]

        # Respondo
        return 'La película {} fue estrenada en el año {} con un score/popularidad de {}'\
            .format(titulo_de_la_filmacion, release_year, popularity)

if __name__ == "__main__":
    uvicorn.run(fastAPIApp, host="0.0.0.0", port=8000)