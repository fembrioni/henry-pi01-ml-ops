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
import ml_model_generator as mlmodel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Declaro la App de FastAPI
fastAPIApp = FastAPI()

# Si estoy en el ambiente de desarrollo, preproceso los dataframes (ETL)
# En produccion simplemente utilizo los archivos ya preprocesados
# Esto es para evitar problemas de memoria con Render
ambiente = os.getenv("AMBIENTE")
if ambiente == 'DEV':
    etlflow.preprocesar_credits_dataframes()
    etlflow.preprocesar_dataframes()

# Proceso el Modelo de Machine Learning
mlmodel.generar_modelo()

# Endpoints
#  1 - /cantidad_filmaciones_mes/{mes}
#  2 - /cantidad_filmaciones_dia/{dia}
#  3 - /score_titulo/{titulo_de_la_filmacion}
#  4 - /votos_titulo/{titulo_de_la_filmacion}
#  5 - /get_actor/{nombre_actor}
#  6 - /get_director/{nombre_director}
# ML - /recomendacion/{titulo}

# Health check
@fastAPIApp.get("/health_check")
def health_check():
    return HTMLResponse(content=None, status_code=204)

# Endpoint 1
@fastAPIApp.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    '''Se ingresa un mes en idioma Español.
    Devuelve la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.
    Ejemplo de retorno: X cantidad de películas fueron estrenadas en el mes de X
    El viernes 9/6 pidieron return {'mes':mes, 'cantidad':respuesta}'''

    # Valido el nombre del mes y obtengo su representacion de dos digitos
    mes_num = apif.obtener_mes_dos_digitos(mes_en_espanol=mes)

    # Si el mes no es valido devuelvo un mensaje de error
    if mes_num == '00':
        return 'El nombre de mes ingresado: {} no es valido'.format(mes)
    else:
        # Devuelvo la cantidad de peliculas que fueron estrenadas en ese mes
        m_df = etlflow.obtener_df_preprocesado('m_df')
        q = m_df[m_df['release_month'] == int(mes_num)].release_month.count()
        respuesta = {'mes' : mes, 'cantidad' : str(q)}
        return respuesta

# Endpoint 2
@fastAPIApp.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    '''Se ingresa un día en idioma Español. Devuelve la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.
    Ejemplo de retorno: X cantidad de películas fueron estrenadas en los días X
    El viernes 9/6 pidieron return {'dia':dia, 'cantidad':respuesta}'''

    # Valido el nombre del dia y obtengo su representacion en ingles
    dia_ingles = apif.obtener_dia_ingles(dia_en_espanol=dia)

    # Si el dia no es valido devuelvo un mensaje de error
    if dia_ingles == 'None':
        return 'El nombre de dia ingresado: {} no es valido'.format(dia)
    else:
        # Devuelvo la cantidad de peliculas que fueron estrenadas ese dia
        m_df = etlflow.obtener_df_preprocesado('m_df')
        q = m_df[m_df['release_day_of_week'] == dia_ingles].release_day_of_week.count()
        respuesta = {'dia' : dia, 'cantidad' : str(q)}
        return respuesta

# Endpoint 3
@fastAPIApp.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
    Ejemplo de retorno: La película X fue estrenada en el año X con un score/popularidad de X
    Se asume: 
     a) el título será ingresado completo
     b) el score se corresponde con el campo popularity
     
    El 9/6 pidieron return {'titulo':titulo, 'anio':respuesta, 'popularidad':respuesta}'''

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
        respuesta = {'titulo' : titulo_de_la_filmacion, 'anio' : str(release_year), 'popularidad' : str(popularity)}
        return respuesta
    
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
    
    El 9/6 pidieron return {'titulo':titulo, 'anio':respuesta, 'voto_total':respuesta, 'voto_promedio':respuesta}'''

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
            # Obtengo el año de estreno y el promedio de las valoraciones
            release_year = registro['release_year'].values[0]
            prom_votos = registro['vote_average'].values[0]

            # Respondo
            respuesta = {'titulo' : titulo_de_la_filmacion,\
                 'anio' : str(release_year),\
                 'voto_total' : str(cant_votos),\
                 'voto_promedio' : str(prom_votos)}
            return respuesta

