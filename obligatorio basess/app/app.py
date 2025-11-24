from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
from db import query_all, query_one, execute


# App Flask principal del obligatorio
app = Flask(__name__)



# Clave para sesiones (flash, login, etc.)
app.secret_key = "cambia-esto-por-algo-seguro"


@app.before_request
def requerir_login():
    #login obligatorio para todas las rutas
    rutas_publicas = {"login", "static"}
    if request.endpoint is None:
        return
    if request.endpoint in rutas_publicas:
        return
    if "user_email" not in session:
        return redirect(url_for("login"))


@app.route("/")
def index():
    # Datos básicos para mostrar en el inicio
    total_participantes = query_one("SELECT COUNT(*) AS c FROM participante")["c"]
    total_salas = query_one("SELECT COUNT(*) AS c FROM sala")["c"]
    total_reservas = query_one("SELECT COUNT(*) AS c FROM reserva")["c"]
    return render_template(
        "index.html",
        total_participantes=total_participantes,
        total_salas=total_salas,
        total_reservas=total_reservas,
    )




# LOGIN / LOGOUT

@app.route("/login", methods=["GET", "POST"])
def login():
    # Si ya está logueado, lo mando al inicio
    if "user_email" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("login"))

        # Buscamos el usuario en la tabla login
        usuario = query_one(
            "SELECT email, contraseña FROM login WHERE email = %s",
            (email,),
        )

        if not usuario or usuario["contraseña"] != password:
            flash("Email o contraseña incorrectos", "error")
            return redirect(url_for("login"))

        # Guardamos email en la sesión
        session["user_email"] = usuario["email"]
        flash("Sesión iniciada correctamente", "success")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "success")
    return redirect(url_for("login"))



# PARTICIPANTES


@app.route("/participantes")
def participantes_list():
    participantes = query_all("SELECT * FROM participante ORDER BY apellido, nombre")
    return render_template("participantes_list.html", participantes=participantes)


@app.route("/participantes/nuevo", methods=["GET", "POST"])
def participantes_nuevo():
    if request.method == "POST":
        ci = request.form.get("ci")
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        email = request.form.get("email")

        if not ci or not nombre or not apellido or not email:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("participantes_nuevo"))

        try:
            execute(
                "INSERT INTO participante (ci, nombre, apellido, email) VALUES (%s, %s, %s, %s)",
                (ci, nombre, apellido, email),
            )
            flash("Participante creado correctamente", "success")
            return redirect(url_for("participantes_list"))
        except Exception as e:
            flash(f"Error al crear participante: {e}", "error")
            return redirect(url_for("participantes_nuevo"))

    return render_template("participantes_form.html", participante=None)


@app.route("/participantes/<ci>/editar", methods=["GET", "POST"])
def participantes_editar(ci):
    participante = query_one("SELECT * FROM participante WHERE ci = %s", (ci,))
    if not participante:
        flash("Participante no encontrado", "error")
        return redirect(url_for("participantes_list"))

    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        email = request.form.get("email")

        if not nombre or not apellido or not email:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("participantes_editar", ci=ci))

        try:
            execute(
                "UPDATE participante SET nombre=%s, apellido=%s, email=%s WHERE ci=%s",
                (nombre, apellido, email, ci),
            )
            flash("Participante actualizado", "success")
            return redirect(url_for("participantes_list"))
        except Exception as e:
            flash(f"Error al actualizar participante: {e}", "error")
            return redirect(url_for("participantes_editar", ci=ci))

    return render_template("participantes_form.html", participante=participante)


@app.route("/participantes/<ci>/eliminar", methods=["POST"])
def participantes_eliminar(ci):
    try:
        execute("DELETE FROM participante WHERE ci = %s", (ci,))
        flash("Participante eliminado", "success")
    except Exception as e:
        flash(f"No se pudo eliminar el participante: {e}", "error")
    return redirect(url_for("participantes_list"))


# SALAS 


@app.route("/salas")
def salas_list():
    # Join con edificio para mostrar dirección
    salas = query_all(
        "SELECT s.*, e.direccion FROM sala s "
        "JOIN edificio e ON s.edificio = e.nombre_edificio "
        "ORDER BY s.edificio, s.nombre_sala"
    )
    return render_template("salas_list.html", salas=salas)



@app.route("/salas/nueva", methods=["GET", "POST"])
def salas_nueva():
    edificios = query_all("SELECT * FROM edificio ORDER BY nombre_edificio")

    if request.method == "POST":
        nombre_sala = request.form.get("nombre_sala")
        edificio = request.form.get("edificio")
        capacidad = request.form.get("capacidad")
        tipo_sala = request.form.get("tipo_sala")

        if not nombre_sala or not edificio or not capacidad or not tipo_sala:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("salas_nueva"))

        try:
            capacidad_int = int(capacidad)
            if capacidad_int <= 0:
                raise ValueError("Capacidad debe ser mayor a 0")
        except ValueError:
            flash("Capacidad debe ser un entero mayor a 0", "error")
            return redirect(url_for("salas_nueva"))

        try:
            execute(
                "INSERT INTO sala (nombre_sala, edificio, capacidad, tipo_sala) "
                "VALUES (%s, %s, %s, %s)",
                (nombre_sala, edificio, capacidad_int, tipo_sala),
            )
            flash("Sala creada correctamente", "success")
            return redirect(url_for("salas_list"))
        except Exception as e:
            flash(f"Error al crear sala: {e}", "error")
            return redirect(url_for("salas_nueva"))

    return render_template("salas_form.html", sala=None, edificios=edificios)


