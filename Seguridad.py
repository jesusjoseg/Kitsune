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
        self.url_php = "https://kitsunepos.rf.gd/VerificarDemo.php"

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

    def Enviar_Vinculacion(self, correo):
        """Envía los datos a VerificarDemo.php resolviendo el bloqueo AES de InfinityFree"""
        import re
        from Crypto.Cipher import AES

        datos_enviar = self.Verifica_estado(correo)

        cabeceras = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

        sesion = requests.Session()  # Usamos una sesión para que recuerde las cookies

        try:
            # 1. Primer intento: Recibir el reto JavaScript
            response = sesion.post(
                self.url_php,
                data=datos_enviar,
                headers=cabeceras,
                timeout=10,
                verify=False
            )

            # Si InfinityFree nos mandó su script AES, lo resolvemos matemáticamente
            if "slowAES.decrypt" in response.text:
                print("[InfinityFree] Sistema de seguridad AES detectado. Calculando Cookie...")

                # Extraemos los tres valores hexadecimales usando Expresiones Regulares (re)
                matches = re.findall(r'toNumbers\("([a-f0-9]+)"\)', response.text)

                if len(matches) >= 3:
                    # Convertimos los strings hex a bytes reales tal como hace el JavaScript
                    a_bytes = bytes.fromhex(matches[0])
                    b_bytes = bytes.fromhex(matches[1])
                    c_bytes = bytes.fromhex(matches[2])

                    # El script usa AES en modo CBC sin padding estándar (o manual)
                    # Configuramos el descifrador con la clave (a) y el vector de inicialización (b)
                    cipher = AES.new(a_bytes, AES.MODE_CBC, b_bytes)
                    decrypted = cipher.decrypt(c_bytes)

                    # Convertimos el resultado a formato hexadecimal (esta es la cookie original)
                    cookie_val = decrypted.hex().lower()

                    # Inyectamos la cookie autorizada en nuestra sesión de Python
                    sesion.cookies.set("__test", cookie_val, domain="kitsunepos.rf.gd", path="/")
                    print(r"[InfinityFree] ¡Cookie __test generada con éxito!")

                    # 2. Segundo intento: Ahora que tenemos la cookie instalada, volvemos a enviar el formulario
                    cabeceras["Accept"] = "application/json"  # Ahora sí pedimos el JSON limpio
                    response = sesion.post(
                        self.url_php,
                        data=datos_enviar,
                        headers=cabeceras,
                        timeout=10,
                        verify=False
                    )

            # Imprimimos en consola para verificar el resultado final limpio
            print("Código final del servidor:", response.status_code)
            print("Respuesta real del servidor:", response.text)

            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "error", "message": f"Error del servidor: {response.status_code}"}

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"No se pudo conectar al servidor: {e}"}