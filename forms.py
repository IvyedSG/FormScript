import requests
import random
import threading
import numpy as np
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Deshabilitar advertencias de SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# ====================================================================================
# 
#                RESPONDER AUTOMÁTICAMENTE GOOGLE FORM
# 
# ==================================================================================

# URL del formulario de Google Forms
GoogleURL = "https://docs.google.com/forms/d/e/1FAIpQLScz966YBiBixLERH6fPwZx0C7R1JQab9cjMB9fEWizWR20Zjg"

urlResponse = GoogleURL + "/formResponse"
urlReferer = GoogleURL + "/viewForm"


# IDs de las entradas encontradas en la consola después de enviar el formulario.
form_data = {
    'entry.192444546': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.1094732297': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.2127124563': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.1504179541': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.412759122': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.1160674523': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.1615303137': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.881648527': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.621481633': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.1070856573': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.891880330': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.602056079': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.1310074750': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.1071564040': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.1323530264': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.1306273844': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.1393179684': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.1398139528': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.1342420244': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
    'entry.285913729': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre']
}


# Configurar sesión con reintentos
session = requests.Session()
retry = Retry(connect=5, read=5, redirect=5, backoff_factor=0.1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Número de hilos que quieres ejecutar (No uses demasiados hilos)
num_threads = 10
chunks_per_thread = 30

threads = []
count_lock = threading.Lock()
count = 0
max_responses = 171


custom_weights = {
    'entry.192444546': [0.05, 0.1, 0.2, 0.3, 0.35],  # A veces
    'entry.1094732297': [0.05, 0.1, 0.2, 0.3, 0.35],  # Siempre
    'entry.2127124563': [0.05, 0.1, 0.2, 0.3, 0.35],  # Siempre
    'entry.1504179541': [0.05, 0.1, 0.2, 0.3, 0.35],  # A veces
    'entry.412759122': [0.05, 0.1, 0.2, 0.3, 0.35],  # Casi siempre
    'entry.1160674523': [0.05, 0.1, 0.2, 0.3, 0.35],  # Casi siempre
    'entry.1615303137': [0.05, 0.15, 0.25, 0.3, 0.25],  # Siempre
    'entry.881648527': [0.1, 0.1, 0.2, 0.25, 0.35],  # Casi nunca
    'entry.621481633': [0.1, 0.1, 0.2, 0.25, 0.35],  # Casi nunca
    'entry.1070856573': [0.05, 0.1, 0.15, 0.3, 0.4],  # Casi siempre
    'entry.891880330': [0.05, 0.15, 0.2, 0.25, 0.35],  # A veces
    'entry.602056079': [0.1, 0.1, 0.2, 0.3, 0.3],  # Siempre
    'entry.1310074750': [0.1, 0.15, 0.2, 0.25, 0.3],  # Siempre
    'entry.1071564040': [0.05, 0.15, 0.2, 0.25, 0.35],  # Casi nunca
    'entry.1323530264': [0.05, 0.1, 0.2, 0.25, 0.4],  # Casi siempre
    'entry.1306273844': [0.05, 0.1, 0.15, 0.25, 0.45],  # A veces
    'entry.1393179684': [0.05, 0.1, 0.2, 0.25, 0.4],  # A veces
    'entry.1398139528': [0.1, 0.15, 0.2, 0.25, 0.3],  # Casi nunca
    'entry.1342420244': [0.1, 0.15, 0.2, 0.25, 0.3],  # Casi siempre
    'entry.285913729': [0.05, 0.1, 0.15, 0.3, 0.4]   # Siempre
}

def submit_form(chunks_per_thread):
    global count
    user_agent = {
        'Referer': urlReferer,
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/28.0.1500.52 Safari/537.36"
    }
    while True:
        with count_lock:
            if count >= max_responses:
                return
            count += 1
            current_count = count

        random_form_data = {}
        for key, values in form_data.items():
            weights = custom_weights[key]
            random_form_data[key] = random.choices(values, weights=weights)[0]

        r = session.post(urlResponse, data=random_form_data, headers=user_agent, verify=False)
        print(f"Enviado: {current_count}")

# Crear y empezar los hilos
for _ in range(num_threads):
    thread = threading.Thread(target=submit_form, args=(chunks_per_thread,))
    threads.append(thread)
    thread.start()

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()

print("Todos los hilos han terminado.")
