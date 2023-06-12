# Este es el readme del proyecto integrador 1 de Henry

Alumno: Fernando Embrioni.

Junio de 2023.

Dados dos datasets, uno contieniendo registros de películas con información como id de la película, título, descripción y otros datos, y otro dataset conteniendo información de actores y actrices por película, y directores(as) por película, se solicita:

- Procesar la información para limpiar la misma y dejarla en formatos que luego puedan ser utilizados con facilidad
- Entrenar un modelo de Machine Learning que permita realizar recomendaciones de películas sobre la base de un título dado
- Desplegar una API con 7 endpoints para resolver las siguientes consultas

    > Cantidad de filmaciones por mes dado el nombre del mes en español

    > Cantidad de filmaciones por día dado el nombre del día en español

    > Conocer año de estreno y popularidad de un título dado

    > Conocer año de estreno, la cantidad de votos y valoración promedio para un título dado

    > Conocer cantidad de filmaciones y otros datos del actor/actriz dado el nombre del mismo / de la misma

    > Conocer datos del director(a) y sus producciones dado el nombre del mismo / de la misma

    > Obtener recomendaciones de películas para ver dado el título de una película

MVP

.- ETL completo.

.- API desplegada. Al menos 1 endpoint es funcional.

.- Video en youtube mostrando que funciona correctamente.

.- Detalles de lo solicitado para el MVP en https://github.com/HX-PRomero/PI_ML_OPS/blob/main/Readme.md .


# Instalacion

Clonar este repositorio (branch "using_git_lfs") en la ubicación que usted defina. El mismo contiene archivos preprocesados de las fuentes originales, lo que permite levantar los servicios más rápido.

Sin embargo, si usted quisiera realizar el procesamiento desde el inicio, deberá copiar a la carpeta "src" los archivos "credits.csv" y "movies_dataset.csv" que se encuentran en el siguiente enlace: https://drive.google.com/drive/folders/1nvSjC2JWUH48o3pb8xlKofi8SNHuNWeu

El comando de construccion del ambiente es "./deploy-script.sh" (Linux).

El comando de ejecucion es "python3 code/main.py".

# Variables de entorno y modos de ejecucion

Las siguientes son las variables de entorno que usted debe definir para que el procesamiento pueda realizarse:

DIRECTORIO_RAIZ : Debe apuntar al directorio en el cual usted ha clonado el proyecto. P.Ej. En el caso del directorio default de Render, podría ser "/opt/render/project/src".

AMBIENTE : Esta variable define el modo de ejecucion. En el caso de ser "DEV", los archivos "credits.csv" y "movies_dataset.csv" deben haber sido copiados previamente según se explica más arriba, y la ejecucion realizará el procesamiento completo de los mismos, volviendo a generar los archivos preprocesados. Si la variable de entorno AMBIENTE tiene otro valor (Recomendado), la ejecucion descansará en los archivos preprocesados.

Nota: La ejecucion en modo "DEV" consume una gran cantidad de memoria RAM, y es mayor a 512MB.

# Items del MVP

ETL completo

El ETL del proyecto está resuelto en los archivos "etl_flow.py" y "etl_functions.py". El codigo está comentado. Las funciones principales de ingreso son "etl_flow.preprocesar_credits_dataframes" y "etl_flow.preprocesar_dataframes" que son invocadas desde "main.py" en el modo de ejecucion "DEV".

API desplegada. Al menos 1 endpoint es funcional

Las APIs solicitadas se encuentran desplegadas bajo las siguientes URLs:

Endpoint 1 : https://henry-pi01-ml-ops-fer.onrender.com/cantidad_filmaciones_mes/Marzo

Endpoint 2 : https://henry-pi01-ml-ops-fer.onrender.com/cantidad_filmaciones_dia/Domingo

Endpoint 3 : https://henry-pi01-ml-ops-fer.onrender.com/score_titulo/The%20Terminator

Endpoint 4 : https://henry-pi01-ml-ops-fer.onrender.com/votos_titulo/Alien

Endpoint 5 : https://henry-pi01-ml-ops-fer.onrender.com/get_actor/Tom%20Hanks

Endpoint 6 : https://henry-pi01-ml-ops-fer.onrender.com/get_director/James%20Cameron

Endpoint Recomendacion : https://henry-pi01-ml-ops-fer.onrender.com/recomendacion/The%20Godfather

Video en youtube mostrando que funciona correctamente

https://youtu.be/LA0Znz6GvM8

