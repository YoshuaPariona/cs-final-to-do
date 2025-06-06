# To-Do App en Python

Una aplicación de gestión de tareas desarrollada con Python y SQLAlchemy. Permite a usuarios registrarse, iniciar sesión y gestionar sus tareas personales con diferentes prioridades y estados.

## Características

- Sistema de usuarios
  - Registro de usuarios
  - Inicio y cierre de sesión
  - Modo oscuro personalizable

- Gestión de tareas
  - Crear tareas con diferentes prioridades
  - Marcar tareas como completadas
  - Actualizar detalles de tareas
  - Eliminar tareas
  - Limpieza automática de tareas antiguas

- Prioridades de tareas
  - Importantes
  - Normales
  - Postergables

## Requisitos

- Python 3.8+
- SQLAlchemy
- SQLite3

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
   python -m pytest tests/
   ```

## Estructura del Proyecto

```
cs-final-to-do/
├── src/
│   ├── controlador/     # Controladores y lógica de negocio
│   │   ├── database/    # Capa de acceso a datos
│   │   └── logica/      # Modelos de base de datos
│   ├── modelo/          # Modelos de dominio
│   └── vista/          # Interfaces de usuario
├── tests/              # Pruebas unitarias
├── README.md
└── requirements.txt
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
