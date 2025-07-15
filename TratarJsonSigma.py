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
import subprocess

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

# Vaciar la tabla prereservas antes de insertar nuevos datos
cursor.execute("TRUNCATE TABLE prereservas")
conexion.commit()

directorio = config["reservas"]
for ruta_archivo in glob.glob(os.path.join(directorio, "*.json")):
    print(f"ruta_archivo: {ruta_archivo}")
    
    nombre_archivo = os.path.basename(ruta_archivo)  # 'reservas_25802.json'
    valor = nombre_archivo.rsplit('_', 1)[-1].replace('.json', '')
    
    #partes = nombre_archivo.split('_')       # ['reservas', '430', '3.json']
    #valor = partes[1]                        # '430'
    
    #print(f"valor del plan: {valor}")

    # Recoger las asignaturas del plan.
    cursor.execute(
    #    "SELECT codAsignatura FROM asignaturas WHERE codplan = %s",
    #    (valor,)
        "SELECT idAsignatura FROM asignaturas WHERE idAsignatura = %s and activo = 1 and vinculada = 0", (valor,)
    )
    asignaturas = cursor.fetchall()

    #print(f"asignaturas: {asignaturas}")    

    if asignaturas:  # Si la lista no está vacía, hay asignaturas
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Aquí puedes procesar el contenido de cada archivo JSON
            if isinstance(data, list) and len(data) > 0:
                #print("El JSON esta lleno.")
                # Ejemplo: recorrer los elementos del JSON
                for item in data:
                    # Procesa cada item como necesites
                    
                    valores_vistos = set()
                    registros_unicos = []
                    encontrado=0

                    if isinstance(item, dict) and "tipologia" in item: 
                        #"tipologia": "Pr&aacute;cticas de laboratorio",
                        if quitar_acentos(item["tipologia"].strip().lower()) == "pr&aacute;cticas de laboratorio":

                            # Comprobar si existen reservas activas
                            cursor.execute("SELECT COUNT(*) FROM reservas")
                            num_reservas_activas = cursor.fetchone()[0]
                            
                            # Si tenemos reservas en la tabla de reservas no es la primera carga
                            if num_reservas_activas > 0:                                                           

                                # Datos a insertar en bbdd
                                codAsignatura = item["codAsignatura"]

                                #Comprobamos que la asignatura no sea vinculada y este activa
                                cursor.execute(
                                    "SELECT COUNT(*) FROM asignaturas WHERE idAsignatura = %s AND activo = 1 and vinculada = 0",
                                    (codAsignatura,)
                                )
                                existe = cursor.fetchone()[0] > 0
                                if existe:

                                    start = item["start"]
                                    if isinstance(start, str):
                                        fecha_start = datetime.fromisoformat(start)
                                    else:
                                        fecha_start = start

                                    if fecha_start.month >= 9:
                                        inicio_anyo_curso = fecha_start.year
                                    else:
                                        inicio_anyo_curso = fecha_start.year - 1

                                    end = item["end"]
                                    codGrupo = item["codGrupo"]
                                    diaSemana = item["diaSemana"]
                                    observacion = item["observacion"]                            
                                    codCentro = item["codCentro"]
                                    procesado = datetime.now()
                                    aula = item["aula"]
                                    espacio = aula.split(' -')[0] if '-' in aula else aula.strip()
                                

                                    #print(f"codAsignatura: {codAsignatura}, start: {end}, codGrupo: {codGrupo},diaSemana: {diaSemana}, observacion: {observacion}, aula: {aula}, codCentro: {codCentro}")
                                    # Consulta SQL para insertar datos
                                    sql = """
                                    INSERT INTO prereservas (idAsignatura, fechaInicio, fechaFin, idgrupo, idespacio, diaSemana, observaciones, procesado, inicio_anyo_curso)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    """

                                    # Ejecutar la consulta con los datos
                                    cursor.execute(sql, (codAsignatura, start, end, codGrupo, espacio, diaSemana, observacion, procesado, inicio_anyo_curso))

                            else:
                                # Datos a insertar en bbdd
                                codAsignatura = item["codAsignatura"]
                                
                               #Comprobamos que la asignatura no sea vinculada y este activa
                                cursor.execute(
                                    "SELECT COUNT(*) FROM asignaturas WHERE idAsignatura = %s AND activo = 1 and vinculada = 0",
                                    (codAsignatura,)
                                )
                                existe = cursor.fetchone()[0] > 0
                                if existe:
                                    start = item["start"]
                                    print(f"codAsignatura introducida : {codAsignatura}")
                                    if isinstance(start, str):
                                        fecha_start = datetime.fromisoformat(start)
                                    else:
                                        fecha_start = start

                                    if fecha_start.month >= 9:
                                        inicio_anyo_curso = fecha_start.year
                                    else:
                                        inicio_anyo_curso = fecha_start.year - 1

                                    end = item["end"]
                                    codGrupo = item["codGrupo"]
                                    diaSemana = item["diaSemana"]
                                    observacion = item["observacion"]                            
                                    codCentro = item["codCentro"]
                                    procesado = datetime.now()
                                

                                    #print(f"codAsignatura: {codAsignatura}, start: {end}, codGrupo: {codGrupo},diaSemana: {diaSemana}, observacion: {observacion}, aula: {aula}, codCentro: {codCentro}")
                                    # Consulta SQL para insertar datos
                                    sql = """
                                    INSERT INTO prereservas (idAsignatura, fechaInicio, fechaFin, idgrupo, diaSemana, observaciones, procesado, inicio_anyo_curso)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                    """

                                    # Ejecutar la consulta con los datos
                                    cursor.execute(sql, (codAsignatura, start, end, codGrupo, diaSemana, observacion, procesado, inicio_anyo_curso))
                                else:
                                    print(f"no tenemos codAsignatura : {codAsignatura}")
                            # Confirmar los cambios en la base de datos
                            conexion.commit()
                            tienepracticas=1
                        else:
                            tienepracticas=0
            else:
                print(f"{valor} NO tiene practicas de laboratorio.")
    else:
        print(f"{valor} NO esta en asignaturas.")
        # Si quieres, puedes saltar el procesamiento de este archivo
        continue