@app.route("/salas/<edificio>/<nombre_sala>/editar", methods=["GET", "POST"])
def salas_editar(edificio, nombre_sala):
    sala = query_one(
        "SELECT * FROM sala WHERE nombre_sala=%s AND edificio=%s",
        (nombre_sala, edificio),
    )
    if not sala:
        flash("Sala no encontrada", "error")
        return redirect(url_for("salas_list"))

    edificios = query_all("SELECT * FROM edificio ORDER BY nombre_edificio")

    if request.method == "POST":
        capacidad = request.form.get("capacidad")
        tipo_sala = request.form.get("tipo_sala")

        try:
            capacidad_int = int(capacidad)
            if capacidad_int <= 0:
                raise ValueError("Capacidad debe ser mayor a 0")
        except ValueError:
            flash("Capacidad inválida", "error")
            return redirect(
                url_for("salas_editar", edificio=edificio, nombre_sala=nombre_sala)
            )

        try:
            execute(
                "UPDATE sala SET capacidad=%s, tipo_sala=%s "
                "WHERE nombre_sala=%s AND edificio=%s",
                (capacidad_int, tipo_sala, nombre_sala, edificio),
            )
            flash("Sala actualizada", "success")
            return redirect(url_for("salas_list"))
        except Exception as e:
            flash(f"Error al actualizar sala: {e}", "error")
            return redirect(
                url_for("salas_editar", edificio=edificio, nombre_sala=nombre_sala)
            )

    return render_template("salas_form.html", sala=sala, edificios=edificios)


@app.route("/salas/<edificio>/<nombre_sala>/eliminar", methods=["POST"])
def salas_eliminar(edificio, nombre_sala):
    try:
        execute(
            "DELETE FROM sala WHERE nombre_sala=%s AND edificio=%s",
            (nombre_sala, edificio),
        )
        flash("Sala eliminada", "success")
    except Exception as e:
        flash(f"No se pudo eliminar la sala: {e}", "error")
    return redirect(url_for("salas_list"))




# RESERVAS

@app.route("/reservas")
def reservas_list():
    reservas = query_all(
        "SELECT r.id_reserva, r.fecha, r.estado, "
        "r.nombre_sala, r.edificio, t.hora_inicio, t.hora_fin "
        "FROM reserva r "
        "JOIN turno t ON r.id_turno = t.id_turno "
        "ORDER BY r.fecha DESC, t.hora_inicio"
    )
    return render_template("reservas_list.html", reservas=reservas)


