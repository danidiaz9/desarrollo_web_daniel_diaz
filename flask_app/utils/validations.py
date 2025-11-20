import re
import filetype
from datetime import datetime

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
    """Valida formato de email"""
    if not email:
        return False, "El email es obligatorio"
    return bool(EMAIL_REGEX.match(email)), "Formato de email inválido (ej: usuario@dominio.com)"


def validate_phone(number: str) -> tuple[bool, str]:
    """Valida formato de teléfono"""
    if not number:
        return True, ""
    return bool(PHONE_REGEX.match(number)), "Formato debe ser +569 seguido de 8 dígitos"


def validate_photos(files: list, min: int = 1, max: int = MAX_PHOTOS) -> tuple[bool, str]:
    """Valida archivos de imagen con chequeo de MIME type y tamaño"""
    valid_files = []
    for f in files:
        if getattr(f, 'filename', None) and f.filename.strip():
            f.stream.seek(0, 2)
            size = f.stream.tell()
            f.stream.seek(0)
            if size > 0:
                valid_files.append(f)

    if not (min <= len(valid_files) <= max):
        return False, f"Debe subir entre {min} y {max} fotos"

    for file in valid_files:
        if not allowed_file(file.filename):
            return False, f"Solo se permiten archivos {', '.join(ALLOWED_EXTENSIONS)}"

        mime = filetype.guess(file.stream.read(2048))
        file.stream.seek(0)
        if not mime or mime.mime not in ALLOWED_MIMETYPES:
            return False, "Tipo de archivo no válido detectado"

        file.stream.seek(0, 2)
        size = file.stream.tell()
        file.stream.seek(0)
        if size > MAX_PHOTO_SIZE:
            return False, f"Tamaño máximo por archivo: {MAX_PHOTO_SIZE // 1024 // 1024}MB"

    return True, ""


def validate_dates(start: str, end: str = None) -> tuple[bool, list[str]]:
    """Valida formato ISO y lógica de fechas"""
    errores = []
    now = datetime.now()

    start_dt = None
    try:
        start_dt = datetime.fromisoformat(start)
        if start_dt < now:
            errores.append("La fecha de inicio no puede ser en el pasado")
    except ValueError:
        errores.append("Formato de fecha de inicio inválido (YYYY-MM-DDTHH:MM)")

    if end and start_dt:
        try:
            end_dt = datetime.fromisoformat(end)
            if end_dt <= start_dt:
                errores.append("La fecha de término debe ser posterior al inicio")
        except ValueError:
            errores.append("Formato de fecha de término inválido (YYYY-MM-DDTHH:MM)")

    return len(errores) == 0, errores


def validate_contact(contact_type: str, value: str) -> tuple[bool, str]:
    """Valida formato según tipo de contacto"""
    if contact_type == 'whatsapp':
        return bool(re.match(r'^\+569\d{8}$', value)), "Formato: +569XXXXXXXX"
    elif contact_type in {'instagram', 'tiktok', 'telegram', 'X'}:
        return bool(re.match(r'^@[\w.]+$', value)), "Formato: @usuario"
    elif contact_type == 'otra':
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value)), "Formato email válido"
    else:
        return False, "Tipo de contacto no válido"


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


def validate_form(data: dict, files: list) -> list[str]:
    """Valida el formulario principal de actividad"""
    errores = []

    if not data.get('comuna'):
        errores.append("Comuna es obligatoria")
    if not data.get('nombre'):
        errores.append("Nombre del organizador es obligatorio")
    if not data.get('email'):
        errores.append("Email es obligatorio")
    if not data.get('fecha_inicio'):
        errores.append("Fecha de inicio es obligatoria")
    if not data.get('tema'):
        errores.append("Tema principal es obligatorio")

    valid, msg = validate_email(data.get('email', ''))
    if not valid:
        errores.append(msg)

    valid, msg = validate_phone(data.get('celular', ''))
    if not valid:
        errores.append(msg)

    valid, date_errors = validate_dates(
        data.get('fecha_inicio'),
        data.get('fecha_termino')
    )
    if not valid:
        errores.extend(date_errors)

    valid, msg = validate_photos(files)
    if not valid:
        errores.append(msg)

    valid, msg = validate_topic(
        data.get('tema'),
        data.get('tema_otro', '')
    )
    if not valid:
        errores.append(msg)

    for i, (tipo, valor) in enumerate(data.get('contactos', [])):
        valid, msg = validate_contact(tipo, valor)
        if not valid:
            errores.append(f"Contacto {i + 1}: {msg}")

    campos_largo = [
        ('nombre', 200, "Nombre del organizador"),
        ('sector', 100, "Sector"),
        ('descripcion', 500, "Descripción")
    ]

    for field, max_len, label in campos_largo:
        valid, msg = validate_field_length(
            data.get(field, ''),
            label,
            max_len
        )
        if not valid:
            errores.append(msg)

    return errores


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
