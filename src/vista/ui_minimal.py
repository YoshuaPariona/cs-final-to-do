"""
Este módulo proporciona una interfaz de usuario minimalista para la aplicación TodoApp.
Permite a los usuarios iniciar sesión, crear cuentas y gestionar sus tareas a través de un menú interactivo.
"""

from getpass import getpass
from datetime import datetime
from ..controlador.database.repository import Repository
from ..controlador.logica.models import Usuario, Tarea

# Instancia del repositorio
repo = Repository()

# Usuario actual en sesión
usuario_actual = None


def ui_minimal():
    """
    Interfaz de usuario principal para la aplicación TodoApp.
    Muestra un menú con opciones para iniciar sesión, crear una cuenta o salir.
    """
    while True:
        print("\n=== Bienvenido a TodoApp ===")
        print("1. Iniciar sesión")
        print("2. Crear cuenta")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            login()
        elif opcion == "2":
            crear_cuenta()
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")


def login():
    """
    Permite a un usuario iniciar sesión en la aplicación.
    Solicita el correo electrónico y la contraseña, y verifica las credenciales.
    """
    global usuario_actual
    print("\n--- Iniciar sesión ---")
    email = input("Email: ")
    contraseña = getpass("Contraseña: ")

    usuario = repo.get_user(email)
    if usuario and usuario.contraseña == contraseña:
        print(f"\n✅ Bienvenido {usuario.nombre}")
        usuario_actual = usuario
        menu_tareas()
    else:
        print("❌ Credenciales incorrectas.")


