# Este es el readme del proyecto integrador 1 de Henry

Alumno: Fernando Embrioni.

Junio de 2023.


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

Endpoint Recomendacion : TODO

Video en youtube mostrando que funciona correctamente

TODO

# Anexos

# Despliegue en Render

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

# Estructura de directorios y contenido de los archivos

TODO
