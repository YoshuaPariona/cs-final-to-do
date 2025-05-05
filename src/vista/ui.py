def imprimir_tareas_agrupadas(tareas_por_grupo):
    for grupo, tareas in tareas_por_grupo.items():
        print(f"\nGrupo: {grupo}")
        for i, (titulo, descripcion) in enumerate(tareas, start=1):
            print(f"  {i}. {titulo}: {descripcion}")

def mostrar_tareas_para_seleccion(tareas):
    print("\nTareas disponibles:")
    for tarea in tareas:
        print(f"{tarea[0]}. {tarea[1]}")

def mostrar_grupos_para_seleccion(grupos):
    print("\nGrupos disponibles:")
    print("0. Sin grupo")
    for grupo in grupos:
        print(f"{grupo[0]}. {grupo[1]}")
