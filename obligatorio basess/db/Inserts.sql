-- sample_data.sql - Datos de ejemplo (tu script actual de inserts)

USE Obligatorio;

INSERT INTO facultad (nombre)
VALUES 
('Ingeniería'),
('Ciencias Empresariales');

INSERT INTO programa_academico (nombre_programa, id_facultad, tipo)
VALUES
('Ingeniería Informática', 1, 'grado'),
('MBA', 2, 'posgrado');

INSERT INTO participante (ci, nombre, apellido, email)
VALUES
('11111111', 'Juan', 'Pérez', 'juan.perez@ucu.edu.uy'),
('22222222', 'María', 'Gómez', 'maria.gomez@ucu.edu.uy'),
('33333333', 'Roberto', 'Suárez', 'roberto.suarez@ucu.edu.uy');

INSERT INTO login (email, contraseña)
VALUES
('juan.perez@ucu.edu.uy', 'hash1'),
('maria.gomez@ucu.edu.uy', 'hash2'),
('roberto.suarez@ucu.edu.uy', 'hash3');

INSERT INTO participante_programa_academico (ci_participante, nombre_programa, rol)
VALUES
('11111111', 'Ingeniería Informática', 'alumno'),
('22222222', 'MBA', 'alumno'),
('33333333', 'Ingeniería Informática', 'docente');

INSERT INTO edificio (nombre_edificio, direccion, departamento)
VALUES
('Aulario Sur', 'Av. 8 de Octubre 2738', 'Montevideo'),
('Biblioteca Central', 'Av. Sarmiento 1250', 'Montevideo');

INSERT INTO sala (nombre_sala, edificio, capacidad, tipo_sala)
VALUES
('Sala 101', 'Aulario Sur', 6, 'libre'),
('Sala 201', 'Aulario Sur', 4, 'posgrado'),
('Sala B1', 'Biblioteca Central', 8, 'docente');

INSERT INTO turno (hora_inicio, hora_fin)
VALUES
('08:00:00', '09:00:00'),
('09:00:00', '10:00:00'),
('10:00:00', '11:00:00');

INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado)
VALUES
('Sala 101', 'Aulario Sur', '2025-11-25', 1, 'activa'),
('Sala 201', 'Aulario Sur', '2025-11-25', 2, 'finalizada'),
('Sala B1', 'Biblioteca Central', '2025-11-26', 1, 'sin_asistencia');

INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia)
VALUES
('11111111', 1, '2025-11-20 10:00:00', TRUE),
('22222222', 2, '2025-11-21 14:30:00', TRUE),
('33333333', 3, '2025-11-22 09:15:00', FALSE);

INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin)
VALUES
('33333333', '2025-11-27', '2026-01-27');
