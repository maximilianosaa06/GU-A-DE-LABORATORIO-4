# Grupo: 2 | Técnica: Algoritmo del panadero
# Integrantes: Rodrigo Collao, Martín Eluney, Maximiliano Saavedra, José Barraza, Leandro Borquez
# Asignatura: Sistemas Operativos | Universidad La Serena

import multiprocessing
import random
import time
import os

# ---------------------------------
# ALGORITMO DEL PANADERO
# ---------------------------------

MAX_PROCESOS = 2

eligiendo = multiprocessing.Array('b', [False] * MAX_PROCESOS)
numero = multiprocessing.Array('i', [0] * MAX_PROCESOS)


def lock_bakery(i):

    eligiendo[i] = True

    numero[i] = max(numero) + 1

    eligiendo[i] = False

    for j in range(MAX_PROCESOS):

        if j == i:
            continue

        while eligiendo[j]:
            pass

        while (
            numero[j] != 0 and
            (
                numero[j] < numero[i] or
                (numero[j] == numero[i] and j < i)
            )
        ):
            pass


def unlock_bakery(i):
    numero[i] = 0


# ---------------------------------
# FACTORIAL
# ---------------------------------

def calcular_factorial(n):

    resultado = 1

    for i in range(2, n + 1):
        resultado *= i

    return resultado


# ---------------------------------
# PROCESO GENERADOR
# ---------------------------------

def generador(id_proceso, archivo):

    for _ in range(5):

        n = random.randint(1, 10)

        lock_bakery(id_proceso)

        try:

            with open(archivo, "a") as f:

                # Escribe línea incompleta
                f.write(f"El factorial de: {n} es:\n")

            print(f"[Generador] Número generado: {n}")

        finally:
            unlock_bakery(id_proceso)

        time.sleep(1)


# ---------------------------------
# PROCESO PROCESADOR
# ---------------------------------

def procesador(id_proceso, archivo):

    procesados = 0

    while procesados < 5:

        lock_bakery(id_proceso)

        try:

            if not os.path.exists(archivo):
                continue

            with open(archivo, "r") as f:
                lineas = f.readlines()

            modificado = False

            for i in range(len(lineas)):

                linea = lineas[i].strip()

                # Buscar líneas incompletas
                if linea.endswith("es:"):

                    partes = linea.split()

                    n = int(partes[3])

                    factorial = calcular_factorial(n)

                    # Completar línea
                    lineas[i] = (
                        f"El factorial de: {n} es: {factorial}\n"
                    )

                    print(
                        f"[Procesador] "
                        f"Factorial calculado de {n}"
                    )

                    procesados += 1
                    modificado = True

                    break

            # Reescribir archivo actualizado
            if modificado:

                with open(archivo, "w") as f:
                    f.writelines(lineas)

        finally:
            unlock_bakery(id_proceso)

        time.sleep(0.5)


# ---------------------------------
# MAIN
# ---------------------------------

if __name__ == "__main__":

    archivo = "resultados.txt"

    # Crear archivo automáticamente
    with open(archivo, "w") as f:
        pass

    p1 = multiprocessing.Process(
        target=generador,
        args=(0, archivo)
    )

    p2 = multiprocessing.Process(
        target=procesador,
        args=(1, archivo)
    )

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("\nPrograma terminado correctamente.")


# --- RESPUESTAS A LA GUÍA N°4 LABORATORIO ---
# a) Sincronización: Coordinación de procesos para evitar competencia por recursos.
# b) Semáforo: Variable entera usada para controlar el acceso a recursos mediante señales.
# c) Mutex: Mecanismo de exclusión mutua para asegurar que solo un hilo acceda a un recurso.
# d) Monitor: Estructura de alto nivel que encapsula datos y funciones con exclusión mutua implícita.
# e) Variable condicional: Mecanismo para que los procesos esperen hasta que se cumpla una condición.
# f) Conclusión Panadero: Es un método de software puro que no depende de hardware, a diferencia de los Locks.
