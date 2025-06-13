"""
Este módulo define los modelos de la base de datos para la aplicación de gestión de tareas.
Utiliza SQLAlchemy para definir las tablas y sus relaciones.
"""

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database.db import Base
from datetime import datetime

class Usuario(Base):
    """
    Representa un usuario en el sistema.
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
    Representa un grupo de tareas en el sistema.
    """
    __tablename__ = 'grupos'
    idGrupo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    tareas = relationship("Tarea", back_populates="grupo")

class TipoTarea(Base):
    """
    Representa un tipo de tarea en el sistema.
    """
    __tablename__ = 'tipo_tareas'
    idTipoTarea = Column(Integer, primary_key=True, autoincrement=True)
    nombreTipo = Column(String)
    descripcion = Column(Text)
    tareas = relationship("Tarea", back_populates="tipo_tarea")

class Tarea(Base):
    """
    Representa una tarea en el sistema.
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
