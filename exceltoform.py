import pandas as pd
import requests
import threading
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 
# ====================================================================================
# 
#                PASAR RESULTADOS DE EXCEL A GOOGLE FORMS
# 
# ==================================================================================
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Leer el archivo Excel
file_path = 'C:/Users/pc1/Desktop/Google-Form-Auto-Spammmer/fortw.xlsx'  # Actualiza esta ruta según sea necesario
data = pd.read_excel(file_path, sheet_name='Hoja1')

# URL del formulario de Google Forms
GoogleURL = "https://docs.google.com/forms/d/e/1FAIpQLSfOLbJv9obgnbEFVwLJ2LxBOZ5dqQum_caRsjEV4Uvx6EvPNA"

urlResponse = GoogleURL + "/formResponse"
urlReferer = GoogleURL + "/viewForm"

# Configurar sesión con reintentos
session = requests.Session()
retry = Retry(connect=5, read=5, redirect=5, backoff_factor=0.1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Número de hilos que quieres ejecutar (No uses demasiados hilos)
num_threads = 10
chunks_per_thread = 25

threads = []
count_lock = threading.Lock()
count = 0
max_responses = len(data)  # Número de respuestas en el archivo Excel

def submit_form():
    global count
    user_agent = {
        'Referer': urlReferer,
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/28.0.1500.52 Safari/537.36"
    }
    while True:
        with count_lock:
            if count >= max_responses:
                return
            current_count = count
            count += 1

        # Crear el diccionario de datos para enviar
        current_form_data = {
            'entry.753621689': data.iloc[current_count, 0],
            'entry.425425378': data.iloc[current_count, 1],
            'entry.960741044': data.iloc[current_count, 2],
            'entry.1367523984': data.iloc[current_count, 3],
            'entry.98974128': data.iloc[current_count, 4],
            'entry.691319681': data.iloc[current_count, 5],
            'entry.475947805': data.iloc[current_count, 6],
            'entry.608321832': data.iloc[current_count, 7],
            'entry.1052439477': data.iloc[current_count, 8],
            'entry.331239872': data.iloc[current_count, 9],
            'entry.1678953737': data.iloc[current_count, 10],
            'entry.218449170': data.iloc[current_count, 11],
            'entry.1923756445': data.iloc[current_count, 12],
            'entry.443068663': data.iloc[current_count, 13],
            'entry.1720614532': data.iloc[current_count, 14],
            'entry.1172391505': data.iloc[current_count, 15],
            'entry.172492878': data.iloc[current_count, 16],
            'entry.924726708': data.iloc[current_count, 17],
            'entry.733229067': data.iloc[current_count, 18],
            'entry.1436234044': data.iloc[current_count, 19],
            'entry.1188828452': data.iloc[current_count, 20],
            'entry.609794076': data.iloc[current_count, 21],
            'entry.1054996394': data.iloc[current_count, 22],
            'entry.622165299': data.iloc[current_count, 23],
            'entry.690602917': data.iloc[current_count, 24],
            'entry.1760425858': data.iloc[current_count, 25],
            'entry.1594747963': data.iloc[current_count, 26],
            'entry.1947112039': data.iloc[current_count, 27],
            'entry.749220870': data.iloc[current_count, 28],
            'entry.1239973735': data.iloc[current_count, 29],
            'entry.1328910268': data.iloc[current_count, 30],
            'entry.879348836': data.iloc[current_count, 31],
            'entry.565038232': data.iloc[current_count, 32],
        }

        r = session.post(urlResponse, data=current_form_data, headers=user_agent, verify=False)
        print(f"Enviado: {current_count}")

# Crear y empezar los hilos
for _ in range(num_threads):
    thread = threading.Thread(target=submit_form)
    threads.append(thread)
    thread.start()

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()

print("Todos los hilos han terminado.")