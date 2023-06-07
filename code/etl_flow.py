# Este es el archivo principal de flow del ETL
# Se procesan dos archivos de origen:
# /com.docker.devenvironments.code/src/movies_dataset.csv
# /com.docker.devenvironments.code/src/credits.csv

# Imports
import numpy as np
import pandas as pd
import etl_functions as etlf

def obtener_dataframes() -> dict:

       # Movies
       # ======
       movies_df = pd.read_csv('/com.docker.devenvironments.code/src/movies_dataset.csv')

       # Me quedo con las columnas utiles segun el criterio de evaluacion
       columns_to_store = ['belongs_to_collection', 'budget', 'genres', 'id',
              'original_language', 'overview',
              'popularity', 'production_companies',
              'production_countries', 'release_date', 'revenue', 'runtime',
              'spoken_languages', 'status', 'tagline', 'title',
              'vote_average', 'vote_count']
       m_df = movies_df[columns_to_store]

       # Drops de registros
       m_df.dropna(subset=['production_companies'], inplace=True)
       m_df.dropna(subset=['spoken_languages'], inplace=True)
       m_df.dropna(subset=['release_date'], inplace=True)

       # Validaciones en el EDA
       # release_date (luego de eliminar los nulos) tiene el formato necesario YYYY-mm-dd. No es necesario hacer modificaciones
       # revenue y budget no tienen nulos

       # Tratamiento columna release_year
       m_df['release_year'] = m_df['release_date'].apply(lambda x: x[0:4])

       # Tratamiento columna release_month (La creo para cumplir con el Endpoint 1)
       m_df['release_month'] = m_df['release_date'].apply(lambda x: x[5:7])

       # Tratamiento columna release_day (La creo para cumplir con el Endpoint 2)
       m_df['release_day_of_week'] = m_df['release_date'].apply(etlf.obtener_dia_de_la_semana)

       # Tratamiento columna return
       m_df['budget'] = m_df['budget'].astype('float64')
       m_df['return'] = m_df['revenue'] / m_df['budget']
       m_df['return'] = m_df['return'].fillna(0)
       m_df['return'] = m_df['return'].replace(np.inf, 0)

       # Tratamiento columna belongs_to_collection
       m_df['collection'] = m_df['belongs_to_collection'].apply(etlf.obtener_dicc)
       m_df['collection_name'] = m_df['collection'].apply(etlf.obtener_valor, args=('name',))

       # Tratamiento columna genres. Genero un nuevo dataframe con los generos expandidos y el id para hacer join
       m_df['genres_names'] = m_df['genres'].apply(etlf.obtener_valores, args=('name',))
       m_genres_df = m_df[['id', 'genres_names']]
       df_expanded = m_genres_df['genres_names'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('genre_name')
       m_genres_df = m_genres_df.join(df_expanded)
       m_genres_df.drop(columns=['genres_names'], inplace=True)

       # Tratamiento columna production_companies. Genero un nuevo dataframe con las companias expandidas y el id para hacer join
       m_df['companies_names'] = m_df['production_companies'].apply(etlf.obtener_valores, args=('name',))
       m_companies_df = m_df[['id', 'companies_names']]
       df_expanded = m_companies_df['companies_names'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('company_name')
       m_companies_df = m_companies_df.join(df_expanded)
       m_companies_df.drop(columns=['companies_names'], inplace=True)

       # Tratamiento columna production_countries. Genero un nuevo dataframe con los paises expandidos y el id para hacer join
       m_df['countries_names'] = m_df['production_countries'].apply(etlf.obtener_valores, args=('name',))
       m_countries_df = m_df[['id', 'countries_names']]
       df_expanded = m_countries_df['countries_names'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('country_name')
       m_countries_df = m_countries_df.join(df_expanded)
       m_countries_df.drop(columns=['countries_names'], inplace=True)

       # Tratamiento columna spoken_languages. Genero un nuevo dataframe con los idiomas expandidos y el id para hacer join
       m_df['languages_names'] = m_df['spoken_languages'].apply(etlf.obtener_valores, args=('name',))
       m_languages_df = m_df[['id', 'languages_names']]
       df_expanded = m_languages_df['languages_names'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('language_name')
       m_languages_df = m_languages_df.join(df_expanded)
       m_languages_df.drop(columns=['languages_names'], inplace=True)

       # Convierto la columna id a entero para poder hacer join con el dataset de credits
       m_df['id'] = m_df['id'].astype(int)

       # Hago drop de las columnas del movies dataframe que no utilizare
       m_df.drop(columns=['belongs_to_collection', 'collection',
                     'genres', 'genres_names',
                     'production_companies', 'companies_names',
                     'production_countries', 'countries_names',
                     'spoken_languages', 'languages_names'], inplace=True)

       # Credits
       # =======
       credits_df = pd.read_csv('/com.docker.devenvironments.code/src/credits.csv')

       # Tratamiento columna cast. Genero un nuevo dataframe con los actores/actrices expandidos y el id para hacer join
       credits_df['cast_names'] = credits_df['cast'].apply(etlf.obtener_valores, args=('name',))
       m_cast_df = credits_df[['id', 'cast_names']]
       df_expanded = m_cast_df['cast_names'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('actor_actress_name')
       m_cast_df = m_cast_df.join(df_expanded)
       m_cast_df.drop(columns=['cast_names'], inplace=True)

       # Tratamiento columna crew. Genero un nuevo dataframe con id (Para hacer join), nombre del trabajo y nombre de la persona
       credits_df['jobs_and_names'] = credits_df['crew'].apply(etlf.obtener_cargo_y_nombre)
       m_crew_job_and_name_df = credits_df[['id', 'jobs_and_names']]
       df_expanded = m_crew_job_and_name_df['jobs_and_names'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('job_and_name')
       m_crew_job_and_name_df = m_crew_job_and_name_df.join(df_expanded)
       m_crew_job_and_name_df.drop(columns=['jobs_and_names'], inplace=True)
       m_crew_job_and_name_df[['job', 'name']] = m_crew_job_and_name_df['job_and_name'].str.split(':-:', expand=True)
       m_crew_job_and_name_df.drop(columns=['job_and_name'], inplace=True)

       # RESUMEN
       # =======
       # Los dataframes del modelo son
       #                   m_df : Es el dataframe principal de movies (Clave id)
       #            m_genres_df : Es el dataframe de generos de cada pelicula (Clave id)
       #         m_companies_df : Es el dataframe de companias que producen cada pelicula (Clave id)
       #         m_countries_df : Es el dataframe de paises que producen cada pelicula (Clave id)
       #         m_languages_df : Es el dataframe de idiomas hablados en cada pelicula (Clave id)
       #              m_cast_df : Es el dataframe de actores y actrices en cada pelicula (Clave id)
       # m_crew_job_and_name_df : Es el dataframe de trabajos del reparto en cada pelicula (Clave id)

       # Devuelvo un diccionario con los dataframes
       dataframes_d = {'m_df' : m_df,
                       'm_genres_df' : m_genres_df,
                       'm_companies_df' : m_companies_df,
                       'm_countries_df' : m_countries_df,
                       'm_languages_df' : m_languages_df,
                       'm_cast_df' : m_cast_df,
                       'm_crew_job_and_name_df' : m_crew_job_and_name_df}
       
       return dataframes_d
