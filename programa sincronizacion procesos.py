# Integrantes: Rodrigo Collao, Martín Eluney, Maximiliano Saavedra, José Barraza, Leandro Borquez
# Técnica utilizada: Algoritmo del Panadero (Bakery Algorithm)

import multiprocessing
import time
import random
import os

# --- VARIABLES COMPARTIDAS (Estado del algoritmo) ---
# Usamos Array de multiprocessing para que los procesos compartan estos datos
MAX_PROCESOS = 2
eligiendo = multiprocessing.Array('b', [False] * MAX_PROCESOS)  # boolean
numero = multiprocessing.Array('i', [0] * MAX_PROCESOS)        # integer

def lock_bakery(i):
    """Protocolo de entrada a la sección crítica"""
    eligiendo[i] = True
    # El proceso toma un número mayor a los actuales
    numero[i] = max(list(numero)) + 1
    eligiendo[i] = False
    
    for j in range(MAX_PROCESOS):
        # Esperar si el proceso j está eligiendo un número
        while eligiendo[j]:
            pass
        # Esperar si el proceso j tiene un número menor o igual (prioridad por ID)
        while (numero[j] != 0 and 
               (numero[j] < numero[i] or (numero[j] == numero[i] and j < i))):
            pass

def unlock_bakery(i):
    """Protocolo de salida de la sección crítica"""
    numero[i] = 0

# --- LÓGICA DEL PROGRAMA ---

def calcular_factorial(n):
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res

def generador(id_proceso, archivo):
    """Parte 1: Genera datos [cite: 21]"""
    for _ in range(5):
        lock_bakery(id_proceso)
        try:
            val = random.randint(1, 10)
            with open(archivo, "a") as f:
                f.write(f"PROCESAR:{val}\n")
            print(f"[Generador] Escribió: {val}")
        finally:
            unlock_bakery(id_proceso)
        time.sleep(1)

def procesador(id_proceso, archivo):
    """Parte 2: Lee y escribe respuesta [cite: 21]"""
    procesados = 0
    while procesados < 5:
        lock_bakery(id_proceso)
        try:
            if os.path.exists(archivo):
                with open(archivo, "r") as f:
                    lineas = f.readlines()
                
                with open(archivo, "w") as f:
                    encontrado = False
                    for l in lineas:
                        if l.startswith("PROCESAR:"):
                            n = int(l.split(":")[1])
                            f.write(f"El factorial de: {n} es {calcular_factorial(n)}\n")
                            procesados += 1
                            encontrado = True
                        else:
                            f.write(l)
        finally:
            unlock_bakery(id_proceso)
        time.sleep(0.5 if not encontrado else 1.2)

if __name__ == "__main__":
    nombre_archivo = "resultados.txt"
    if os.path.exists(nombre_archivo): os.remove(nombre_archivo)

    # Crear procesos con sus respectivos IDs (0 y 1)
    p1 = multiprocessing.Process(target=generador, args=(0, nombre_archivo))
    p2 = multiprocessing.Process(target=procesador, args=(1, nombre_archivo))

    p1.start()
    p2.start()
    p1.join()
    p2.join()
