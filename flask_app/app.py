from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from database.db import *
from utils.validations import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

@app.route('/')
def index():
    actividades = get_ultimas_actividades(5)
    return render_template('index.html', actividades=actividades)

@app.route('/informar-actividad', methods=['GET', 'POST'])
def informar():
    if request.method == 'POST':
        fotos_guardadas = []
        try:
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            # Validar archivos
            fotos = request.files.getlist('fotos')
            valido, mensaje = validate_photos(fotos)
            if not valido:
                flash(mensaje, 'danger')
                return render_template('informar-actividad.html', regiones=get_regiones())
            
            # Validar campos principales
            errores = []
            campos_requeridos = {
                'region': 'Debe seleccionar una región',
                'comuna': 'Debe seleccionar una comuna',
                'nombre': 'El nombre es obligatorio',
                'email': 'El email es obligatorio',
                'fecha_inicio': 'La fecha de inicio es obligatoria'
            }
            
            for campo, mensaje in campos_requeridos.items():
                if not request.form.get(campo):
                    errores.append(mensaje)

            # Validar teléfono
            celular = request.form.get('celular', '')
            if celular:
                valido, mensaje = validate_phone(celular)
                if not valido:
                    errores.append(mensaje)

            # Validar email
            email = request.form['email']
            valido, mensaje = validate_email(email)
            if not valido:
                errores.append(mensaje)

            # Validar fechas
            fecha_inicio = datetime.fromisoformat(request.form['fecha_inicio'])
            fecha_termino = request.form.get('fecha_termino')
            valido, mensaje_fechas = validate_fechas(fecha_inicio, datetime.fromisoformat(fecha_termino) if fecha_termino else None)
            if not valido:
                errores.extend(mensaje_fechas)

            # Validar tema
            tema = request.form.get('tema')
            glosa_otro = request.form.get('tema_otro', '')
            valido, mensaje = validate_custom_topic(tema, glosa_otro)
            if not valido:
                errores.append(mensaje)

            # Validar contactos
            contactos = [(request.form.get('contacto_tipo'), request.form.get('contacto_valor'))]
            valido, mensaje = validate_contactos(contactos)
            if not valido:
                errores.append(mensaje)

            if errores:
                for error in errores:
                    flash(error, 'danger')
                return render_template('informar-actividad.html', 
                                       regiones=get_regiones(),
                                       temas=get_temas())

            # Procesar datos válidos
            actividad_data = {
                'comuna_id': request.form['comuna'],
                'sector': request.form.get('sector', ''),
                'nombre': request.form['nombre'],
                'email': email,
                'celular': celular,
                'dia_hora_inicio': fecha_inicio,
                'dia_hora_termino': datetime.fromisoformat(fecha_termino) if fecha_termino else None,
                'descripcion': request.form['descripcion']
            }

            temas_data = [{'tema': tema, 'glosa_otro': glosa_otro}]
            
            contactos_data = []
            for metodo in ['whatsapp', 'telegram', 'twitter', 'instagram', 'tiktok', 'otro']:
                if metodo in request.form.getlist('contacto'):
                    valor = request.form.get(f"{metodo}_id")
                    if valor:
                        contactos_data.append({'nombre': metodo, 'identificador': valor})

            fotos_data = []
            for foto in fotos:
                if foto and allowed_file(foto.filename):
                    filename = secure_filename(foto.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    foto.save(filepath)
                    fotos_guardadas.append(filepath)
                    fotos_data.append({'ruta_archivo': filepath, 'nombre_archivo': filename})

            create_actividad(actividad_data, temas_data, contactos_data, fotos_data)
            
            flash('Actividad registrada exitosamente!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            for filepath in fotos_guardadas:
                try:
                    os.remove(filepath)
                except:
                    pass
            flash(f'Error al procesar la solicitud: {str(e)}', 'danger')
            return render_template('informar-actividad.html', 
                                   regiones=get_regiones(),
                                   temas=get_temas())

    # GET: Mostrar formulario
    return render_template('informar-actividad.html', 
                           regiones=get_regiones(),
                           temas=get_temas())

@app.route('/listado-actividades')
def listado():
    page = request.args.get('page', 1, type=int)
    actividades, total = get_actividades_paginadas(page=page)
    return render_template('listado-actividades.html', actividades=actividades, total=total)

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

@app.route('/api/comunas')
def api_comunas():
    region_id = request.args.get('region_id')
    comunas = get_comunas_por_region(region_id)
    return jsonify([{'id': c.id, 'nombre': c.nombre} for c in comunas])