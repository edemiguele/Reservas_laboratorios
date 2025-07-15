# -*- coding: utf-8 -*-
# O # -*- coding: cp1252 -*-
# O # -*- coding: latin-1 -*-

from asyncio.windows_events import NULL
import json
import requests
import mysql.connector
import os
from openpyxl import load_workbook
from openpyxl import Workbook
import glob
import unicodedata
from datetime import datetime

def quitar_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_path, "r") as config_file:
    config = json.load(config_file)

# Configuración de la conexión
conexion = mysql.connector.connect(
    host=config["db_host"],       # Dirección del servidor
    user=config["db_user"],       # Usuario de la base de datos
    password=config["db_password"],  # Contraseña del usuario
    database=config["db_name"]    # Nombre de la base de datos
)

# Crear un cursor para ejecutar consultas
cursor = conexion.cursor()

directorio = config["reservas"]
for ruta_archivo in glob.glob(os.path.join(directorio, "*.json")):
    print(f"ruta_archivo: {ruta_archivo}")
    
    #valor = nombre_archivo.rsplit('_', 1)[-1].replace('.json', '')
    nombre_archivo = os.path.basename(ruta_archivo)  # 'reservas_430_3.json'
    partes = nombre_archivo.split('_')       # ['reservas', '430', '3.json']
    valor = partes[1]                        # '430'
    
    #print(f"valor del plan: {valor}")

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        data = json.load(f)
        # Aquí puedes procesar el contenido de cada archivo JSON
        if isinstance(data, list) and len(data) > 0:
            print("El JSON esta lleno.")
            # Ejemplo: recorrer los elementos del JSON
            for item in data:
                # Procesa cada item como necesites
                    
                valores_vistos = set()
                registros_unicos = []
                encontrado=0
                if isinstance(item, dict): 
                    #"tipologia": "Pr&aacute;cticas de laboratorio",
                    if "aula" in item and item["aula"] is not None and item["aula"] != " ":        
                        aula = item["aula"]
                        inicio = item["start"]
                        fin = item["end"]                                                   

                        # Consulta SQL para insertar datos
                        sql = """
                        INSERT INTO sigma (aula, inicio, fin)
                        VALUES (%s, %s, %s)
                        """

                        # Ejecutar la consulta con los datos
                        cursor.execute(sql, (aula, inicio, fin))
        else:
            print(f"{valor} No tiene datos.")  
conexion.commit()
# Cerrar el cursor y la conexión
cursor.close()
conexion.close()
