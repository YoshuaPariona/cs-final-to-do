from src.logica import db_handler
from src.vista import ui

def main():
    while True:
        print("\nMenú principal:")
        print("1. Mostrar tareas")
        print("2. Agrupar tarea (cambiar grupo)")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            tareas = db_handler.mostrar_tareas()
            ui.imprimir_tareas_agrupadas(tareas)

        elif opcion == "2":
            tareas = db_handler.obtener_tareas()
            ui.mostrar_tareas_para_seleccion(tareas)
            id_tarea = int(input("Selecciona el ID de la tarea: "))

            grupos = db_handler.obtener_grupos()
            ui.mostrar_grupos_para_seleccion(grupos)
            id_grupo_input = input("Selecciona el ID del grupo (0 para sin grupo): ")

            id_grupo = int(id_grupo_input) if id_grupo_input != "0" else None
            db_handler.cambiar_grupo_tarea(id_tarea, id_grupo)
            print("Grupo actualizado con éxito.")

        elif opcion == "3":
            print("Saliendo...")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
