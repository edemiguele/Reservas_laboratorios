import mysql.connector
import os
import json
import csv
from datetime import timedelta, datetime

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

dias_eina = ['La3', 'Ma3', 'Xa3', 'Ja3', 'Va3', 'Lb3', 'Mb3', 'Xb3', 'Jb3', 'Vb3', ]

# Generar intervalos de media hora desde las 8:00 hasta las 22:00
intervalos = []
hora_inicio = datetime.strptime("08:00", "%H:%M")
hora_fin = datetime.strptime("22:00", "%H:%M")
while hora_inicio < hora_fin:
    hora_fin_intervalo = hora_inicio + timedelta(minutes=30)
    intervalos.append((hora_inicio.time(), hora_fin_intervalo.time()))
    hora_inicio = hora_fin_intervalo

fecha_corte = "2026-01-01"

sql = """
SELECT DISTINCT CONCAT(idAsignatura, '-', idgrupo) as asignaturas
FROM reservas
WHERE diaEina = %s
  AND idEspacio IS NOT NULL
  AND TIME(fechaInicio) < %s AND TIME(fechaFin) > %s
  AND {condicion_fecha}
"""


def guardar_csv(nombre_csv, condicion_fecha, fecha_corte):
    with open(nombre_csv, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=';')
        for dia in dias_eina:
            writer.writerow([f"Resultados para diaEina = {dia}"])
            for inicio, fin in intervalos:
                params = (dia, fin.strftime("%H:%M:%S"), inicio.strftime("%H:%M:%S"), fecha_corte)
                consulta = sql.format(condicion_fecha=condicion_fecha)
                cursor.execute(consulta, params)
                asignaturas = [str(row[0]) for row in cursor.fetchall()]
                hora_str = f"{inicio.strftime('%H:%M')}-{fin.strftime('%H:%M')}"
                if asignaturas:
                    writer.writerow([hora_str] + asignaturas)
                else:
                    writer.writerow([hora_str, "(sin asignaturas)"])
            writer.writerow([])  # Línea en blanco entre días

# Guardar CSV para antes del 01/01/2026
csv_antes = os.path.join(os.path.dirname(config_path), "sabana_antes_2026.csv")
guardar_csv(csv_antes, "DATE(fechaInicio) < %s", fecha_corte)

# Guardar CSV para desde el 01/01/2026 (inclusive)
csv_despues = os.path.join(os.path.dirname(config_path), "sabana_despues_2026.csv")
guardar_csv(csv_despues, "DATE(fechaInicio) >= %s", fecha_corte)

print(f"CSV generado: {csv_antes}")
print(f"CSV generado: {csv_despues}")

cursor.close()
conexion.close()