def crear_cuenta():
    """
    Permite a un nuevo usuario crear una cuenta en la aplicación.
    Solicita información como nombre, correo electrónico y contraseña, y guarda el nuevo usuario en el repositorio.
    """
    print("\n--- Crear nueva cuenta ---")
    nombre = input("Nombre: ")
    email = input("Email: ")
    contraseña = getpass("Contraseña: ")
    confirmar = getpass("Confirmar contraseña: ")

    if contraseña != confirmar:
        print("❌ Las contraseñas no coinciden.")
        return

    if repo.get_user(email):
        print("❌ El email ya está registrado.")
        return

    nuevo_usuario = Usuario(
        nombre=nombre,
        email=email,
        contraseña=contraseña,
        modoOscuro=False
    )

    if repo.save_user(nuevo_usuario):
        print("✅ Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
    else:
        print("❌ Error al crear cuenta.")


def menu_tareas():
    """
    Muestra el menú de tareas para el usuario actual.
    Proporciona opciones para ver, crear, modificar y eliminar tareas, así como cerrar sesión.
    """
    while True:
        print(f"\n--- Tareas de {usuario_actual.email} ---")
        print("1. Ver todas las tareas")
        print("2. Crear nueva tarea")
        print("3. Modificar tarea")
        print("4. Eliminar tarea")
        print("5. Eliminar todas las tareas")
        print("6. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_tareas()
        elif opcion == "2":
            crear_tarea()
        elif opcion == "3":
            modificar_tarea()
        elif opcion == "4":
            eliminar_tarea()
        elif opcion == "5":
            eliminar_todas_tareas()
        elif opcion == "6":
            print("Sesión cerrada.")
            break
        else:
            print("Opción no válida.")


def ver_tareas():
    """
    Muestra todas las tareas del usuario actual.
    """
    tareas = repo.get_user_tasks(usuario_actual.idUsuario)
    if not tareas:
        print("No tienes tareas registradas.")
        return

    print("\n--- Tus tareas ---")
    for tarea in tareas:
        fecha_v = tarea.fechaVencimiento.strftime("%d-%m-%Y") if tarea.fechaVencimiento else "N/A"
        print(f"[{tarea.idTarea}] {tarea.titulo} | Estado: {tarea.estado} | Vence: {fecha_v}")


def crear_tarea():
    """
    Permite al usuario crear una nueva tarea.
    Solicita información como título, descripción, fecha de vencimiento y prioridad.
    """
    print("\n--- Crear nueva tarea ---")
    titulo = input("Título: ")
    descripcion = input("Descripción: ")
    while True:
        fecha_str = input("Fecha de vencimiento (DD-MM-YYYY): ")
        try:
            fecha_vencimiento = datetime.strptime(fecha_str, "%d-%m-%Y")
            hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if fecha_vencimiento < hoy:
                print("❌ La fecha no puede ser antes que hoy. Inténtalo de nuevo.")
            else:
                break
        except ValueError:
            print("❌ Fecha no válida. Usa el formato DD-MM-YYYY.")

    prioridad = input("Prioridad (alta, media, baja): ").lower()
    estado = "pendiente"

    tarea = Tarea(
        titulo=titulo,
        descripcion=descripcion,
        fechaVencimiento=fecha_vencimiento,
        prioridad=prioridad,
        estado=estado,
        idUsuario=usuario_actual.idUsuario,
        fechaCreacion=datetime.utcnow()
    )

    if repo.save_task(tarea):
        print("✅ Tarea creada.")
    else:
        print("❌ Error al guardar la tarea.")


def modificar_tarea():
    """
    Permite al usuario modificar una tarea existente.
    Solicita el ID de la tarea y permite actualizar la descripción, estado y fecha de vencimiento.
    """
    tarea_id = input("ID de la tarea a modificar: ")
    tarea = buscar_tarea_por_id(tarea_id)
    if not tarea:
        return

    print(f"\nModificando tarea: {tarea.titulo}")
    nueva_desc = input("Nueva descripción (dejar en blanco para mantener): ")
    nuevo_estado = input("Nuevo estado (pendiente, en progreso, completada): ")
    nueva_fecha = input("Nueva fecha vencimiento (DD-MM-YYYY, opcional): ")

    if nueva_desc:
        tarea.descripcion = nueva_desc
    if nuevo_estado:
        tarea.estado = nuevo_estado
    if nueva_fecha:
        try:
            fecha_nueva = datetime.strptime(nueva_fecha, "%d-%m-%Y")
            hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if fecha_nueva < hoy:
                print("❌ La fecha no puede ser menor que hoy.")
                return
            tarea.fechaVencimiento = fecha_nueva
        except ValueError:
            print("❌ Fecha inválida. No se actualizó.")

    if repo.save_task(tarea):
        print("✅ Tarea actualizada.")
    else:
        print("❌ No se pudo actualizar la tarea.")


def eliminar_tarea():
    """
    Permite al usuario eliminar una tarea específica.
    Solicita el ID de la tarea y la elimina del repositorio.
    """
    tarea_id = input("ID de la tarea a eliminar: ")
    if repo.delete_task(int(tarea_id), usuario_actual.idUsuario):
        print("✅ Tarea eliminada.")
    else:
        print("❌ No se pudo eliminar la tarea.")


def eliminar_todas_tareas():
    """
    Permite al usuario eliminar todas sus tareas.
    Solicita confirmación antes de proceder con la eliminación.
    """
    confirmacion = input("¿Seguro que deseas eliminar TODAS tus tareas? (s/n): ")
    if confirmacion.lower() == "s":
        tareas = repo.get_user_tasks(usuario_actual.idUsuario)
        for tarea in tareas:
            repo.delete_task(tarea.idTarea, usuario_actual.idUsuario)
        print("✅ Todas las tareas fueron eliminadas.")
    else:
        print("❌ Cancelado.")


def buscar_tarea_por_id(tarea_id):
    """
    Busca una tarea por su ID en la lista de tareas del usuario actual.

    Parámetros:
    tarea_id (str): El ID de la tarea a buscar.

    Retorna:
    Tarea: La tarea encontrada o None si no se encuentra.
    """
    try:
        tarea_id = int(tarea_id)
        tareas = repo.get_user_tasks(usuario_actual.idUsuario)
        for tarea in tareas:
            if tarea.idTarea == tarea_id:
                return tarea
        print("❌ Tarea no encontrada.")
        return None
    except ValueError:
        print("❌ ID inválido.")
        return None