# Endpoint 5
@fastAPIApp.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor):
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset
    debiendo devolver el éxito del mismo medido a través del retorno.
    Además, la cantidad de películas en las que ha participado y el promedio
    de retorno. La definición no deberá considerar directores.
    
    Ejemplo de retorno: El actor X ha participado de X cantidad de filmaciones,
    el mismo ha conseguido un retorno de X con un promedio de X por filmación
    
    El 9/6 pidieron return {'actor':nombre_actor, 'cantidad_filmaciones':respuesta, 'retorno_total':respuesta, 'retorno_promedio':respuesta}'''

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
        respuesta = {'actor' : nombre_actor,\
            'cantidad_filmaciones' : str(cant_peliculas),\
            'retorno_total' : str(retorno),\
            'retorno_promedio' : str(prom_retorno)}
        return respuesta

# Endpoint 6
@fastAPIApp.get("/get_director/{nombre_director}")
def get_director(nombre_director):
    '''Se ingresa el nombre de un director que se encuentre dentro de un dataset
    debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá
    devolver el nombre de cada película con la fecha de lanzamiento, retorno
    individual, costo y ganancia de la misma.
    
    El 9/6 pidieron return {'director':nombre_director, 'retorno_total_director':respuesta, 
    'peliculas':respuesta, 'anio':respuesta,, 'retorno_pelicula':respuesta, 
    'budget_pelicula':respuesta, 'revenue_pelicula':respuesta}'''

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
        retorno_director = m_join['return'].mean()

        # Preparo la respuesta
        rta = {'director' : None,\
               'retorno_total_director' : None,\
               'peliculas' : None,\
               'anio' : None,\
               'retorno_pelicula' : None,\
               'budget_pelicula' : None,\
               'revenue_pelicula' : None}
        rta['director'] = nombre_director
        rta['retorno_total_director'] = str(retorno_director)

        lista_peliculas = []
        lista_anio = []
        lista_ret_pelicula = []
        lista_budget_pelicula = []
        lista_rev_pelicula = []
        for idx, row in m_join.iterrows():
            lista_peliculas.append(row['title'])
            lista_anio.append(str(row['release_date']))
            lista_ret_pelicula.append(str(row['return']))
            lista_budget_pelicula.append(str(row['budget']))
            lista_rev_pelicula.append(str(row['revenue']))
        rta['peliculas'] = lista_peliculas
        rta['anio'] = lista_anio
        rta['retorno_pelicula'] = lista_ret_pelicula
        rta['budget_pelicula'] = lista_budget_pelicula
        rta['revenue_pelicula'] = lista_rev_pelicula

        # Respondo
        return rta

# Endpoint 7 - recomendacion ML
@fastAPIApp.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    # El 9/6 pidieron return {'lista recomendada': respuesta}

    # Evaluo la cantidad de registros con ese nombre de pelicula
    m_df = etlflow.obtener_df_preprocesado('m_df')
    q = m_df[m_df['title'] == titulo].title.count()

    # Si no hay registros se informa tal situacion
    if q < 1:
        return 'No se encuentran registros con el siguiente nombre de filmación: {}'.format(titulo)
    else:
        # Existe al menos un registro. Me quedo con el primero de ellos
        registros = m_df[m_df['title'] == titulo]
        registro = registros.head(1)
        idx_pelicula_consultada = registro.index.values[0]

        # Recupero el vectorizador entrenado y la matriz TFIDF para realizar las recomendaciones
        tfidf_vectorizer = mlmodel.deserealizar('vec_tfidf')
        mtx_tfidf = mlmodel.deserealizar('mtx_tfidf')

        # Elijo el titulo de este film como query document
        query_document = registro['overview'].values[0]

        # Sobre la base de la matriz TFIDF busco los indices de documentos similares
        query_tfidf = tfidf_vectorizer.transform([query_document])
        similarity_scores = cosine_similarity(query_tfidf, mtx_tfidf)
        similarity_scores = similarity_scores.flatten()  # Convierto a un 1D array
        related_documents_indices = similarity_scores.argsort()[::-1]  # Ordeno los indices por orden descendente

        # Preparo la respuesta
        rta = {'lista recomendada' : None}
        lista_recom = []
        top_titulos = 5
        for idx_label in related_documents_indices:
            if idx_label != idx_pelicula_consultada:
                lista_recom.append(m_df.loc[idx_label].title)
                top_titulos = top_titulos - 1
                if top_titulos < 1:
                    break
        rta['lista recomendada'] = lista_recom

        # Respondo
        return rta

if __name__ == "__main__":
    uvicorn.run(fastAPIApp, host="0.0.0.0", port=8000)