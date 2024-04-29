# Escáner de Puertos con Nmap 🛡️

Este proyecto consiste en un script Python que utiliza la biblioteca nmap para realizar un escaneo de puertos en una dirección IP especificada por el usuario. Además, permite al usuario seleccionar un puerto específico para obtener detalles adicionales.

Se creará una carpeta llamada reportes en la ruta donde se encuentre el script que guardará el reporte generado.

## Descargar Python ✅

1. **Actualizar repositorios**

        sudo apt update


        sudo apt upgrade

2. **Instalar Python3**

        sudo apt install python3
   
4.  **Instalar nmap**

        sudo apt install nmap
      

5. **Instalar módulo psutil**

    Proporciona información sobre los procesos en ejecución y la utilización del sistema.

        pip install psutil


## Descargar script 🚀

1. **Clonar el Repositorio:** Clona este repositorio en tu máquina local:

    git clone https://github.com/M0r3n0SVQ/Script-nmap.git

2. **Navegar al Directorio:** Navega al directorio del repositorio:

    cd Script-nmap

3. **Ejecutar el Script:**

   **Linux**
   
   python3 SCRIPT-NMAP.py

   **Windows**
   
   py SCRIPT-NMAP.py

4. **Sigue las Instrucciones en pantalla para ingresar la dirección IP y seleccionar un puerto para obtener detalles de seguridad.**

## Detener Servicios en Windows ⛔

Cuando seleccionamos el puerto, nos mostrará por pantalla los detalles del puerto y un numero a la derecha que es el ID del proceso.
Podemos parar el proceso utilizando el administrador de tareas de Windows, lo podemos abrir con CTRL + Mayús + ESC, una vez abierto seleccionamos la pestaña Servicios, en la parte superior nos sale un buscador para ver que proceso está asociado al puerto, si es un proceso que no reconocemos podemos detenerlo ya que
podría tratarse de un proceso malicioso de parte de un ataque.

## Detener Servicios en Linux ⛔

Cuando necesites detener un servicio asociado a un puerto en Linux, puedes seguir estos pasos:


1. **Si al ejecutar el script sobre el puerto deseado y no muesta el proceso podemos intentar averiguarlo con el comando:**
   
   netstat -tuln
   
   ss -tuln

2. **Detener el proceso: Una vez que hayas identificado el PID del proceso que deseas detener, utiliza el comando kill seguido del PID para detener el proceso.**

    sudo kill PID_del_proceso

## Funcionalidades ✨

- **Escaneo de Puertos:** Utiliza la biblioteca nmap para escanear los puertos de una dirección IP.
- **Visualización de Puertos Abiertos:** Muestra los puertos abiertos encontrados durante el escaneo.
- **Selección de Puerto:** Permite al usuario seleccionar un puerto específico para obtener detalles adicionales.
- **Generación de Reporte:** Genera un reporte de seguridad en un archivo de texto.

## Errores ❌

**En Linux puede haber errores que no muestre el proceso asociado al puerto o que muestre un nombre de proceso asociado erróneo.**

## Contribuciones 🤝

Las contribuciones son bienvenidas. Si encuentras algún problema o tienes alguna mejora, no dudes en abrir un issue o enviar un pull request.

## Autor

Este proyecto fue desarrollado por [M0r3n0SVQ](https://github.com/M0r3n0SVQ).

---
