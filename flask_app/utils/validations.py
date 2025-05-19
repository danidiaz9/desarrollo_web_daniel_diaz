import re
from datetime import datetime

# --- Validación de archivos ---
def allowed_file(filename, allowed_extensions={'png', 'jpg', 'jpeg'}):
    """Valida la extensión de un archivo"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def validate_file_size(file_stream, max_size=5*1024*1024):
    """Valida el tamaño de un archivo (5MB por defecto)"""
    file_stream.seek(0, 2)  # Ir al final del archivo
    size = file_stream.tell()
    file_stream.seek(0)  # Resetear posición
    return size <= max_size, f"El archivo excede el tamaño máximo de {max_size//1024//1024}MB"

# --- Validación de datos del formulario ---
def validate_phone(number):
    """Valida formato de teléfono chileno: +569XXXXXXXX"""
    if not number:
        return True, None
    pattern = r'^\+569\d{8}$'
    return (re.match(pattern, number) is not None, 
            "Formato debe ser +569 seguido de 8 dígitos")

def validate_email(email):
    """Valida formato básico de email"""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return (re.match(pattern, email) is not None, 
            "Formato de email inválido")

def validate_select_field(value, field_name):
    """Valida que un campo de selección tenga valor"""
    return (bool(value), 
            f"Debe seleccionar {field_name}")

def validate_text_length(text, max_length, field_name):
    """Valida longitud máxima de texto"""
    if not text:
        return True, None
    return (len(text) <= max_length, 
            f"{field_name} excede el máximo de {max_length} caracteres")

def validate_photos(files, min=1, max=5):
    """Valida cantidad de fotos subidas"""
    uploaded_files = [f for f in files if f.filename != '']
    return (min <= len(uploaded_files) <= max, 
            f"Debe subir entre {min} y {max} fotos")

# --- Validación de fechas ---
def validate_fechas(fecha_inicio, fecha_termino=None):
    """Valida lógica de fechas:
    - fecha_inicio no puede ser en el pasado
    - fecha_termino debe ser posterior a fecha_inicio (si existe)
    """
    ahora = datetime.now()
    errores = []
    
    # Validar fecha inicio
    if fecha_inicio < ahora:
        errores.append("La fecha de inicio no puede ser en el pasado")
    
    # Validar fecha término
    if fecha_termino:
        if fecha_termino <= fecha_inicio:
            errores.append("La fecha de término debe ser posterior a la de inicio")
    
    return (len(errores) == 0, errores)

# --- Validación tema personalizado ---
def validate_custom_topic(topic, glosa):
    """Valida lógica del campo 'otro' en temas"""
    if topic == 'otro':
        return (len(glosa) >= 3, 
                "Descripción del tema debe tener al menos 3 caracteres")
    return True, None

# --- Validación de contactos ---
def validate_contacto(tipo, valor):
    """Valida formato específico para cada tipo de contacto"""
    validaciones = {
        'whatsapp': (r'^\+569\d{8}$', "Formato WhatsApp: +569XXXXXXXX"),
        'instagram': (r'^@[\w.]+$', "Formato Instagram: @usuario"),
        'telegram': (r'^@[\w.]+$', "Formato Telegram: @usuario"),
        'X': (r'^@[\w.]+$', "Formato X: @usuario"),
        'tiktok': (r'^@[\w.]+$', "Formato TikTok: @usuario"),
        'otra': (r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$', "Formato email válido")
    }
    
    if tipo not in validaciones:
        return False, "Tipo de contacto no válido"
    
    pattern, mensaje = validaciones[tipo]
    return (re.match(pattern, valor) is not None, mensaje)

def validate_contactos(contactos, max=5):
    """Valida lista completa de contactos"""
    if len(contactos) > max:
        return False, f"Máximo {max} métodos de contacto permitidos"
    
    for tipo, valor in contactos:
        valido, mensaje = validate_contacto(tipo, valor)
        if not valido:
            return False, f"Error en {tipo}: {mensaje}"
    
    return True, None

# --- Validación de horarios ---
def validate_horario(inicio, termino=None):
    """Valida formato datetime-local"""
    try:
        datetime.fromisoformat(inicio)
        if termino:
            datetime.fromisoformat(termino)
        return True, None
    except ValueError:
        return False, "Formato de fecha inválido (usar YYYY-MM-DDTHH:MM)"