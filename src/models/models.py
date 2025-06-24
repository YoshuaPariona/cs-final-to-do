from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from src.database.db import Base
from datetime import datetime


class Usuario(Base):
    """
    Modelo que representa a un usuario.

    Atributos:
        idUsuario (int): Identificador único del usuario.
        nombre (str): Nombre del usuario.
        email (str): Correo electrónico del usuario.
        contraseña (str): Contraseña del usuario.
        modoOscuro (bool): Preferencia de tema oscuro.
        tareas (list): Lista de tareas asociadas al usuario.
    """
    __tablename__ = 'usuarios'

    idUsuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    email = Column(String)
    contraseña = Column(String)
    modoOscuro = Column(Boolean)
    tareas = relationship("Tarea", back_populates="usuario")


class Grupo(Base):
    """
    Modelo que representa un grupo de tareas.

    Atributos:
        idGrupo (int): Identificador único del grupo.
        nombre (str): Nombre del grupo.
        tareas (list): Lista de tareas asociadas al grupo.
    """
    __tablename__ = 'grupos'

    idGrupo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    tareas = relationship("Tarea", back_populates="grupo")


class TipoTarea(Base):
    """
    Modelo que representa un tipo o categoría de tarea.

    Atributos:
        idTipoTarea (int): Identificador único del tipo de tarea.
        nombreTipo (str): Nombre del tipo de tarea.
        descripcion (str): Descripción del tipo de tarea.
        tareas (list): Lista de tareas asociadas al tipo.
    """
    __tablename__ = 'tipo_tareas'

    idTipoTarea = Column(Integer, primary_key=True, autoincrement=True)
    nombreTipo = Column(String)
    descripcion = Column(Text)
    tareas = relationship("Tarea", back_populates="tipo_tarea")


class Tarea(Base):
    """
    Modelo que representa una tarea.

    Atributos:
        idTarea (int): Identificador único de la tarea.
        titulo (str): Título de la tarea.
        descripcion (str): Descripción de la tarea.
        fechaCreacion (datetime): Fecha y hora de creación.
        fechaVencimiento (datetime): Fecha límite para completar la tarea.
        estado (str): Estado actual de la tarea.
        prioridad (str): Prioridad asignada a la tarea.
        tipo (str): Tipo o categoría de la tarea.
        idUsuario (int): ID del usuario propietario.
        idGrupo (int): ID del grupo al que pertenece la tarea.
        idTipoTarea (int): ID del tipo de tarea.
        usuario (Usuario): Relación con el usuario.
        grupo (Grupo): Relación con el grupo.
        tipo_tarea (TipoTarea): Relación con el tipo de tarea.
    """
    __tablename__ = 'tareas'

    idTarea = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String)
    descripcion = Column(Text)
    fechaCreacion = Column(DateTime, default=datetime.utcnow)
    fechaVencimiento = Column(DateTime)
    estado = Column(String)
    prioridad = Column(String)
    tipo = Column(String)

    idUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'))
    idGrupo = Column(Integer, ForeignKey('grupos.idGrupo'))
    idTipoTarea = Column(Integer, ForeignKey('tipo_tareas.idTipoTarea'))

    usuario = relationship("Usuario", back_populates="tareas")
    grupo = relationship("Grupo", back_populates="tareas")
    tipo_tarea = relationship("TipoTarea", back_populates="tareas")


class Event(Base):
    __tablename__ = 'eventos'
    idEvento = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String)
    descripcion = Column(Text)
    fecha = Column(String)  # ISO date string
    hora = Column(String)   # HH:MM
    prioridad = Column(String)
    idUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'))
    usuario = relationship("Usuario")
