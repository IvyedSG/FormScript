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
GoogleURL = "https://docs.google.com/forms/d/e/1FAIpQLSfeF4YtDttz2clrFb3Rusa6sXGU4DfWEPzJcpXHeLa_BT3AEg"

urlResponse = GoogleURL + "/formResponse"
urlReferer = GoogleURL + "/viewForm"

# IDs de las entradas encontradas en la consola después de enviar el formulario.
form_data = {
    'entry.753621689': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 4. Casi Siempre
    'entry.425425378': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 4. Casi Siempre
    'entry.960741044': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 4. Casi Siempre
    'entry.1367523984': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 3. A Veces
    'entry.98974128': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],    # 2. Casi Nunca
    'entry.691319681': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],    # 2. Casi Nunca
    'entry.475947805': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 2. Casi Nunca
    'entry.608321832': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 3. A Veces
    'entry.1052439477': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 2. Casi Nunca
    'entry.331239872': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 2. Casi Nunca
    'entry.1678953737': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 3. A Veces
    'entry.218449170': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 4. Casi Siempre
    'entry.1923756445': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 3. A Veces
    'entry.443068663': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 3. A Veces
    'entry.1720614532': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 3. A Veces
    'entry.1172391505': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 3. A Veces
    'entry.172492878': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 4. Casi Siempre
    'entry.924726708': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 4. Casi Siempre
    'entry.733229067': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 4. Casi Siempre
    'entry.1436234044': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 3. A Veces
    'entry.1188828452': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 4. Casi Siempre
    'entry.609794076': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 3. A Veces
    'entry.1054996394': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 3. A Veces
    'entry.622165299': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 2. Casi Nunca
    'entry.690602917': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 4. Casi Siempre
    'entry.1760425858': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 4. Casi Siempre
    'entry.1594747963': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 3. A Veces
    'entry.1947112039': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 4. Casi Siempre
    'entry.749220870': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 3. A Veces
    'entry.1239973735': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 2. Casi Nunca
    'entry.1328910268': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],  # 4. Casi Siempre
    'entry.879348836': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre'],   # 4. Casi Siempre
    'entry.565038232': ['1. Nunca', '2. Casi Nunca', '3. A Veces', '4. Casi Siempre', '5. Siempre']    # 3. A Veces
}


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
max_responses = 10

# Pesos personalizados para cada entry
custom_weights = {
    'entry.753621689': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192],  #1
    'entry.425425378': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192],  #2
    'entry.960741044': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192],  #3
    'entry.1367523984': [0.1060, 0.2185, 0.2980, 0.2815, 0.0960], #4
    'entry.98974128': [0.1159, 0.3046, 0.3079, 0.1854, 0.0861],   #5
    'entry.691319681': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192],  #6
    'entry.475947805': [0.0993, 0.1821, 0.3245, 0.2914, 0.1026],  #7
    'entry.608321832': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192], #8
    'entry.1052439477': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192], #9
    'entry.331239872': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192], #10
    'entry.1678953737': [0.1225, 0.2252, 0.2815, 0.2483, 0.1225], #11
    'entry.218449170': [0.1126, 0.1788, 0.3377, 0.2881, 0.0828],  #12
    'entry.1923756445': [0.0993, 0.1821, 0.3245, 0.2914, 0.1026], #13
    'entry.443068663': [0.1225, 0.2252, 0.2815, 0.2483, 0.1225],  #14
    'entry.1720614532': [0.1126, 0.1722, 0.2715, 0.3179, 0.1358], #15
    'entry.1172391505': [0.1126, 0.1788, 0.3377, 0.2881, 0.0828], #16
    'entry.172492878': [0.1126, 0.1788, 0.3377, 0.2881, 0.0828], #17
    'entry.924726708': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192],  #18
    'entry.733229067': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192],  #19
    'entry.1436234044': [0.0993, 0.1821, 0.3245, 0.2914, 0.1026], #20
    'entry.1188828452': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192], #21
    'entry.609794076': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192], #22
    'entry.1054996394': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192], #23
    'entry.622165299': [0.1225, 0.2252, 0.2815, 0.2483, 0.1225],  #24
    #==========================2DA VARIABLE====================
    'entry.690602917': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192],  #25
    'entry.1760425858': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192], #26
    'entry.1594747963': [0.0993, 0.1821, 0.3245, 0.2914, 0.1026], #27
    'entry.1947112039': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192], #28
    'entry.749220870': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192],  #29
    'entry.1239973735': [0.0993, 0.1821, 0.3245, 0.2914, 0.1026], #30
    'entry.1328910268': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192], #31
    'entry.879348836': [0.0629, 0.1954, 0.2616, 0.3609, 0.1192], #32
    'entry.565038232': [0.1225, 0.2252, 0.2815, 0.2483, 0.1225] #33
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
