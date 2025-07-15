# Reservas_laboratorios
Carga de datos para la aplicación de reservas de laboratorios

# Fichero de configuracion de los parametros de la aplicación, 
las rutas tendran que ser modificadas a las rutas del servidor:
{
    "db_host": "danae03.unizar.es",
    "db_user": "tauadm",
    "db_password": "xxxxxxxxxxxxxxxx",
    "db_name": "tau",
    "virtualeslsi": "D:\\Proyectos\\DatosExcel\\Cortina virtual LSI.xlsx",
    "virtualesatc": "D:\\Proyectos\\DatosExcel\\Cortina virtual ATC.xlsx",
    "virtualesisa": "D:\\Proyectos\\DatosExcel\\Cortina virtual ISA.xlsx",
    "restriccioneslsi":"D:\\Proyectos\\DatosExcel\\Restricciones laboratorios LSI.xlsx",
    "restriccionesatc":"D:\\Proyectos\\DatosExcel\\Restricciones laboratorios ATC.xlsx",
    "restriccionesisa":"D:\\Proyectos\\DatosExcel\\Restricciones laboratorios ISA.xlsx",
    "lugaresisa":"D:\\Proyectos\\DatosExcel\\Lugar practicas ISA.xlsx",
    "lugaresatc":"D:\\Proyectos\\DatosExcel\\Lugar practicas ATC.xlsx",
    "lugareslsi":"D:\\Proyectos\\DatosExcel\\Lugar practicas LSI.xlsx",
    "url": "https://docenciadiis:docenfacildiis@odile.unizar.es/api/asignaturaGrupoProfesor/2025/110/5007",
    "reservas": "D:\\Proyectos\\DatosExcel\\reservas\\",
    "calendario": "D:\\Proyectos\\DatosExcel\\calendario.csv",
    "manuales": "D:\\Proyectos\\DatosExcel\\reservas_manual_25_26.xlsx",
    "gruposacentro": "D:\\Proyectos\\DatosExcel\\resolucion_conflictos.csv"
}
virtualeslsi: fichero que proporciona Carlos con las cortinas virtuales de LSI
virtualesatc: fichero que proporciona Carlos con las cortinas virtuales de ATC
virtualesisa: fichero que proporciona Carlos con las cortinas virtuales de ISA
restriccioneslsi: fichero que proporciona Carlos con las restricciones de laboratorios de LSI
restriccionesatc: fichero que proporciona Carlos con las restricciones de laboratorios de ATC
restriccionesisa: fichero que proporciona Carlos con las restricciones de laboratorios de ISA
lugaresisa: fichero que proporciona Carlos con los lugares donde se impartiran practicas de ISA
lugaresatc: fichero que proporciona Carlos con los lugares donde se impartiran practicas de ATC
lugareslsi: fichero que proporciona Carlos con los lugares donde se impartiran practicas de LSI
calendario: fichero con los dias de calendario EINA que proporciona Alberto
manuales: fichero con las reservas que se definen de forma manual por Carlos

url: point de api de odile

reservas: carpeta donde se encuentran los ficheros JSON descargados de Sigma.

# Ficheros que lo componen:

- TratarJsonOdile.py aplicación que carga los datos de las aplicaciones desde Odile del departamento
- TratarExcel.py aplicación que carga los datos de las excel de cortinas virtuales, restricciones, lugares.
- TratarJsonSigma.py aplicación que carga en prereservas todos los datos de Sigma
- TratarCSVCalendario.py aplicación que define para cada prereserva el dia de calendario EINA que es.
- TratarManuales.py aplicacion que carga las reservas definidas de forma manual.
- GenerarInformeCentro.py aplicación que genera una excel para que se pase a Centro y ellos incorporen a mano los datos de todas en Sigma.
- Sabana.py aplicación que genera una excel para comprobación de datos por parte de Carlos.

  # Importante leer documento TAU.pdf.
