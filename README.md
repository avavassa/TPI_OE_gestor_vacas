# Chatbot para Gestión de Vacaciones

**Trabajo Práctico Integrador**

Este proyecto simula un asistente virtual de Recursos Humanos que automatiza todo el ciclo de solicitud de vacaciones: desde la validación del legajo hasta la actualización del saldo disponible, pasando por la aprobación o rechazo según la regla de negocio. El bot está implementado en Python con una máquina de estados finitos y manejo robusto de errores (caminos infelices), demostrando la integración entre el modelado de procesos BPMN y el código funcional.

El sistema fue desarrollado como parte del Trabajo Práctico Integrador de la materia **Organización Empresarial** de la **Tecnicatura Universitaria en Programación (TUP)** de la **Universidad Tecnológica Nacional (UTN)**.


## Características principales

- Máquina de estados finitos para gestionar la conversación
- Validación de legajos y saldos
- Manejo de errores (entradas inválidas, saldo insuficiente, legajo inexistente)
- Persistencia mediante archivo CSV (`empleados.csv`)
- Actualización automática del saldo tras cada solicitud aprobada
- Interfaz por consola


## Requisitos
- Python 3.8 o superior (recomendado)


## Instrucciones de ejecución

1. Clonar el repositorio (o descargar los archivos).
2. Ubicarse en la carpeta del proyecto.
3. Asegurarse de que el archivo empleados.csv esté en la misma carpeta.
4. Ejecutar:

´´´python3 bot_vacaciones.py´´
5. Seguir las instrucciones en pantalla. En cualquier momento se puede escribir salir para terminar.


## Integrantes

Georgina Daniela Maldonado

Ana Termignoni

Comision M26 - C1 - 26