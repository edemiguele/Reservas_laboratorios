# -*- coding: utf-8 -*-
# O # -*- coding: cp1252 -*-
# O # -*- coding: latin-1 -*-

import csv
import json
import mysql.connector
import os

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

for clave, valor in config.items():
    if "calendario" in clave.lower():  # Verifica si "excel" está en el nombre de la clave
        # Ruta del archivo Excel
        ruta_csv = valor
        with open(ruta_csv, newline='', encoding='utf-8') as csvfile:
            lector = csv.reader(csvfile, delimiter=';')  # Usa el delimitador adecuado
            for fila in lector:
                if len(fila) < 4:
                    continue  # Saltar filas de cabecera
                fecha = fila[1]  
                diaeina = fila[3] 
                # Actualizar la tabla prereservas
                consulta = """
                    UPDATE prereservas
                    SET diaEina = %s
                    WHERE DATE_FORMAT(fechaInicio, "%d/%m/%Y") = %s
                """
                #print(f"diaeina: {diaeina},fecha: {fecha}")
                cursor.execute(consulta, (diaeina, fecha))

conexion.commit()
cursor.close()
conexion.close()


