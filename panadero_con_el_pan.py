import threading
import time
import random

# --- CONFIGURACIÓN ---
N_HILOS = 5
contador_compartido = 0

# Estructuras de datos delvs algoritmo
eligiendo = [False] * N_HILOS
numero = [0] * N_HILOS

def algoritmo_panadero(id_hilo):
    global contador_compartido
    
    for _ in range(2):  # Cada hilo intentará entrar 2 veces a la sección crítica
        
        # 1. PROTOCOLO DE ENTRADA: Tomar un número
        # -------------------------------------------------------
        eligiendo[id_hilo] = True
        print(f"  [Hilo {id_hilo}] Eligiendo número...")
        
        # El ticket es el máximo actual + 1
        numero[id_hilo] = max(numero) + 1
        print(f"  [Hilo {id_hilo}] Mi ticket es: {numero[id_hilo]}")
        
        eligiendo[id_hilo] = False
        
        # 2. PROTOCOLO DE ESPERA: El "Turno"
        # -------------------------------------------------------
        for j in range(N_HILOS):
            # Esperar si el hilo j está eligiendo número
            while eligiendo[j]:
                pass 
            
            # Esperar si el hilo j tiene un número menor
            # O si tienen el mismo número, esperar si j tiene un ID menor (Desempate)
            while (numero[j] != 0) and (
                (numero[j] < numero[id_hilo]) or 
                (numero[j] == numero[id_hilo] and j < id_hilo)
            ):
                # Espera activa (Busy waiting)
                pass

        # 3. SECCIÓN CRÍTICA
        # -------------------------------------------------------
        print(f"===> Hilo {id_hilo} ENTRA a la Sección Crítica (Ticket {numero[id_hilo]})")
        
        # Simulamos una operación sobre un recurso compartido
        temp = contador_compartido
        time.sleep(random.uniform(0.1, 0.4)) # Simulamos carga de trabajo
        contador_compartido = temp + 1
        
        print(f"<=== Hilo {id_hilo} SALE de la Sección Crítica. Contador: {contador_compartido}")

        # 4. PROTOCOLO DE SALIDA
        # -------------------------------------------------------
        numero[id_hilo] = 0 
        
        # Sección no crítica
        time.sleep(random.uniform(0.1, 0.5))

# --- EJECUCIÓN DEL SIMULADOR ---
if __name__ == "__main__":
    print(f"Iniciando Algoritmo del Panadero con {N_HILOS} hilos...")
    hilos = []
    
    for i in range(N_HILOS):
        t = threading.Thread(target=algoritmo_panadero, args=(i,))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    print(f"\nProceso terminado. Valor final del contador: {contador_compartido}")
    print(f"Valor esperado: {N_HILOS * 2}")