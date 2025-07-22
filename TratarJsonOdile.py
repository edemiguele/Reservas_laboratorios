# -*- coding: utf-8 -*-
# O # -*- coding: cp1252 -*-
# O # -*- coding: latin-1 -*-

import json
import requests
import mysql.connector
import os
from openpyxl import load_workbook
from openpyxl import Workbook

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

# Realizar la solicitud datos json
r = requests.get(config["url"])
# Convertir la respuesta a un diccionario
data = r.json()

# Vaciar la tabla asignaturas antes de insertar nuevos datos
cursor.execute("TRUNCATE TABLE asignaturas")
conexion.commit()

# Verificar el primer elemento de la lista
if isinstance(data, list) and len(data) > 0:
    print("El JSON esta lleno.")
else:
    print("El JSON no es una lista o esta vacio.")


#"tipoDocencia":132,"denomTipoDocencia":"(3B)Prácticas informatizadas "
#"tipoDocencia":131,"denomTipoDocencia":"(3A)Prácticas de laboratorio "

#Tabla Asignaturas: codAsignatura, nbAsignatura, codArea, acronimo, centro, cuatrimestre, manual, vinculada, activo, aulacentro, aulateoria, rotada
valores_vistos = set()
registros_unicos = []
encontrado=0

for item in data:

    if isinstance(item, dict):

        #if item["tipoDocencia"] == 131 or item["tipoDocencia"] == 132:        

            if item["codAsignatura"] not in valores_vistos:
                valores_vistos.add(item["codAsignatura"])

                # Datos a insertar en bbdd
                codAsignatura = item["codAsignatura"]
                denomAsignatura = item["denomAsignatura"]
                codPlan = item["codPlan"]
                denomPlan = item["denomPlan"]
                codArea = item["codArea"]
                codCentro = item["codCentro"]
                anualCuatrimestral = item["anualCuatrimestral"]
                vinculada = item["vinculada"]
                curso = item["curso"]
               
                #Calculamos el acronimo
                primeras_letras = [palabra[0] for palabra in denomPlan.split()  if palabra[0].isupper()]
                segundas_letras = [palabra[0] for palabra in denomAsignatura.split()]
                acronimo = ("".join(segundas_letras)).lower()+"_"+"".join(primeras_letras)

                # Consulta SQL para insertar datos
                sql = """
                INSERT INTO asignaturas (idAsignatura, nbAsignatura,codPlan,denomPlan, codArea, acronimo, centro, cuatrimestre, manual, vinculada, curso)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                # Ejecutar la consulta con los datos
                cursor.execute(sql, (codAsignatura, denomAsignatura, codPlan, denomPlan, codArea, acronimo, codCentro, anualCuatrimestral,0, vinculada, curso))

                # Confirmar los cambios en la base de datos
                conexion.commit()
               
# Cerrar el cursor y la conexión
cursor.close()
conexion.close()