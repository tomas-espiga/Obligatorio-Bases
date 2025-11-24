-- Salas más reservadas

SELECT r.nombre_sala, r.edificio, COUNT(*) AS total_reservas
FROM reserva r
GROUP BY r.nombre_sala, r.edificio
ORDER BY total_reservas DESC;

-- Turnos más demandados

SELECT t.id_turno, t.hora_inicio, t.hora_fin, COUNT(r.id_reserva) AS total_reservas
FROM reserva r
JOIN turno t ON r.id_turno = t.id_turno
GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
ORDER BY total_reservas DESC;

-- Promedio de participantes por sala

SELECT r.nombre_sala, r.edificio, AVG(rp_count.cantidad) AS promedio_participantes
FROM (
    SELECT id_reserva, COUNT(*) AS cantidad
    FROM reserva_participante
    GROUP BY id_reserva
) rp_count
JOIN reserva r ON rp_count.id_reserva = r.id_reserva
GROUP BY r.nombre_sala, r.edificio;

-- Cantidad de reservas por carrera y facultad 

SELECT pa.nombre_programa,
       f.nombre AS facultad,
       COUNT(DISTINCT rp.id_reserva) AS total_reservas
FROM reserva_participante rp
JOIN participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
JOIN facultad f ON pa.id_facultad = f.id_facultad
GROUP BY pa.nombre_programa, f.nombre;

-- Porcentaje de ocupación de salas por edificio

SELECT e.nombre_edificio,
       COUNT(r.id_reserva) AS total_reservas,
       ROUND((COUNT(r.id_reserva) / (SELECT COUNT(*) FROM reserva) * 100), 2) AS porcentaje_ocupacion
FROM edificio e
LEFT JOIN sala s ON s.edificio = e.nombre_edificio
LEFT JOIN reserva r ON r.nombre_sala = s.nombre_sala AND r.edificio = s.edificio
GROUP BY e.nombre_edificio;

-- Cantidad de reservas y asistencias de profesores y alumnos (grado y posgrado) 

SELECT ppa.rol,
       pa.tipo,
       COUNT(DISTINCT rp.id_reserva) AS total_reservas,
       SUM(rp.asistencia = TRUE) AS total_asistencias
FROM reserva_participante rp
JOIN participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
GROUP BY ppa.rol, pa.tipo;

-- Cantidad de sanciones para profesores y alumnos (grado y posgrado) 

SELECT ppa.rol,
       pa.tipo,
       COUNT(*) AS total_sanciones
FROM sancion_participante sp
JOIN participante_programa_academico ppa ON sp.ci_participante = ppa.ci_participante
JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
GROUP BY ppa.rol, pa.tipo;

-- Porcentaje de reservas efectivamente utilizadas vs. canceladas/no asistidas 

SELECT
    SUM(estado IN ('activa','finalizada')) AS reservas_utilizadas,
    SUM(estado IN ('cancelada','sin_asistencia')) AS reservas_no_usadas,
    ROUND(SUM(estado IN ('activa','finalizada')) / COUNT(*) * 100, 2) AS pct_utilizadas,
    ROUND(SUM(estado IN ('cancelada','sin_asistencia')) / COUNT(*) * 100, 2) AS pct_no_usadas
FROM reserva;

-- Extra 1: Participantes que usan más edificios distintos

SELECT 
    rp.ci_participante,
    p.nombre,
    p.apellido,
    COUNT(DISTINCT r.edificio) AS edificios_distintos_usados
FROM reserva_participante rp
JOIN reserva r ON rp.id_reserva = r.id_reserva
JOIN participante p ON p.ci = rp.ci_participante
GROUP BY rp.ci_participante, p.nombre, p.apellido
ORDER BY edificios_distintos_usados DESC;

-- Extra 2: Turnos menos demandados por edificio

SELECT 
    e.nombre_edificio,
    t.hora_inicio,
    t.hora_fin,
    COUNT(r.id_reserva) AS total_reservas
FROM edificio e
JOIN sala s ON s.edificio = e.nombre_edificio
JOIN turno t
LEFT JOIN reserva r 
    ON r.nombre_sala = s.nombre_sala 
    AND r.edificio = s.edificio 
    AND r.id_turno = t.id_turno
GROUP BY e.nombre_edificio, t.id_turno, t.hora_inicio, t.hora_fin
ORDER BY e.nombre_edificio, total_reservas ASC;

-- Extra 3: Participantes con mayor tasa de no asistencia

SELECT 
    rp.ci_participante,
    p.nombre,
    p.apellido,
    COUNT(*) AS total_reservas,
    SUM(r.estado = 'sin_asistencia') AS no_asistencias,
    ROUND(SUM(r.estado = 'sin_asistencia') / COUNT(*) * 100, 2) AS pct_no_asistencia
FROM reserva_participante rp
JOIN reserva r ON r.id_reserva = rp.id_reserva
JOIN participante p ON p.ci = rp.ci_participante
GROUP BY rp.ci_participante, p.nombre, p.apellido
HAVING total_reservas >= 3
ORDER BY pct_no_asistencia DESC;

-- Extra 4: Días de la semana con más actividad por tipo de sala

SELECT 
    DAYNAME(r.fecha) AS dia_semana,
    s.tipo_sala,
    COUNT(r.id_reserva) AS total_reservas
FROM reserva r
JOIN sala s ON s.nombre_sala = r.nombre_sala AND s.edificio = r.edificio
GROUP BY dia_semana, s.tipo_sala
ORDER BY dia_semana, s.tipo_sala;