@app.route("/reservas/nueva", methods=["GET", "POST"])
def reservas_nueva():
    salas = query_all("SELECT * FROM sala ORDER BY edificio, nombre_sala")
    turnos = query_all("SELECT * FROM turno ORDER BY hora_inicio")

    if request.method == "POST":
        nombre_sala = request.form.get("nombre_sala")
        edificio = request.form.get("edificio")
        fecha = request.form.get("fecha")
        id_turno = request.form.get("id_turno")
        ci_participantes = request.form.get("ci_participantes")

        if not (nombre_sala and edificio and fecha and id_turno and ci_participantes):
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("reservas_nueva"))

        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            flash("Fecha inválida", "error")
            return redirect(url_for("reservas_nueva"))

        # 1. Para obtener datos de la sala 
        sala = query_one(
            "SELECT capacidad, tipo_sala FROM sala "
            "WHERE nombre_sala=%s AND edificio=%s",
            (nombre_sala, edificio),
        )
        if not sala:
            flash("La sala seleccionada no existe", "error")
            return redirect(url_for("reservas_nueva"))

        capacidad_sala = sala["capacidad"]
        tipo_sala = sala["tipo_sala"]

        # 2. Evitamos doble reserva misma sala + fecha + turno
        choque = query_one(
            "SELECT COUNT(*) AS c "
            "FROM reserva "
            "WHERE nombre_sala=%s AND edificio=%s AND fecha=%s AND id_turno=%s "
            "AND estado <> 'cancelada'",
            (nombre_sala, edificio, fecha_obj, id_turno),
        )
        if choque["c"] > 0:
            flash("Ya existe una reserva en esa sala para ese día y turno", "error")
            return redirect(url_for("reservas_nueva"))



        lista_ci = [c.strip() for c in ci_participantes.split(",") if c.strip()]

        if len(lista_ci) > capacidad_sala:
            flash(
                f"La sala tiene capacidad {capacidad_sala} pero ingresaste {len(lista_ci)} participantes",
                "error",
            )
            return redirect(url_for("reservas_nueva"))
        

        # Chequeamos lo de los 7 días
        fecha_inicio_ventana = fecha_obj - timedelta(days=6)

        # 4. Las reglas por participante
        for ci in lista_ci:
            participante = query_one("SELECT ci FROM participante WHERE ci=%s", (ci,))
            if not participante:
                flash(f"El participante {ci} no existe", "error")
                return redirect(url_for("reservas_nueva"))

            academico = query_all(
                "SELECT ppa.rol, pa.tipo "
                "FROM participante_programa_academico ppa "
                "JOIN programa_academico pa ON pa.nombre_programa = ppa.nombre_programa "
                "WHERE ppa.ci_participante=%s",
                (ci,),
            )

            exonerado = False
            for fila in academico:
                rol = fila["rol"]       
                tipo = fila["tipo"]     

                # Docentes en salas de docentes y posgrados en salas de posgrad
                if tipo_sala == "docente" and rol == "docente":
                    exonerado = True
                if tipo_sala == "posgrado" and tipo == "posgrado":
                    exonerado = True

            if not exonerado:
                # Maxima de 2 reservas por día
                reservas_dia = query_one(
                    "SELECT COUNT(*) AS c FROM reserva r "
                    "JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva "
                    "WHERE rp.ci_participante=%s AND r.fecha=%s "
                    "AND r.estado <> 'cancelada'",
                    (ci, fecha_obj),
                )
                if reservas_dia["c"] >= 2:
                    flash(
                        f"El participante {ci} ya tiene 2 reservas ese día",
                        "error",
                    )
                    return redirect(url_for("reservas_nueva"))

                # Maxima de 3 reservas activas en la semana
                activas_semana = query_one(
                    "SELECT COUNT(*) AS c FROM reserva r "
                    "JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva "
                    "WHERE rp.ci_participante=%s "
                    "AND r.estado='activa' "
                    "AND r.fecha BETWEEN %s AND %s",
                    (ci, fecha_inicio_ventana, fecha_obj),
                )
                if activas_semana["c"] >= 3:
                    flash(
                        f"El participante {ci} ya tiene 3 reservas activas en la semana",
                        "error",
                    )
                    return redirect(url_for("reservas_nueva"))

        # 5. Crear reserva y asignar a los participantes
        try:
            id_reserva = execute(
                "INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado) "
                "VALUES (%s, %s, %s, %s, 'activa')",
                (nombre_sala, edificio, fecha_obj, id_turno),
            )

            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for ci in lista_ci:
                execute(
                    "INSERT INTO reserva_participante "
                    "(ci_participante, id_reserva, fecha_solicitud_reserva, asistencia) "
                    "VALUES (%s, %s, %s, NULL)",
                    (ci, id_reserva, ahora),
                )

            flash("Reserva creada correctamente", "success")
            return redirect(url_for("reservas_list"))
        except Exception as e:
            flash(f"Error al crear reserva: {e}", "error")
            return redirect(url_for("reservas_nueva"))

    return render_template("reservas_form.html", salas=salas, turnos=turnos)


if __name__ == "__main__":
    app.run(debug=True)


# SANCIONES


@app.route("/sanciones")
def sanciones_list():
    sanciones = query_all(
        "SELECT sp.id_sancion, sp.ci_participante, sp.fecha_inicio, sp.fecha_fin, "
        "p.nombre, p.apellido "
        "FROM sancion_participante sp "
        "JOIN participante p ON p.ci = sp.ci_participante "
        "ORDER BY sp.fecha_inicio DESC"
    )
    return render_template("sanciones_list.html", sanciones=sanciones)



@app.route("/sanciones/nueva", methods=["GET", "POST"])
def sanciones_nueva():
    participantes = query_all(
        "SELECT ci, nombre, apellido FROM participante ORDER BY apellido, nombre"
    )

    if request.method == "POST":
        ci = request.form.get("ci_participante")
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")

        if not ci or not fecha_inicio or not fecha_fin:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("sanciones_nueva"))

        try:
            # Validamos formato de fecha YYYY-MM-DD
            datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            flash("Formato de fecha inválido", "error")
            return redirect(url_for("sanciones_nueva"))

        try:
            execute(
                "INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin) "
                "VALUES (%s, %s, %s)",
                (ci, fecha_inicio, fecha_fin),
            )
            flash("Sanción creada correctamente", "success")
            return redirect(url_for("sanciones_list"))
        except Exception as e:
            flash(f"Error al crear sanción: {e}", "error")
            return redirect(url_for("sanciones_nueva"))

    return render_template("sanciones_form.html", participantes=participantes)



@app.route("/sanciones/<int:id_sancion>/eliminar", methods=["POST"])
def sanciones_eliminar(id_sancion):
    try:
        execute(
            "DELETE FROM sancion_participante WHERE id_sancion = %s",
            (id_sancion,),
        )
        flash("Sanción eliminada", "success")
    except Exception as e:
        flash(f"No se pudo eliminar la sanción: {e}", "error")
    return redirect(url_for("sanciones_list"))

