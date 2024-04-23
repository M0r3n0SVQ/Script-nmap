#!/usr/bin/python3

import nmap
import subprocess

print('''
           _____     _____       _____ _____  _   _  _____ 
          |  _  |   |____ |     |  _  /  ___|| | | ||  _  |
 _ __ ___ | |/' |_ __   / /_ __ | |/' \ `--. | | | || | | |
| '_ ` _ \|  /| | '__|  \ \ '_ \|  /| |`--. \| | | || | | |
| | | | | \ |_/ / | .___/ / | | \ |_/ /\__/ /\ \_/ /\ \/' /
|_| |_| |_|\___/|_| \____/|_| |_|\___/\____/  \___/  \_/\_\
                                                           
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

# Comando para obtener información detallada del puerto seleccionado
comando_netstat_puerto = f"netstat -tuln | grep {puerto_seleccionado}"

# Ejecutar el comando y obtener la salida
salida_netstat_puerto = subprocess.run(comando_netstat_puerto, shell=True, capture_output=True, text=True)

# Mostrar los detalles del puerto seleccionado por pantalla
print(f"\nDetalles del puerto {puerto_seleccionado}:")
print(salida_netstat_puerto.stdout)

# Función para generar el reporte de seguridad
def generar_reporte(puerto, detalles):
    reporte = f"Detalles del puerto {puerto}:\n{detalles}"
    return reporte

# Generar el reporte de seguridad
reporte_seguridad = generar_reporte(puerto_seleccionado, salida_netstat_puerto.stdout)

# Escribir el reporte en un archivo de texto
nombre_archivo = "reporte_seguridad.txt"
with open(nombre_archivo, "w") as archivo:
    archivo.write(reporte_seguridad)

print(f"\nReporte de seguridad guardado en el archivo: {nombre_archivo}")
