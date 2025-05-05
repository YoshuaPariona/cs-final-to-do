from src.logica.usuarios import registrar_usuario, login
from src.logica.tareas import crear_tarea, ver_tareas_usuario, cambiar_estado_tarea, crear_grupo, ver_grupos
from src.database.db import init_db
from datetime import datetime

def menu_usuario(idUsuario):
    while True:
        print("\n--- MENÚ DE USUARIO ---")
        print("1. Ver mis tareas")
        print("2. Crear tarea")
        print("3. Cambiar estado de una tarea")
        print("4. Crear grupo")
        print("5. Ver grupos")
        print("6. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            ver_tareas_usuario(idUsuario)
        elif opcion == "2":
            titulo = input("Título: ")
            descripcion = input("Descripción: ")
            fecha_venc = input("Fecha de vencimiento (YYYY-MM-DD): ")
            prioridad = input("Prioridad (baja/media/alta): ").lower()
            estado = input("Estado (pendiente/completada): ").lower()
            tipo = input("Tipo (texto, checklist, etc.): ")
            crear_tarea(titulo, descripcion, fecha_venc, prioridad, estado, tipo, idUsuario)
        elif opcion == "3":
            idTarea = int(input("ID de la tarea: "))
            nuevo_estado = input("Nuevo estado (pendiente/completada): ").lower()
            cambiar_estado_tarea(idTarea, nuevo_estado)
        elif opcion == "4":
            nombre_grupo = input("Nombre del grupo: ")
            crear_grupo(nombre_grupo)
        elif opcion == "5":
            ver_grupos()
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

def main():
    init_db()
    while True:
        print("\n--- BIENVENIDO ---")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            email = input("Email: ")
            contraseña = input("Contraseña: ")
            modo = input("¿Modo oscuro activado? (s/n): ").lower() == "s"
            registrar_usuario(nombre, email, contraseña, modo)
        elif opcion == "2":
            email = input("Email: ")
            contraseña = input("Contraseña: ")
            idUsuario = login(email, contraseña)
            if idUsuario:
                menu_usuario(idUsuario)
        elif opcion == "3":
            print("¡Adiós!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