# Una vez que se han insertado todos los datos tenemos que realizar una excel con los datos de reservas de asignaturas manuales      
# Consulta SQL para obtener las reservas asociadas a asignaturas con manual = 1
consulta_select = """
    SELECT r.idAsignatura, r.fechaInicio, r.fechaFin, r.idgrupo, r.idespacio, r.numpractica, r.observaciones
    FROM prereservas r
    INNER JOIN asignaturas a ON r.idAsignatura = a.idasignatura
    WHERE a.manual = 1
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
hoja.title = "Reservas Manual"

# Escribir los nombres de las columnas en la primera fila
hoja.append(columnas)

# Escribir los datos en las filas siguientes
# preservas contiene: id, idAsignatura,inicio,fin,idgrupo,idespacio,numpractica,observaciones,diaSemana, diaEina, procesado, inicio_anyo_curso
for fila in resultados:
    nueva_fila = list(fila)
    try:
        # Intenta convertir el campo a datetime si es string
        if isinstance(nueva_fila[2], str):
            nueva_fila[2] = datetime.fromisoformat(nueva_fila[2])
        if isinstance(nueva_fila[3], str):
            nueva_fila[3] = datetime.fromisoformat(nueva_fila[3])
    except Exception:
        pass  # Si falla, deja el valor original
    hoja.append(fila)

# Ruta para guardar el archivo Excel en el mismo directorio que config.json
ruta_excel_salida = os.path.join(os.path.dirname(config_path), "reservas_manual.xlsx")

# Guardar el archivo Excel
wb.save(ruta_excel_salida)

print(f"Archivo Excel generado en: {ruta_excel_salida}")               
# Cerrar el cursor y la conexión
cursor.close()
conexion.close()

# Ejecutamo TratarCSVCalendario.py para que rellene los dias de calendario EINA
subprocess.run(["python", "TratarCSVCalendario.py"])