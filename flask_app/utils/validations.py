import re
import filetype
from datetime import datetime
from collections import defaultdict

# Constantes
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
PHONE_REGEX = re.compile(r'^\+\d{3}\.\d{8}$')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_MIMETYPES = {'image/jpeg', 'image/png'}
MAX_PHOTOS = 5
MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5MB
VALID_TOPICS = {'música', 'deporte', 'ciencias', 'religión', 'política', 
               'tecnología', 'juegos', 'baile', 'comida', 'otro'}

def allowed_file(filename: str) -> bool:
    """Verifica si la extensión del archivo es permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_email(email: str) -> tuple[bool, str]:
    """Valida formato de email con regex mejorado"""
    if not email:
        return False, "El email es obligatorio"
    return (bool(EMAIL_REGEX.match(email)), 
           "Formato de email inválido (ej: usuario@dominio.com)")

def validate_phone(number: str) -> tuple[bool, str]:
    """Valida formato de teléfono chileno"""
    if not number:
        return True, ""  # Campo opcional
    return (bool(PHONE_REGEX.match(number)), 
           "Formato debe ser +569 seguido de 8 dígitos")

def validate_photos(files: list, min: int = 1, max: int = MAX_PHOTOS) -> tuple[bool, str]:
    """Valida archivos de imagen con chequeo de MIME type y tamaño"""
    # Solo archivos realmente subidos
    valid_files = [f for f in files if getattr(f, 'filename', None) and f.filename.strip()]
    
    # Validar cantidad
    if not (min <= len(valid_files) <= max):
        return False, f"Debe subir entre {min} y {max} fotos"
    
    # Validar cada archivo
    for file in valid_files:
        # Extensión
        if not allowed_file(file.filename):
            return False, f"Solo se permiten archivos {', '.join(ALLOWED_EXTENSIONS)}"
        
        # MIME Type
        mime = filetype.guess(file.stream.read(2048))
        file.stream.seek(0)
        if not mime or mime.mime not in ALLOWED_MIMETYPES:
            return False, "Tipo de archivo no válido detectado"
        
        # Tamaño
        file.stream.seek(0, 2)
        size = file.stream.tell()
        file.stream.seek(0)
        if size > MAX_PHOTO_SIZE:
            return False, f"Tamaño máximo por archivo: {MAX_PHOTO_SIZE//1024//1024}MB"
    
    return True, ""

def validate_dates(start: str, end: str = None) -> tuple[bool, list[str]]:
    """Valida formato ISO y lógica de fechas"""
    errors = []
    now = datetime.now()
    
    # Formato inicio
    start_dt = None
    try:
        start_dt = datetime.fromisoformat(start)
        if start_dt < now:
            errors.append("La fecha de inicio no puede ser en el pasado")
    except ValueError:
        errors.append("Formato de fecha de inicio inválido (YYYY-MM-DDTHH:MM)")
    
    # Formato término
    if end and start_dt:
        try:
            end_dt = datetime.fromisoformat(end)
            if end_dt <= start_dt:
                errors.append("La fecha de término debe ser posterior al inicio")
        except ValueError:
            errors.append("Formato de fecha de término inválido (YYYY-MM-DDTHH:MM)")
    
    return (len(errors) == 0, errors)

def validate_contact(contact_type: str, value: str) -> tuple[bool, str]:
    """Valida formato según tipo de contacto"""
    patterns = {
        'whatsapp': (r'^\+569\d{8}$', "Formato: +569XXXXXXXX"),
        'instagram': (r'^@[\w.]+$', "Formato: @usuario"),
        'tiktok': (r'^@[\w.]+$', "Formato: @usuario"),
        'telegram': (r'^@[\w.]+$', "Formato: @usuario"),
        'X': (r'^@[\w.]+$', "Formato: @usuario"),
        'otra': (r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$', "Formato email válido")
    }
    
    if contact_type not in patterns:
        return False, "Tipo de contacto no válido"
    
    regex, msg = patterns[contact_type]
    return (bool(re.match(regex, value)), msg)

def validate_topic(topic: str, description: str = "") -> tuple[bool, str]:
    """Valida selección de tema y descripción si es 'otro'"""
    if topic not in VALID_TOPICS:
        return False, "Tema no válido"
    
    if topic == 'otro' and len(description.strip()) < 3:
        return False, "Debe describir el tema (mín. 3 caracteres)"
    
    return True, ""

def validate_field_length(value: str, field_name: str, 
                         max_length: int, required: bool = False) -> tuple[bool, str]:
    """Valida longitud de campos de texto"""
    if required and not value.strip():
        return False, f"{field_name} es obligatorio"
    
    if len(value) > max_length:
        return False, f"{field_name} no puede exceder {max_length} caracteres"
    
    return True, ""

# Función unificadora
def validate_form(data: dict, files: list) -> list[str]:
    """
    Realiza todas las validaciones del formulario
    Retorna: lista de strings con los errores encontrados
    """
    errors = defaultdict(list)
    
    # Campos obligatorios
    required_fields = {
        'comuna': "Comuna",
        'nombre': "Nombre del organizador",
        'email': "Email",
        'fecha_inicio': "Fecha de inicio",
        'tema': "Tema principal"
    }
    
    for field, name in required_fields.items():
        if not data.get(field):
            errors[field].append(f"{name} es obligatorio")
    
    # Validaciones individuales
    valid, msg = validate_email(data.get('email', ''))
    if not valid: errors['email'].append(msg)
    
    valid, msg = validate_phone(data.get('celular', ''))
    if not valid: errors['celular'].append(msg)
    
    valid, date_errors = validate_dates(
        data.get('fecha_inicio'), 
        data.get('fecha_termino')
    )
    if not valid: errors['fechas'].extend(date_errors)
    
    valid, msg = validate_photos(files)
    if not valid: errors['fotos'].append(msg)
    
    valid, msg = validate_topic(
        data.get('tema'), 
        data.get('tema_otro', '')
    )
    if not valid: errors['tema'].append(msg)
    
    # Validar contactos
    for i, (tipo, valor) in enumerate(data.get('contactos', [])):
        valid, msg = validate_contact(tipo, valor)
        if not valid:
            errors[f'contacto_{i}'].append(msg)
    
    # Validar longitudes
    length_checks = {
        'nombre': 200,
        'sector': 100,
        'descripcion': 500
    }
    
    for field, max_len in length_checks.items():
        valid, msg = validate_field_length(
            data.get(field, ''), 
            field.capitalize(), 
            max_len
        )
        if not valid: errors[field].append(msg)
    
    # Convertir el diccionario de errores a una lista de strings
    errores_lista = []
    for lista in errors.values():
        errores_lista.extend(lista)
    
    return errores_lista

def validate_comentario(nombre: str, texto: str) -> list[str]:
    """Valida los campos del formulario de comentario"""
    errores = []

    if not nombre or len(nombre.strip()) < 3:
        errores.append("El nombre debe tener al menos 3 caracteres.")
    elif len(nombre.strip()) > 80:
        errores.append("El nombre no puede tener más de 80 caracteres.")

    if not texto or len(texto.strip()) < 5:
        errores.append("El comentario debe tener al menos 5 caracteres.")

    return errores
