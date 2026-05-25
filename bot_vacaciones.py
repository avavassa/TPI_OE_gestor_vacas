# TPI_OE_gestor_vacas
# Trabajo Práctico Integrador de la materia Organización Empresarial - TUP

# ==========================================
# SIMULACIÓN DE BOT DE GESTIÓN DE VACACIONES
# CON MÁQUINA DE ESTADOS Y MANEJO DE ERRORES
# ==========================================

import csv
import os

# Base de datos simulada en memoria (Persistencia en Diccionario)
# Archivos CSV
EMPLEADOS_CSV = "empleados.csv"
SOLICITUDES_CSV = "solicitudes_vacaciones.csv"

# ------------------ Funciones de CSV ------------------
def leer_empleados():
    empleados = {}
    if not os.path.exists(EMPLEADOS_CSV):
        print(f"Error: No se encuentra el archivo {EMPLEADOS_CSV}")
        return empleados
    with open(EMPLEADOS_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                id_emp = (row['id_empleado'])
                nombre = row['nombre']
                dias = int(row['saldo'])
                empleados[id_emp] = {'nombre': nombre, 'saldo': dias}
            except (ValueError, KeyError):
                continue
    return empleados


empleados_db = leer_empleados()

def chatbot_vacaciones():
    print("==================================================")
    print("--- ASISTENTE VIRTUAL DE RRHH (Simulador Bot) ---")
    print("Instrucciones: Escriba 'salir' en cualquier momento para finalizar.")
    print("==================================================")
    
    # Inicialización de Estados
    # Estados posibles: 'INICIO', 'VALIDANDO_LEGAJO', 'SOLICITANDO_DIAS', 'FIN'
    estado = 'INICIO'
    legajo_activo = None

    while estado != 'FIN':
        
        if estado == 'INICIO':
            print("\nBot: ¡Hola! Soy el asistente de RRHH. Por favor, ingrese su número de legajo para comenzar:")
            estado = 'VALIDANDO_LEGAJO'
            
        elif estado == 'VALIDANDO_LEGAJO':
            entrada = input("Usuario: ").strip()
            
            if entrada.lower() == 'salir':
                estado = 'FIN'
                print("Bot: Gracias por utilizar el asistente. ¡Hasta luego!")
                continue
                
            # Camino Feliz / Infeliz: Validación de existencia de legajo
            if entrada in empleados_db:
                legajo_activa = entrada
                empleado = empleados_db[legajo_activa]
                print(f"Bot: Bienvenido/a {empleado['nombre']}. Verificado con éxito.")
                print(f"Bot: Actualmente cuenta con un saldo de {empleado['saldo']} días de vacaciones disponibles.")
                
                if empleado['saldo'] > 0:
                    print("Bot: ¿Cuántos días de vacaciones desea solicitar?")
                    estado = 'SOLICITANDO_DIAS'
                else:
                    print("Bot: Usted no posee días disponibles en este período. El proceso ha finalizado.")
                    estado = 'INICIO' # Reinicia el flujo para otro usuario
            else:
                # Camino Infeliz: Legajo inexistente
                print("Bot: [ERROR] El legajo ingresado no existe en nuestros registros. Inténtelo de nuevo.")
                # Permanece en el estado VALIDANDO_LEGAJO

        elif estado == 'SOLICITANDO_DIAS':
            entrada = input("Usuario: ").strip()
            
            if entrada.lower() == 'salir':
                estado = 'FIN'
                print("Bot: Solicitud cancelada. Gracias por comunicarse.")
                continue
                
            # Camino Infeliz: El usuario ingresa texto en lugar de números (Crash Prevention)
            try:
                dias_pedidos = int(entrada)
            except ValueError:
                print("Bot: [ERROR] Por favor, introduzca un valor numérico válido (ej. 5).")
                continue # Permanece en el mismo estado pidiendo el dato
                
            # Camino Infeliz: Pide números negativos o cero
            if dias_pedidos <= 0:
                print("Bot: [ERROR] La cantidad de días debe ser mayor a cero.")
                continue
                
            # Decisión Lógica: ¿Tiene saldo suficiente? (Gateway del BPMN)
            empleado = empleados_db[legajo_activa]
            if dias_pedidos <= empleado['saldo']:
                # Camino Feliz: Descontar días y actualizar persistencia en memoria
                empleado['saldo'] -= dias_pedidos
                print(f"Bot: ¡Solicitud aprobada con éxito!")
                print(f"Bot: Se han descontado {dias_pedidos} días. Su nuevo saldo es de {empleado['saldo']} días.")
                print("==================================================")
                estado = 'INICIO' # Retorna al inicio para atender nuevas consultas
            else:
                # Camino Infeliz: Saldo insuficiente
                print(f"Bot: [RECHAZADO] No puede solicitar {dias_pedidos} días. Su saldo actual es de solo {empleado['saldo']} días.")
                print("Bot: Ingrese una cantidad menor o escriba 'salir'.")
                # Permanece en el estado SOLICITANDO_DIAS

# Ejecución del programa simulador
if __name__ == "__main__":
    chatbot_vacaciones()
