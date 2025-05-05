-- schema.sql
CREATE TABLE IF NOT EXISTS usuarios (
  idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT,
  email TEXT UNIQUE,
  contraseña TEXT,
  modoOscuro BOOLEAN
);

CREATE TABLE IF NOT EXISTS grupos (
  idGrupo INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT
);

CREATE TABLE IF NOT EXISTS tipo_tareas (
  idTipoTarea INTEGER PRIMARY KEY AUTOINCREMENT,
  nombreTipo TEXT,
  descripcion TEXT
);

CREATE TABLE IF NOT EXISTS tareas (
  idTarea INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT,
  descripcion TEXT,
  fechaCreacion TEXT,
  fechaVencimiento TEXT,
  estado TEXT,
  prioridad TEXT,
  tipo TEXT,
  idUsuario INTEGER,
  idGrupo INTEGER,
  idTipoTarea INTEGER,
  FOREIGN KEY (idUsuario) REFERENCES usuarios(idUsuario),
  FOREIGN KEY (idGrupo) REFERENCES grupos(idGrupo),
  FOREIGN KEY (idTipoTarea) REFERENCES tipo_tareas(idTipoTarea)
);
