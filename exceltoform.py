import pandas as pd
import requests
import threading
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# ====================================================================================
# 
#                EXECL A FORMULARIO  GOOGLE FORM
# 
# ==================================================================================


# Configuración para desactivar advertencias de SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Leer el archivo Excel
file_path = 'C:/Users/Usuario/Desktop/FormScript/SagoResponse2.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')

# URLs de Google Forms
GoogleURL = "https://docs.google.com/forms/d/e/1FAIpQLScz966YBiBixLERH6fPwZx0C7R1JQab9cjMB9fEWizWR20Zjg"
urlResponse = GoogleURL + "/formResponse"
urlReferer = GoogleURL + "/viewForm"

# Configurar la sesión con reintentos
session = requests.Session()
retry = Retry(connect=5, read=5, redirect=5, backoff_factor=0.1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Configuración de hilos
num_threads = 10

# Dividir los índices entre los hilos
indices = list(range(len(data)))
chunks = [indices[i::num_threads] for i in range(num_threads)]

# Función para enviar datos de formulario
def submit_form(indices_chunk):
    user_agent = {
        'Referer': urlReferer,
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/28.0.1500.52 Safari/537.36"
    }
    for idx in indices_chunk:
        current_form_data = {
            'entry.192444546': data.iloc[idx, 0],
            'entry.1094732297': data.iloc[idx, 1],
            'entry.2127124563': data.iloc[idx, 2],
            'entry.1504179541': data.iloc[idx, 3],
            'entry.412759122': data.iloc[idx, 4],
            'entry.1160674523': data.iloc[idx, 5],
            'entry.1615303137': data.iloc[idx, 6],
            'entry.881648527': data.iloc[idx, 7],
            'entry.621481633': data.iloc[idx, 8],
            'entry.1070856573': data.iloc[idx, 9],
            'entry.891880330': data.iloc[idx, 10],
            'entry.602056079': data.iloc[idx, 11],
            'entry.1310074750': data.iloc[idx, 12],
            'entry.1071564040': data.iloc[idx, 13],
            'entry.1323530264': data.iloc[idx, 14],
            'entry.1306273844': data.iloc[idx, 15],
            'entry.1393179684': data.iloc[idx, 16],
            'entry.1398139528': data.iloc[idx, 17],
            'entry.1342420244': data.iloc[idx, 18],
            'entry.285913729': data.iloc[idx, 19]
        }
        
        response = session.post(urlResponse, data=current_form_data, headers=user_agent, verify=False)
        print(f"Enviado: {idx}, Status: {response.status_code}")

# Crear y empezar los hilos
threads = []
for chunk in chunks:
    thread = threading.Thread(target=submit_form, args=(chunk,))
    threads.append(thread)
    thread.start()

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()

print("Todos los hilos han terminado.")