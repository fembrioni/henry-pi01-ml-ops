# Este es el archivo principal de procesamiento del proyecto
# PI01-MLOPS de Henry

# Imports
import pandas as pd
from fastapi import FastAPI
import etl_flow as etlf

# Declaro la App de FastAPI
fastAPIApp = FastAPI()

# Obtengo los dataframes procesados luego del ETL
dataframes_d = etlf.obtener_dataframes()

# Endpoints

# Endpoint de prueba
@fastAPIApp.get("/inicio")
async def ruta_prueba():
    return "Hola"
