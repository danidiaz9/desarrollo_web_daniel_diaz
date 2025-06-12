from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from collections import Counter
import calendar
import os
import hashlib
import filetype
from database.db import *
from utils.validations import *

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def generar_nombre_archivo_seguro(file):
    _filename = hashlib.sha256(
        secure_filename(file.filename).encode("utf-8")
    ).hexdigest()
    _extension = filetype.guess(file).extension
    return f"{_filename}.{_extension}"

@app.route('/')
def index():
    actividades = get_actividades()[:5]
    return render_template('index.html', actividades=actividades)

@app.route('/informar-actividad', methods=['GET', 'POST'])
def informar():
    regiones = get_regiones()
    if request.method == 'POST':
        # Validaciones de formulario
        datos = request.form
        archivos = request.files.getlist('fotos')
        errores = validate_form(datos, archivos)
        if errores:
            for error in errores:
                flash(error, "error")
            return render_template('informar-actividad.html', regiones=regiones)
        comuna_id = datos.get('comuna')
        sector = datos.get('sector')
        nombre = datos.get('nombre')
        email = datos.get('email')
        celular = datos.get('celular')
        dia_hora_inicio = datos.get('fecha_inicio')
        dia_hora_termino = datos.get('fecha_termino')
        descripcion = datos.get('descripcion')
        tema = datos.get('tema')
        tema_otros = datos.get('tema_otro')
        contactos = datos.getlist('contactos')
        fotos = request.files.getlist('fotos')

        create_actividad(comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion)
        
        actividad = get_actividad_por_campos(nombre, email, dia_hora_inicio)
        actividad_id = actividad.id
        if tema:
            create_tema(tema, tema_otros if tema_otros else None, actividad_id)
        # Procesa los contactos
        for metodo in ['whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra']:
            identificador = request.form.get(f"{metodo}_id")
            if identificador:  # Si el usuario ingresó un valor
                create_contacto(metodo, identificador, actividad_id)
        for file in fotos:
            if file and allowed_file(file.filename):
                filename = generar_nombre_archivo_seguro(file)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                create_foto(actividad.id, filename)
            else:
                flash("Archivo no permitido o no válido.", "error")
                return render_template('informar-actividad.html', regiones=regiones)
        flash("¡Actividad registrada exitosamente!", "success")
        return redirect(url_for('index'))
    
    return render_template('informar-actividad.html', regiones=regiones)

@app.route('/listado-actividades')
def listado():
    page = int(request.args.get('page', 1))
    per_page = 5
    actividades = get_actividades()
    actividades = sorted(actividades, key=lambda x: x.dia_hora_inicio, reverse=True)
    total = len(actividades)
    actividades_pagina = actividades[(page-1)*per_page:page*per_page]
    max_page = (total + per_page - 1) // per_page
    if total == 0:
        max_page = 1
    return render_template(
        'listado-actividades.html',
        actividades=actividades_pagina,
        page=page,
        max_page=max_page
    )

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

@app.route('/api/comunas')
def comunas():
    region_id = request.args.get('region_id')
    comunas = get_comunas_por_region(region_id)
    return jsonify([{'id': c.id, 'nombre': c.nombre} for c in comunas])

@app.route('/api/actividad/<int:actividad_id>')
def detalle_actividad(actividad_id):
    actividad = get_actividad_por_id(actividad_id)
    if not actividad:
        # Retorna HTML de error, no redirect
        return render_template('404.html', mensaje="Actividad no encontrada"), 404
    return render_template('detalle-actividad.html', actividad=actividad)

@app.route('/api/actividad/<int:actividad_id>/comentarios', methods=['POST'])
def agregar_comentario(actividad_id):
    actividad = get_actividad_por_id(actividad_id)
    if not actividad:
        return jsonify({'error': 'Actividad no encontrada'}), 404

    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    texto = data.get('texto', '').strip()

    errores = validate_comentario(nombre, texto)
    if errores:
        return jsonify({'errores': errores}), 400

    fecha = datetime.now()
    create_comentario(nombre, texto, fecha, actividad_id)
    return jsonify({
        'nombre': nombre,
        'texto': texto,
        'fecha': fecha.strftime('%Y-%m-%d %H:%M')
    }), 201

@app.route('/api/actividad/<int:actividad_id>/comentarios', methods=['GET'])
def lista_comentarios(actividad_id):
    comentarios = get_comentarios_por_actividad(actividad_id)
    # Formatea los comentarios para el frontend
    comentarios_json = [
        {
            "nombre": c.nombre,
            "texto": c.texto,
            "fecha": c.fecha.strftime('%Y-%m-%d %H:%M')
        }
        for c in comentarios
    ]
    return jsonify(comentarios_json)

@app.route("/api/estadisticas")
def api_estadisticas():

    actividades = get_actividades()

    # --- Gráfico de líneas: actividades por día ---
    fechas = [a.dia_hora_inicio.date() for a in actividades]
    por_dia = Counter(fechas)
    dias_ordenados = sorted(por_dia.items())
    lineas = {
        "dias": [d.strftime("%a %d") for d, _ in dias_ordenados],
        "cantidades": [c for _, c in dias_ordenados]
    }

    # --- Gráfico de torta: actividades por tipo ---
    tipos = []
    for a in actividades:
        tipos.extend([t.tema for t in a.temas])
    tipos_contados = Counter(tipos)
    torta = {
        "tipos": list(tipos_contados.keys()),
        "cantidades": list(tipos_contados.values())
    }

    # --- Gráfico de barras: horarios por mes ---
    horarios = {
        "mañana": lambda h: 5 <= h < 12,
        "mediodía": lambda h: 12 <= h < 14,
        "tarde": lambda h: 14 <= h < 21
    }
    resumen = {mes: {"mañana": 0, "mediodía": 0, "tarde": 0} for mes in range(1, 13)}

    for a in actividades:
        dt = a.dia_hora_inicio
        h = dt.hour
        for key, cond in horarios.items():
            if cond(h):
                resumen[dt.month][key] += 1
                break

    meses = [calendar.month_abbr[m] for m in sorted(resumen.keys())]
    barras = {
        "meses": meses,
        "manana": [resumen[m]["mañana"] for m in sorted(resumen)],
        "mediodia": [resumen[m]["mediodía"] for m in sorted(resumen)],
        "tarde": [resumen[m]["tarde"] for m in sorted(resumen)]
    }

    return jsonify({
        "lineas": lineas,
        "torta": torta,
        "barras": barras
    })
