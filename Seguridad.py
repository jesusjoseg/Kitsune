import subprocess
import hashlib
import os
from datetime import datetime ,date

from sqlalchemy.sql.operators import exists


class SeguridadDemo:
    def __init__(self):
        self.app_data = os.path.join(os.environ['LOCALAPPDATA'],"KITSUNE_DEMO")
        self.rastro_file =os.path.join(self.app_data,"win_log_sys.dat")
        self.dias_Maximo= 30

    def Obtener_hwid(self):
        try:
            comondo_baseboard= 'powershell "GET-CimInstance Win32_BaseBoard | Select-Object -ExpandProperty SerialNumber"'
            comondo_cpu= 'powershell "Get-CimInstance Win32_Processor | Select-Object -ExpandProperty ProcessorId"'

            m_board = subprocess.check_output((comondo_baseboard),shell=True).decode().strip()
            cpu = subprocess.check_output((comondo_cpu),shell=True).decode().strip()
            raw_id=f"Kitsune-{m_board}-{cpu}"
            return hashlib.sha256(raw_id.encode()).hexdigest()[:16].upper()
        except Exception as e:
            print(f"Error obteniendo Hwid{e}")
            return "HWID_UNKNOWN"

    def Verficar_Licencia(self,token_local =None):
        try:
            os.makedirs(self.app_data, exist_ok=True)
            if os.path.exists(self.rastro_file):
                with open(self.rastro_file,"r") as f:
                    fecha_guardada_texto= f.read().strip()
                fecha_istalacion = datetime.strptime(fecha_guardada_texto,"%d/%m/%Y").date()
                fecha_actual =date.today()
                dias_pasado = (fecha_actual-fecha_istalacion).days
                dias_restante = self.dias_Maximo - dias_pasado
                if dias_restante <= 0:
                    return {
                        "status": "success",
                        "message": "Ecositemas Demo operadores de forma local.",
                        "dia": dias_restante
                    }
                else:
                    return {
                        "status": "success",
                        "message": "Ecosistema de forma local.",
                        "dia": dias_restante
                    }
            else:
                fecha_hoy = date.today().strftime("%d/%m/%Y")
                with open(self.rastro_file,"w") as f:
                    f.write(fecha_hoy)
                if os.name == "nt":
                    subprocess.check_call(["attrib", "+H", self.rastro_file])
                return {
                    "status": "success",
                    "message": "Periodo de prueba inicializado correctamente.",
                    "dia": self.dias_Maximo
                }
        except Exception as e:

            return{
                "status": "success",
                "message": f"Error critico de consistencia local:{e}",
                "dia":0
            }