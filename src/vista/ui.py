from src.logica.tareas import crear_grupo, listar_grupos

def menu_principal():
    while True:
        print("1. Crear Grupo")
        print("2. Ver Grupos")
        print("0. Salir")
        op = input("Opción: ")

        if op == "1":
            nombre = input("Nombre del grupo: ")
            crear_grupo(nombre)
        elif op == "2":
            grupos = listar_grupos()
            for g in grupos:
                print(f"{g[0]} - {g[1]}")
        elif op == "0":
            break