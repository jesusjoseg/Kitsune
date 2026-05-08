import subprocess
import hashlib
import requests
import platform
import os
from datetime import datetime, timedelta

class SeguridadDemo:
    def __init__(self):
        self.app_data=os.path.join(os.environ['LOCALAPPDATA'],"KITSUNE_DEMO")
        self.rastro_file = os.path.join(self.app_data,"win_log_sys.dat")
        self.url_php="http://localhost:3000/Php/VerificarDemo.php"
    def Obtener_hwid(self):
        try:
            m_board=subprocess.check_output('wmic baseboard get serialnumber',shell=True).decode().split('\n')[1].strip()
            cpu=subprocess.check_output('wmic cpu get processorid',shell=True).decode().split('\n')[1].strip()
            raw_id =f"Kitsune-{m_board}-{cpu}"
            return hashlib.sha256(raw_id.encode()).hexdigest()[:16].upper()
        except:
            return "ID_Unknowk"

    def Gestiona_rastro_local(self):
        if not os.path.exists(self.app_data):
            os.makedirs(self.app_data)
            os.system(f'attrib +h "{self.app_data}')
        if not os.path.exists(self.rastro_file):
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            with open(self.rastro_file,'w') as f:
                f.write(fecha_hoy)
            return fecha_hoy
        else:
            with open(self.rastro_file,'r') as f:
                return f.read().strip()
    def Verifica_estado(self):
        fecha_instala_str=self.Gestiona_rastro_local()
        fecha_instala = datetime.strptime(fecha_instala_str,'%Y-%m-%d')
        dia_usados = (datetime.now() - fecha_instala).days
        dias_restantes = 30- dia_usados

        datos={
            "hwid":self.Obtener_hwid(),
            "NombreDePc": platform.node(),
            "fecha_instala": fecha_instala,
            "Version": "V1.0_Demos",
            "Dias_Restantes": dias_restantes
        }
        return datos