# Anexos

## Despliegue en Render

La siguiente información se brinda como sugerencia para el despliegue en Render ( https://dashboard.render.com/ ) como Servicio Web.


> Environment > Environment Variables

Cree la variable AMBIENTE. El valor de la misma será "PROD". Sólo podrá tomar el valor "DEV" si su ambiente de Render tiene una memoria RAM mínima de 2 GB. Ver instrucciones de instalación para más detalles.

Cree la variable DIRECTORIO_RAIZ. El valor de la misma será el path al directorio raíz del proyecto. Si no definió un directorio raíz para el proyecto, entonces coloque "/opt/render/project/src" en la misma.

> Settings > General

Name : Defina un nombre para su servicio Web. P.Ej. "prueba-ml-ops".

Region : Dejar lo que se ofrezca por defecto.

Instance Type : Free o la que usted tenga contratada.

> Settings > Build & Deploy

Repository : "https://github.com/fembrioni/henry-pi01-ml-ops".

Branch : "using_git_lfs".

Root Directory : Defina el que usted quiera o deje en blanco. Recuerde actualizar la variable de entorno DIRECTORIO_RAIZ de forma acorde. Si lo deja en blanco, a Junio de 2023 Render usa "/opt/render/project/src", por lo que deberá escribir eso en su variable antes mencionada.

Build Filters : Dejar vacío.

Build command : "./deploy-script.sh".

Start command : "python3 code/main.py". Dentro de main.py están las instrucciones para levantar los servicios web de la App (FastAPI) en el puerto 8000, utilizando uvicorn. Si no desea usar ese puerto, vaya al final de "main.py" y actualicelo a un valor que le sea conveniente.

Auto-Deploy : Dejar en Yes.

> Settings > Custom Domains

Sin cambios.

> Settings > PR Previews

Sin cambios.

> Settings > Health & Alerts

Sin cambios.

## Estructura de directorios y contenido de los archivos

El proyecto está estructurado bajo el siguiente esquema de directorios.

### Directorio raiz

Contiene archivos relacionados con la configuracion y el despliegue.

`.gitattributes y .gitignore` relacionados con git.

`compose-dev.yaml` es el archivo de configuracion del ambiente de desarrollo.

`readme.md` es el documento que usted está leyendo ahora.

`requirements.txt` contiene las dependencias requeridas por el proyecto.

`deploy-script.sh` contiene las instrucciones para desplegar el proyecto en un ambiente Linux (Se puede armar un .bat con su contenido para hacer el despliegue en Windows).

### Directorio ./src

Contiene archivos relacionados con el origen de los datos. Dado que los archivos `"credits.csv" y "movies_dataset.csv"` son muy voluminosos, decidí no incluirlos en este repositorio. Sin embargo, más arriba se provee un link para descargar los mismos. En el modo de ejecución "PROD" los mismos no son necesarios.

`Diccionario_de_datos_movies.tsv` contiene las descripciones de los campos en "movies_dataset.csv".

### Directorio ./src/preproc

Contiene `archivos con extensión "tsv"`. Los mismos se corresponden con el preprocesamiento (ETL) de los archivos originales.
Además, en este directorio, una vez se ejecute por primera vez el proyecto, se crearán dos archivos con extensión "ser" que se corresponden con la serializacion de dos objetos que componen el modelo de recomendación de películas.

### Directorio ./code

Contiene los archivos de programa de este proyecto.

Los `archivos con extensión "ipynb"` son archivos de Jupyter Notebook y contienen Análisis Exploratorios de Datos, como así también pruebas de concepto.

`main.py` es el archivo mediante el cual se procesa la información y se proveen los servicios de API. Si la variable de ambiente "AMBIENTE" tiene valor "DEV" se procesarán los archivos "credits.csv" y "movies_dataset.csv" por lo que asegurese de haber copiado los mismos al directorio ./src antes de ejecutar main.py.

`ml_model_generator.py` contiene las funciones de preprocesamiento de texto y el entrenamiento del modelo de recomendación basado en similaridad coseno vía TFIDF (Term Frequency-Inverse Document Frequency). El entrenamiento se almacena en dos archivos serializados vía pickle.

`etl_flow.py` junto con el soporte de `etl_functions.py` contiene las funciones de ETL. Su ejecucion produce un lote de archivos en la carpeta ./src/preproc con extensión "tsv". Los mismos se corresponden con diversos dataframes que comparten el "id" de la película para luego hacer join entre los mismos.
