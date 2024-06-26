#!/usr/bin/python3

import nmap
import subprocess
import platform
import os
from datetime import datetime
import psutil

print('''

  __  __  ___      ____         ___   _______      ______  
 |  \\/  |/ _ \\    |___ \\       / _ \\ / ____\\ \\    / / __ \\ 
 | \\  / | | | |_ __ __) |_ __ | | | | (___  \\ \\  / / |  | |
 | |\\/| | | | | '__|__ <| '_ \\| | | |\\___ \\  \\ \\/ /| |  | |
 | |  | | |_| | |  ___) | | | | |_| |____) |  \\  / | |__| |
 |_|  |_|\\___/|_| |____/|_| |_|\\___/|_____/    \\/   \\___\\_\\
                                                           
''')

# Obtener la ruta del directorio del script
ruta_script = os.path.dirname(os.path.abspath(__file__))

# Solicitar al usuario que ingrese la dirección IP a escanear
ip = input("Ingresa la IP a escanear: ")

# Crear un objeto PortScanner
nm = nmap.PortScanner()

# Realizar el escaneo de puertos con argumentos específicos
results = nm.scan(hosts=ip, arguments="-sV -Pn")

# Función para obtener los puertos abiertos
def obtener_puertos_abiertos():
    puertos_abiertos = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            port_list = nm[host][proto].keys()
            for port in port_list:
                if nm[host][proto][port]["state"] == "open":
                    puertos_abiertos.append(port)
    return puertos_abiertos

# Obtener los puertos abiertos
puertos_abiertos = obtener_puertos_abiertos()

# Mostrar los puertos abiertos al usuario
print("Puertos abiertos:")
for idx, puerto in enumerate(puertos_abiertos, start=1):
    print(f"{idx}. Puerto {puerto}")

# Solicitar al usuario que ingrese el número de puerto a analizar
numero_puerto = int(input("\nIngresa el número del puerto para ver los detalles: "))

# Validar la entrada del usuario
while numero_puerto < 1 or numero_puerto > len(puertos_abiertos):
    print("Número de puerto inválido.")
    numero_puerto = int(input("Por favor, ingresa un número de puerto válido: "))

# Obtener el puerto seleccionado por el usuario
puerto_seleccionado = puertos_abiertos[numero_puerto - 1]

# Determinar el sistema operativo
sistema_operativo = platform.system()

# Comando para obtener información detallada del puerto seleccionado
if sistema_operativo == "Windows":
    comando_netstat_puerto = f"netstat -ano | findstr LISTENING | findstr :{puerto_seleccionado}"
else:
    comando_netstat_puerto = f"netstat -tuln | grep {puerto_seleccionado}"

# Ejecutar el comando y obtener la salida
salida_netstat_puerto = subprocess.run(comando_netstat_puerto, shell=True, capture_output=True, text=True)

# Función para obtener el PID del proceso asociado al puerto utilizando psutil
def obtener_pid_por_puerto(numero_puerto):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == numero_puerto:
            return conn.pid
    return None

# Obtener el PID del proceso asociado al puerto
pid_proceso = obtener_pid_por_puerto(puerto_seleccionado)

# Función para obtener el nombre del proceso asociado al PID utilizando psutil
def obtener_nombre_proceso(pid):
    try:
        proceso = psutil.Process(pid)
        nombre_proceso = proceso.name()
        return nombre_proceso
    except psutil.NoSuchProcess:
        return None
    except psutil.AccessDenied:
        return "Acceso denegado"
    except Exception as e:
        print(f"Error al obtener el nombre del proceso: {e}")
        return None

# Obtener el nombre del proceso asociado al PID
nombre_proceso = obtener_nombre_proceso(pid_proceso)

# Mostrar el nombre del proceso si se obtiene
if nombre_proceso:
    print(f"Nombre del proceso asociado al puerto: {nombre_proceso}")
else:
    print("No se pudo obtener el nombre del proceso asociado al puerto.")

# Mostrar los detalles del puerto seleccionado por pantalla
print(f"\nDetalles del puerto {puerto_seleccionado} en sistemas {sistema_operativo}:")
print(salida_netstat_puerto.stdout)

# Generar el reporte de seguridad
reporte_seguridad = f"Detalles del puerto {puerto_seleccionado}:\n"
reporte_seguridad += f"PID del proceso: {pid_proceso}\n"
reporte_seguridad += salida_netstat_puerto.stdout

# Ruta del directorio para los reportes
ruta_reportes = os.path.join(ruta_script, "reportes")

# Verificar si el directorio de reportes existe, si no existe, crearlo
if not os.path.exists(ruta_reportes):
    os.makedirs(ruta_reportes)

# Ruta del archivo reporte en la carpeta de reportes
fecha_actual = datetime.now().strftime("%Y-%m-%d")
ruta_reporte = os.path.join(ruta_reportes, f"reporte_seguridad_{fecha_actual}.txt")

# Escribir el reporte en el archivo
with open(ruta_reporte, "w") as archivo:
    archivo.write(reporte_seguridad)

print(f"\nReporte de seguridad guardado en el archivo: {ruta_reporte}")

# Solicitar al usuario que presione una tecla para salir
input("\nPresiona Enter para salir...")



