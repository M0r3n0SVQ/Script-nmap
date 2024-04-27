#!/usr/bin/python3

import nmap
import subprocess
import platform
import os
from datetime import datetime

print('''

  __  __  ___      ____         ___   _______      ______  
 |  \\/  |/ _ \\    |___ \\       / _ \\ / ____\\ \\    / / __ \\ 
 | \\  / | | | |_ __ __) |_ __ | | | | (___  \\ \\  / / |  | |
 | |\\/| | | | | '__|__ <| '_ \\| | | |\\___ \\  \\ \\/ /| |  | |
 | |  | | |_| | |  ___) | | | | |_| |____) |  \\  / | |__| |
 |_|  |_|\\___/|_| |____/|_| |_|\\___/|_____/    \\/   \\___\\_\\
                                                           
''')

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

# Obtener el PID del proceso asociado al puerto
if sistema_operativo == "Windows":
    if 'tcp' in results.keys() and puerto_seleccionado in results['tcp']:
        pid_proceso = int(results['tcp'][puerto_seleccionado]['pid'])
    else:
        pid_proceso = None
else:
    pid_proceso = int(salida_netstat_puerto.stdout.split()[6])

# Mostrar los detalles del puerto seleccionado por pantalla
print(f"\nDetalles del puerto {puerto_seleccionado} en sistemas {sistema_operativo}:")
print(salida_netstat_puerto.stdout)

# Función para generar el reporte de seguridad
def generar_reporte(puerto, detalles, pid):
    reporte = f"Detalles del puerto {puerto}:\nPID del proceso: {pid}\n{detalles}"
    return reporte

# Generar el reporte de seguridad
reporte_seguridad = generar_reporte(puerto_seleccionado, salida_netstat_puerto.stdout, pid_proceso)

# Obtener la fecha actual
fecha_actual = datetime.now().strftime("%Y-%m-%d")

# Directorio del escritorio según el sistema operativo
if sistema_operativo == "Windows":
    directorio_escritorio = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
else:
    directorio_escritorio = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

# Ruta del archivo para el reporte en el escritorio
ruta_reporte = os.path.join(directorio_escritorio, f"reporte_seguridad_{fecha_actual}.txt")

# Escribir el reporte en el archivo
with open(ruta_reporte, "w") as archivo:
    archivo.write(reporte_seguridad)

print(f"\nReporte de seguridad guardado en el archivo: {ruta_reporte}")

# Solicitar al usuario que presione una tecla para salir
input("\nPresiona Enter para salir...")



