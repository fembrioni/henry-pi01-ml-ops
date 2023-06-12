# Este es el programa donde se define y procesa el modelo de recomendación,
# sobre la base del uso de la similaridad coseno
# El mismo deja escrita la serializacion de una matriz de TFIDF en el archivo
# ./src/preproc/mtx_tfidf.ser que luego puede ser cargada para dar soporte a
# una API de recomendacion

# Imports
import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download("stopwords")
import etl_flow as etlflow
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

# Funciones de preprocesamiento

# Elimina signos de puntuacion de una lista tokenizada
def limpia_signos_de_puntuacion(lista_tokens: list):
    token_rta = []
    for palabra in lista_tokens:
        for letra in palabra:
            if letra in string.punctuation:
                palabra=palabra.replace(letra,"")
        token_rta.append(palabra)
    return token_rta

# Elimina numeros
def limpia_numeros(lista_tokens: list):
    token_rta = []
    for palabra in lista_tokens:
        for letra in palabra:
            if letra in string.digits:
                palabra=palabra.replace(letra,"")
        token_rta.append(palabra)
    return token_rta

# Elimina tokens vacios
def elimina_tokens_vacios(lista_tokens: list):
    token_rta = []
    for palabra in lista_tokens:
        if palabra != "":
            token_rta.append(palabra)
    return token_rta

# Pasa los tokens a minusculas
def pasa_tokens_a_minusculas(lista_tokens: list):
    token_rta = []
    for palabra in lista_tokens:
        token_rta.append(palabra.lower())
    return token_rta

# Elimina tokens cortos
def elimina_tokens_cortos(lista_tokens: list):
    token_rta = []
    for palabra in lista_tokens:
        if len(palabra)>=3:
            token_rta.append(palabra)
    return token_rta

# Elimina stop words
def elimina_stop_words(lista_tokens: list):
    a=set(stopwords.words('english'))
    token_rta = [palabra for palabra in lista_tokens if palabra not in a]
    return token_rta

# Tokeniza el texto y limpia la lista tokenizada
def tokenize_and_clean(texto: str):
    token = word_tokenize(texto) # Tokenizo
    token = limpia_signos_de_puntuacion(token) # Limpio signos de puntuacion
    token = limpia_numeros(token) # Limpio números
    token = elimina_tokens_vacios(token) # Elimino tokens vacios
    token = pasa_tokens_a_minusculas(token) # Paso los tokens a minusculas
    token = elimina_tokens_cortos(token) # Elimino tokens cortos
    token = elimina_stop_words(token) # Elimino stop words del Inglés, de la lista de tokens
    return token

# Tokeniza, limpia y vuelve a armar en forma de string
def tokenizar_limpiar_y_obtener_string(texto: str):
    token_limpio = tokenize_and_clean(texto)
    t_str = ' '.join(token_limpio)
    return t_str

# Serializador / Deserializador de objetos
serializados_d = {'mtx_tfidf' : ['src/preproc/mtx_tfidf.ser', '\t'],
                  'vec_tfidf' : ['src/preproc/vec_tfidf.ser', '\t']}

def serializar(nombre_objeto: str, objeto: any):
       
       if nombre_objeto in serializados_d.keys():

              # Obtengo el directorio raiz desde la variable de entorno DIRECTORIO_RAIZ
              dir_raiz = os.getenv("DIRECTORIO_RAIZ")

              # Escribo el objeto al archivo correspondiente
              path_archivo = os.path.join(dir_raiz, serializados_d[nombre_objeto][0])
              with open(path_archivo, "wb") as archivo:
                  pickle.dump(objeto, archivo)

       else:

              # Error. El serializable no esta en la lista de serializables
              print('Error: El serializable no esta en la lista de serializables preprocesados')

def deserealizar(nombre_objeto: str):

       if nombre_objeto in serializados_d.keys():

              # Obtengo el directorio raiz desde la variable de entorno DIRECTORIO_RAIZ
              dir_raiz = os.getenv("DIRECTORIO_RAIZ")

              # Obtengo el objeto desde el archivo correspondiente
              objeto = None
              path_archivo = os.path.join(dir_raiz, serializados_d[nombre_objeto][0])
              with open(path_archivo, "rb") as archivo:
                   objeto = pickle.load(archivo)

              return objeto
       
       else:

              # Error. El objeto no ha sido preprocesado
              print('Error: El objeto no esta en la lista de serializables preprocesados')
              return None

# Procesamiento
if __name__ == '__main__':

    # Recupero el movies dataset preprocesado
    m_df = etlflow.obtener_df_preprocesado('m_df')

    # Elimino las columnas no utilizadas. Conservo solo id y overview
    m_df = m_df[['id', 'overview']]

    # Tokenizo, limpio y rearmo los overviews
    m_df['cleansed_overview'] = m_df['overview'].apply(tokenizar_limpiar_y_obtener_string)

    # Instancio un Tf-Idf vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Armo la matriz Tf-Idf
    documentos = m_df['cleansed_overview']
    tfidf_matrix = tfidf_vectorizer.fit_transform(documentos)

    # Serializo el vectorizador entrenado y la matriz TFIDF para su uso en la API
    serializar('vec_tfidf', tfidf_vectorizer)
    serializar('mtx_tfidf', tfidf_matrix)
