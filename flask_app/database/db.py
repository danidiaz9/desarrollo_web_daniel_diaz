from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from .models import Region, Comuna, Actividad, Foto, ContactarPor, ActividadTema, Comentario

# Configuración de la base de datos
DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

# --- Database Functions ---

def get_regiones():
    session = SessionLocal()
    regiones = session.query(Region).all()
    session.close()
    return regiones

def get_regiones_por_id(region_id):
    session = SessionLocal()
    region = session.query(Region).filter_by(id=region_id).first()
    session.close()
    return region

def get_comunas():
    session = SessionLocal()
    comunas = session.query(Comuna).all()
    session.close()
    return comunas

def get_comunas_por_region(region_id):
    session = SessionLocal()
    comunas = session.query(Comuna).filter_by(region_id=region_id).all()
    session.close()
    return comunas

def get_comuna_por_id(comuna_id):
    session = SessionLocal()
    comuna = session.query(Comuna).filter_by(id=comuna_id).first()
    session.close()
    return comuna

# --- Actividades ---

def create_actividad(comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion):
    session = SessionLocal()
    new_actividad = Actividad(
        comuna_id=comuna_id,
        sector=sector,
        nombre=nombre,
        email=email,
        celular=celular,
        dia_hora_inicio=dia_hora_inicio,
        dia_hora_termino=dia_hora_termino,
        descripcion=descripcion
    )
    session.add(new_actividad)
    session.commit()
    session.close() 

def get_actividades():
    session = SessionLocal()
    actividades = session.query(Actividad).options(
        joinedload(Actividad.comuna),
        joinedload(Actividad.fotos),
        joinedload(Actividad.temas),
        joinedload(Actividad.contactos)
    ).all()
    session.close()
    return actividades

def get_actividad_por_id(actividad_id):
    session = SessionLocal()
    actividad = session.query(Actividad).options(
        joinedload(Actividad.comuna),
        joinedload(Actividad.fotos),
        joinedload(Actividad.temas),
        joinedload(Actividad.contactos),
        joinedload(Actividad.comentarios)
    ).filter_by(id=actividad_id).first()
    session.close()
    return actividad

def get_actividad_por_campos(nombre, email, dia_hora_inicio):
    session = SessionLocal()
    actividad = session.query(Actividad).filter_by(
        nombre = nombre,
        email = email,
        dia_hora_inicio = dia_hora_inicio
    ).first()
    session.close()
    return actividad

# --- Fotos ---
def create_foto(actividad_id, filename):
    session = SessionLocal()
    # filename debe ser solo el nombre del archivo, la ruta la defines tú
    ruta_archivo = f"static/uploads/{filename}"
    new_foto = Foto(
        actividad_id=actividad_id,
        ruta_archivo=ruta_archivo,
        nombre_archivo=filename
    )
    session.add(new_foto)
    session.commit()
    session.close()

def get_fotos():
    session = SessionLocal()
    fotos = session.query(Foto).all()
    session.close()
    return fotos

# --- Contactos ---
def create_contacto(nombre, identificador, actividad_id):
    session = SessionLocal()
    new_contacto = ContactarPor(
        nombre=nombre,  # tipo de contacto: 'whatsapp', 'telegram', etc.
        identificador=identificador,
        actividad_id=actividad_id
    )
    session.add(new_contacto)
    session.commit()
    session.close()

def get_contactos():
    session = SessionLocal()
    contactos = session.query(ContactarPor).all()
    session.close()
    return contactos

# --- Temas ---
def create_tema(tema, glosa_otro, actividad_id):
    session = SessionLocal()
    new_tema = ActividadTema(
        tema=tema,  # debe coincidir con los valores del Enum en el modelo
        glosa_otro=glosa_otro,
        actividad_id=actividad_id
    )
    session.add(new_tema)
    session.commit()
    session.close()

def get_temas():
    session = SessionLocal()
    temas = session.query(ActividadTema).all()
    session.close()
    return temas

# --- Comentarios ---
def create_comentario(nombre, texto, fecha, actividad_id):
    session = SessionLocal()
    new_comentario = Comentario(
        nombre=nombre,
        texto=texto,
        fecha=fecha,
        actividad_id=actividad_id
    )
    session.add(new_comentario)
    session.commit()
    session.close()

def get_comentarios():
    session = SessionLocal()
    comentarios = session.query(Comentario).all()
    session.close()
    return comentarios

def get_comentarios_por_actividad(actividad_id):
    session = SessionLocal()
    comentarios = session.query(Comentario).filter_by(actividad_id=actividad_id).all()
    session.close()
    return comentarios