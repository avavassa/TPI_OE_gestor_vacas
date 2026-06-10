# Trabajo Práctico Integrador de la materia Organización Empresarial - TUP

# ==========================================
# SIMULACIÓN DE BOT DE GESTIÓN DE VACACIONES
# CON MÁQUINA DE ESTADOS Y MANEJO DE ERRORES
# ==========================================

import csv
import os

# Archivo CSV utilizado como mecanismo de persistencia
EMPLEADOS_CSV = "empleados.csv"

# ----------------- FUNCIONES DE PERSISTENCIA --------------
def leer_empleados():
    """ 
    Lee contenido de csv empleados. 
    """
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

def actualizar_saldo(empleados_db):
    """
    Guarda los saldos actualizados en empleados.csv
    """
    with open(EMPLEADOS_CSV, mode='w', newline='', encoding='utf-8') as f:
        campos = ['id_empleado', 'nombre', 'saldo']

        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

        for id_emp, datos in empleados_db.items():
            writer.writerow({
                'id_empleado': id_emp,
                'nombre': datos['nombre'],
                'saldo': datos['saldo']
            })

# ------------------ FUNCIONES DE NEGOCIO ------------------
def validar_legajo(legajo, empleados):
    """Verifica si el legajo existe. Devuelve los datos del empleado o None."""
    if legajo in empleados_db:
        return empleados_db[legajo]
    return None

def validar_dias(entrada):
    """
    Verifica que la cantidad de días sea un número entero positivo.
    Devuelve el número o None si es inválido.
    """
    try:
        dias = int(entrada)

        if dias <= 0:
            return None

        return dias

    except ValueError:
        return None

def procesar_solicitud(empleado, dias_pedidos):
    """
    Valida si el empleado tiene saldo suficiente.
    Devuelve True o False.
    """
    if dias_pedidos <= empleado['saldo']:
        empleado['saldo'] -= dias_pedidos
        return True

    return False

# -------------------- PROGRAMA PRINCIPAL ------------------

empleados_db = leer_empleados()

def chatbot_vacaciones():
    print("==================================================")
    print("--- ASISTENTE VIRTUAL DE RRHH (Simulador Bot) ---")
    print("Instrucciones: Escriba 'salir' en cualquier momento para finalizar.")
    print("==================================================")
    
    # Inicialización de Máquina de Estados
    # Estados posibles: 'INICIO', 'VALIDANDO_LEGAJO', 'SOLICITANDO_DIAS', 'FIN'
    estado = 'INICIO'
    legajo_activo = None

    while estado != 'FIN':

        # ==========================================
        # ESTADO: INICIO
        # ==========================================
        
        if estado == 'INICIO': # Mensaje inicial
            print("\nBot: ¡Hola! Soy el asistente de RRHH. Por favor, ingrese su número de legajo para comenzar:")
            estado = 'VALIDANDO_LEGAJO' # Estado cambia después del mensaje inicial
        
        # ==========================================
        # ESTADO: VALIDANDO_LEGAJO
        # ==========================================

        elif estado == 'VALIDANDO_LEGAJO': # Solicita entrada del usuario
            entrada = input("Usuario: ").strip()
            
            if entrada.lower() == 'salir': # Si el usuario ingresa 'salir' el estado cambia a 'FIN'
                estado = 'FIN'
                print("Bot: Gracias por utilizar el asistente. ¡Hasta luego!")
                continue
                
            # Validación de existencia de legajo
            empleado = validar_legajo(entrada, empleados_db) # Llama a función de validación de legajo

            if empleado: # Si el legajo existe, la función devuelve el empleado
                legajo_activo = entrada
                print(f"Bot: Bienvenido/a {empleado['nombre']}. Legajo verificado con éxito.")
                print(f"Bot: Actualmente cuenta con un saldo de {empleado['saldo']} días de vacaciones disponibles.")

                if empleado['saldo'] > 0: # Pregunta cuántos días sólo si el usuario tiene saldo
                    print("Bot: ¿Cuántos días de vacaciones desea solicitar?")
                    estado = 'SOLICITANDO_DIAS' # Estado cambia a 'SOLICITANDO_DIAS'
                else: # Camino infeliz: saldo igual a 0
                    print("Bot: Usted no posee días disponibles en este período. El proceso ha finalizado.")
                    estado = 'INICIO' # Vuelve al estado 'INICIO'
            else: # Camino infeliz: la validación de legajo devolvió None
                print("Bot: [ERROR] El legajo ingresado no existe en nuestros registros. Inténtelo de nuevo.")

        # ==========================================
        # ESTADO: SOLICITANDO_DIAS
        # ==========================================

        elif estado == 'SOLICITANDO_DIAS': # Espera entrada de días del usuario
            entrada = input("Usuario: ").strip()
            
            if entrada.lower() == 'salir':
                estado = 'FIN'
                print("Bot: Solicitud cancelada. Gracias por comunicarse.")
                continue
                
            dias_pedidos = validar_dias(entrada) # Llama a la función de validar entrada de días

            if dias_pedidos is None:
                print("Bot: [ERROR] Debe ingresar un número entero mayor a cero.")
                continue
                
            # Decisión Lógica: ¿Tiene saldo suficiente? (Gateway del BPMN)
            empleado = empleados_db[legajo_activo]

            solicitud_aprobada = procesar_solicitud(empleado,dias_pedidos) # Llama a función de procesar_solicitud

            if solicitud_aprobada: # Camino Feliz: solicitud aprobada                
                actualizar_saldo(empleados_db) # Se llama a la función actualizar_saldo
                print(f"Bot: ¡Solicitud aprobada con éxito!")
                print(f"Bot: Se han descontado {dias_pedidos} días. Su nuevo saldo es de {empleado['saldo']} días.")
                print("==================================================")
                estado = 'INICIO' # Retorna al inicio para atender nuevas consultas
            else: # Camino Infeliz: Saldo insuficiente                
                print(f"Bot: [RECHAZADO] No puede solicitar {dias_pedidos} días. Su saldo actual es de solo {empleado['saldo']} días.")
                print("Bot: Ingrese una cantidad menor o escriba 'salir'.")
                # Permanece en el estado SOLICITANDO_DIAS

# Ejecución del programa simulador
if __name__ == "__main__":
    chatbot_vacaciones()
