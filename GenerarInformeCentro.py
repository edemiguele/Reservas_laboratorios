import mysql.connector
import os
import json
import csv
from datetime import timedelta, datetime
from openpyxl import Workbook

config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_path, "r") as config_file:
    config = json.load(config_file)

conexion = mysql.connector.connect(
    host=config["db_host"],
    user=config["db_user"],
    password=config["db_password"],
    database=config["db_name"]
)
cursor = conexion.cursor()

consulta_select = """
SELECT a.nbAsignatura AS Nombre_Asignatura, 
       a.denomplan AS Titulacion, 
		 a.idAsignatura AS Codigo_Asignatura, 
		 a.curso AS Curso, 
		 a.cuatrimestre AS Semestrre, 
		 r.idgrupo AS Grupo_Practicas, 
		 SUBSTRING(r.diaEina, 1, 2) AS Dia_EINA,
		 date_format(r.fechaInicio, '%d/%m/%Y %H:%i') AS Fecha_Inicio,
		 date_format(r.fechaFin, '%d/%m/%Y %H:%i') AS Fecha_Fin, 
		 r.idespacio AS Espacio, 
		 e.edificio AS Edificio
FROM asignaturas a, reservas r, espacios e
WHERE a.idAsignatura=r.idAsignatura
AND r.idespacio=e.codEspacio
ORDER BY r.idAsignatura, r.idgrupo, r.fechaInicio;
"""

# Ejecutar la consulta
cursor.execute(consulta_select)

# Obtener los resultados
resultados = cursor.fetchall()

# Obtener los nombres de las columnas
columnas = [desc[0] for desc in cursor.description]

# Crear un nuevo archivo Excel
wb = Workbook()
hoja = wb.active
hoja.title = "ReservasDIIS"

# Escribir los nombres de las columnas en la primera fila
hoja.append(columnas)

# Escribir los datos en las filas siguientes
for fila in resultados:
    nueva_fila = list(fila)
    hoja.append(fila)

# Ruta para guardar el archivo Excel en el mismo directorio que config.json
ruta_excel_salida = os.path.join(os.path.dirname(config_path), "ReservasDIIS.xlsx")

# Guardar el archivo Excel
wb.save(ruta_excel_salida)

print(f"Archivo Excel generado en: {ruta_excel_salida}")               
# Cerrar el cursor y la conexión
cursor.close()
conexion.close()
