-- schema.sql - Esquema de base de datos (tu script actual)

CREATE DATABASE Obligatorio;

USE Obligatorio;

CREATE TABLE login (
  email VARCHAR(255) PRIMARY KEY,
  contraseña VARCHAR(255) NOT NULL
);

CREATE TABLE participante (
  ci VARCHAR(20) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE facultad (
  id_facultad INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE programa_academico (
  nombre_programa VARCHAR(150) PRIMARY KEY,
  id_facultad INT NOT NULL,
  tipo ENUM('grado','posgrado') NOT NULL,
  FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)
);

CREATE TABLE participante_programa_academico (
  id_alumno_programa INT AUTO_INCREMENT PRIMARY KEY,
  ci_participante VARCHAR(20) NOT NULL,
  nombre_programa VARCHAR(150) NOT NULL,
  rol ENUM('alumno','docente') NOT NULL,
  FOREIGN KEY (ci_participante) REFERENCES participante(ci),
  FOREIGN KEY (nombre_programa) REFERENCES programa_academico(nombre_programa)
);

CREATE TABLE edificio (
  nombre_edificio VARCHAR(150) PRIMARY KEY,
  direccion VARCHAR(255),
  departamento VARCHAR(100)
);

CREATE TABLE sala (
  nombre_sala VARCHAR(100),
  edificio VARCHAR(150),
  capacidad INT NOT NULL,
  tipo_sala ENUM('libre','posgrado','docente') NOT NULL,
  PRIMARY KEY (nombre_sala, edificio),
  FOREIGN KEY (edificio) REFERENCES edificio(nombre_edificio)
);

CREATE TABLE turno (
  id_turno INT AUTO_INCREMENT PRIMARY KEY,
  hora_inicio TIME NOT NULL,
  hora_fin TIME NOT NULL
);

CREATE TABLE reserva (
  id_reserva INT AUTO_INCREMENT PRIMARY KEY,
  nombre_sala VARCHAR(100) NOT NULL,
  edificio VARCHAR(150) NOT NULL,
  fecha DATE NOT NULL,
  id_turno INT NOT NULL,
  estado ENUM('activa','cancelada','sin_asistencia','finalizada') NOT NULL,
  FOREIGN KEY (nombre_sala, edificio) REFERENCES sala(nombre_sala, edificio),
  FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
);

CREATE TABLE reserva_participante (
  ci_participante VARCHAR(20) NOT NULL,
  id_reserva INT NOT NULL,
  fecha_solicitud_reserva DATETIME NOT NULL,
  asistencia BOOLEAN,
  PRIMARY KEY (ci_participante, id_reserva),
  FOREIGN KEY (ci_participante) REFERENCES participante(ci),
  FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

CREATE TABLE sancion_participante (
  id_sancion INT AUTO_INCREMENT PRIMARY KEY,
  ci_participante VARCHAR(20) NOT NULL,
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NOT NULL,
  FOREIGN KEY (ci_participante) REFERENCES participante(ci)
);
