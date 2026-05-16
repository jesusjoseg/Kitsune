import subprocess
import hashlib
import requests
import platform
import os
from datetime import datetime


class SeguridadDemo:
    def __init__(self):
        self.app_data = os.path.join(os.environ['LOCALAPPDATA'], "KITSUNE_DEMO")
        self.rastro_file = os.path.join(self.app_data, "win_log_sys.dat")
        # Asegúrate de que esta URL sea la de tu servidor local o remoto
        self.url_php = "http://localhost:3000/VerificarDemo.php"

    def Obtener_hwid(self):
        try:
            # Usamos PowerShell en lugar de WMIC para mayor compatibilidad
            comando_baseboard = 'powershell "Get-CimInstance Win32_BaseBoard | Select-Object -ExpandProperty SerialNumber"'
            comando_cpu = 'powershell "Get-CimInstance Win32_Processor | Select-Object -ExpandProperty ProcessorId"'

            m_board = subprocess.check_output(comando_baseboard, shell=True).decode().strip()
            cpu = subprocess.check_output(comando_cpu, shell=True).decode().strip()

            raw_id = f"Kitsune-{m_board}-{cpu}"
            # Creamos el Hash para la columna 'Vincule'
            return hashlib.sha256(raw_id.encode()).hexdigest()[:16].upper()
        except Exception as e:
            print(f"Error obteniendo HWID con PowerShell: {e}")
            return "ID_UNKNOWN"

    def Gestiona_rastro_local(self):
        if not os.path.exists(self.app_data):
            os.makedirs(self.app_data)
            os.system(f'attrib +h "{self.app_data}"')

        if not os.path.exists(self.rastro_file):
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            with open(self.rastro_file, 'w') as f:
                f.write(fecha_hoy)
            return fecha_hoy
        else:
            with open(self.rastro_file, 'r') as f:
                contenido = f.read().strip()

                # --- SOLUCIÓN AL ERROR ---
                # Si el archivo tiene el formato largo (Fecha:2026...), extraemos solo la fecha
                if "Fecha:" in contenido:
                    # Buscamos la línea que empieza con Fecha: y cortamos los 10 caracteres de la fecha
                    for linea in contenido.split('\n'):
                        if linea.startswith("Fecha:"):
                            return linea.replace("Fecha:", "").strip()

                # Si el archivo ya está limpio o es formato simple, lo devolvemos tal cual
                return contenido

    def Verifica_estado(self ,correo):
        fecha_instala_str = self.Gestiona_rastro_local()
        fecha_instala = datetime.strptime(fecha_instala_str, '%Y-%m-%d')
        dia_usados = (datetime.now() - fecha_instala).days
        dias_restantes = 30 - dia_usados

        # Los nombres de las llaves coincidirán con lo que recibirá el PHP
        datos = {
            "hwid": self.Obtener_hwid(),
            "NombrePc": platform.node(),
            "correo": correo,
            "dias_restantes": dias_restantes
        }
        return datos

    def Enviar_Vinculacion(self ,correo):
        """Envía los datos a VerificarDemo.php para actualizar la tabla Usuario"""
        datos_enviar = self.Verifica_estado(correo)
        try:
            # Enviamos los datos por POST
            response = requests.post(self.url_php, data=datos_enviar, timeout=7)
            return response.json()
        except Exception as e:
            return {"status": "error", "mensaje": str(e)}