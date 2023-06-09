# Este es el archivo principal de procesamiento del proyecto
# PI01-MLOPS de Henry

# Imports
import os
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import etl_flow as etlflow
import api_functions as apif

# Declaro la App de FastAPI
fastAPIApp = FastAPI()

# Si estoy en el ambiente de desarrollo, preproceso los dataframes (ETL)
# En produccion simplemente utilizo los archivos ya preprocesados
# Esto es para evitar problemas de memoria con Render
ambiente = os.getenv("AMBIENTE")
if ambiente == 'DEV':
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
        q = m_df[m_df['release_month'] == int(mes_num)].release_month.count()
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
    
# Endpoint 4
@fastAPIApp.get("/votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion):
    '''Se ingresa el título de una filmación esperando como respuesta
    el título, la cantidad de votos y el valor promedio de las votaciones.
    La misma variable deberá de contar con al menos 2000 valoraciones,
    caso contrario, debemos contar con un mensaje avisando que no cumple
    esta condición y que por ende, no se devuelve ningun valor.

    Ejemplo de retorno: La película X fue estrenada en el año X. La misma
    cuenta con un total de X valoraciones, con un promedio de X
    
    SUPUESTO DE TRABAJO: Dado que la informacion de año de estreno no se solicita, no se emitirá'''

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

        # Obtengo los valores de cantidad de votos
        cant_votos = registro['vote_count'].values[0]

        # Si la cantidad de votos no alcanza, emito un mensaje avisando de esa situacion
        if cant_votos < 2000:
            return 'La cantidad de votos es menor a 2000, por lo que no se emite la valoracion promedio'
        else:
            # Obtengo el promedio de las valoraciones
            prom_votos = registro['vote_average'].values[0]

            # Respondo
            return 'La película {} cuenta con un total de {} valoraciones, con un promedio de {}'\
                .format(titulo_de_la_filmacion, cant_votos, prom_votos)

# Endpoint 5
@fastAPIApp.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor):
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset
    debiendo devolver el éxito del mismo medido a través del retorno.
    Además, la cantidad de películas en las que ha participado y el promedio
    de retorno. La definición no deberá considerar directores.
    
    Ejemplo de retorno: El actor X ha participado de X cantidad de filmaciones,
    el mismo ha conseguido un retorno de X con un promedio de X por filmación'''

    # Evaluo la cantidad de registros con ese nombre de actor
    m_cast_df = etlflow.obtener_df_preprocesado('m_cast_df')
    q = m_cast_df[m_cast_df['actor_actress_name'] == nombre_actor].actor_actress_name.count()

    # Si no hay registros se informa tal situacion
    if q < 1:
        return 'No se encuentran registros con el siguiente nombre de actor/actriz: {}'.format(nombre_actor)
    else:
        # Uso los registros del actor/atriz para joinearlos con los datos de las peliculas
        m_cast_df = m_cast_df[m_cast_df['actor_actress_name'] == nombre_actor]
        m_df = etlflow.obtener_df_preprocesado('m_df')
        m_join = pd.merge(left=m_cast_df, right=m_df, on='id', how='inner')
        del m_cast_df
        del m_df

        # calculo la informacion solicitada
        retorno = m_join['return'].sum()
        cant_peliculas = m_join['id'].count()
        prom_retorno = retorno / cant_peliculas

        # Respondo
        return 'El actor/actriz {} ha participado en {} filmaciones, el mismo ha conseguido un retorno de {} con un promedio de {} por filmación'\
        .format(nombre_actor, cant_peliculas, retorno, prom_retorno)

# Endpoint 6
@fastAPIApp.get("/get_director/{nombre_director}")
def get_director(nombre_director):
    '''Se ingresa el nombre de un director que se encuentre dentro de un dataset
    debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá
    devolver el nombre de cada película con la fecha de lanzamiento, retorno
    individual, costo y ganancia de la misma.'''

    # Evaluo la cantidad de registros con ese nombre de director
    m_crew_df = etlflow.obtener_df_preprocesado('m_crew_job_and_name_df')
    q = m_crew_df[m_crew_df['name'] == nombre_director].name.count()

    # Si no hay registros se informa tal situacion
    if q < 1:
        return 'No se encuentran registros con el siguiente nombre de director(a): {}'.format(nombre_director)
    else:
        # Uso los registros del director para joinearlos con los datos de las peliculas
        m_crew_df = m_crew_df[m_crew_df['name'] == nombre_director]
        m_df = etlflow.obtener_df_preprocesado('m_df')
        m_join = pd.merge(left=m_crew_df, right=m_df, on='id', how='inner')

        # calculo la informacion solicitada
        retorno_director = m_join['return'].sum()

        # Preparo la respuesta
        rta = '''<head>
                    <style>
                        table {
                        table-layout: fixed;
                        width: 100%;
                        }
                        
                        td {
                        width: 20%
                        }
                    </style>
                </head>
                <body>'''
        rta = rta + '''El/la director(a) {} tiene un retorno de {} según la siguiente lista de películas:<br><br>'''\
                .format(nombre_director, retorno_director)
        rta = rta + '''<table><tr><td>Film</td><td>Fecha lanz</td><td>Retorno</td><td>Costo</td><td>Ganancia</td></tr>'''
        for idx, row in m_join.iterrows():
            rta = rta + '''<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'''\
            .format(row['title'], row['release_date'], row['return'], row['budget'], row['revenue'])
        rta = rta + '''</table></body>'''

        # Respondo con HTMLResponse para poder incluir controles HTML de fin de linea y otros formatos
        return HTMLResponse(content=rta)

if __name__ == "__main__":
    uvicorn.run(fastAPIApp, host="0.0.0.0", port=8000)