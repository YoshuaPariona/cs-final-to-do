# To-Do App en Python

Una aplicación de gestión de tareas desarrollada con Python y SQLAlchemy. Permite a usuarios registrarse, iniciar sesión y gestionar sus tareas personales con diferentes prioridades y estados.

## Características

- Sistema de usuarios
   - Registro de usuarios
   - Inicio y cierre de sesión

- Gestión de tareas
   - Crear tareas con diferentes prioridades
   - Marcar tareas como completadas
   - Actualizar detalles de tareas
   - Eliminar tareas

-  Estados de tareas
   - New
   - En prograso
   - Completado

## Requisitos

- Python 3.8+
- SQLAlchemy
- SQLite3
- Pywebview

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/YoshuaPariona/cs-final-to-do.git
   cd cs-final-to-do
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta las pruebas:
   ```bash
   python -m pytest tests/run_all_tests
   ```

## Estructura del Proyecto

```
cs-final-to-do/
├── src/
│   ├── controlador/    # Controladores y lógica de negocio
│   ├── database/       # Capa de acceso a datos
│   ├── modelo/         # Modelos de dominio
│   └── vista/          # Interfaces de usuario
│      └── static/     # Diseño de interfaz en js
├── tests/              # Pruebas unitarias
├── main.py
├── README.md
└── requirements.txt
└── run_tests_with_coverage.bat
```

## Arquitectura

- Patrón MVC (Modelo-Vista-Controlador)
- SQLAlchemy como ORM
- Modelos de dominio independientes de la base de datos
- Pruebas unitarias con pytest

## Integrantes del equipo

| N° | Integrante |
|----|------------|
| 1 | Javier Curi Dayana Jessica |
| 2 | Pariona Inga Logan Yoshua Leonardo |
| 3 | Perez Ravelo Angel Simon |
| 4 | Quispe Medina Alexander Willy |
| 5 | Ricaldi Solis Maylon Amilcar |
| 6 | Urquizo Oré Francis Maxuel |

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.
