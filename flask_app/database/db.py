from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, joinedload
from .models import Region, Comuna, Actividad, Foto, ContactarPor, ActividadTema

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
    region = session.query(Region).get(region_id)
    session.close()
    return region

def get_comunas():
    session = SessionLocal()
    comunas = session.query(Comuna).order_by(Comuna.nombre).all()
    session.close()
    return comunas

def get_comunas_por_region(region_id):
    session = SessionLocal()
    comunas = session.query(Comuna).filter_by(region_id=region_id).all()
    session.close()
    return comunas

def get_comuna_por_id(comuna_id):
    session = SessionLocal()
    comuna = session.query(Comuna).get(comuna_id)
    session.close()
    return comuna

def create_actividad(actividad_data, temas_data, contactos_data, fotos_data):
    session = SessionLocal()
    try:
        nueva_actividad = Actividad(**actividad_data)
        session.add(nueva_actividad)
        session.flush()
        
        for tema in temas_data:
            session.add(ActividadTema(actividad_id=nueva_actividad.id, **tema))
            
        for contacto in contactos_data:
            session.add(ContactarPor(actividad_id=nueva_actividad.id, **contacto))
            
        for foto in fotos_data:
            session.add(Foto(actividad_id=nueva_actividad.id, **foto))
            
        session.commit()
        return nueva_actividad.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_ultimas_actividades(num):
    session = SessionLocal()
    try:
        actividades = session.query(Actividad)\
            .options(
                joinedload(Actividad.comuna),
                joinedload(Actividad.fotos),
                joinedload(Actividad.temas),
                joinedload(Actividad.contactos)
            )\
            .order_by(Actividad.dia_hora_inicio.desc())\
            .limit(num)\
            .all()
        return actividades
    finally:
        session.close()

def get_actividades_paginadas(page=1, per_page=5):
    session = SessionLocal()
    try:
        actividades = session.query(Actividad)\
            .options(
                joinedload(Actividad.comuna),
                joinedload(Actividad.fotos),
                joinedload(Actividad.temas),
                joinedload(Actividad.contactos)
            )\
            .order_by(Actividad.dia_hora_inicio.desc())\
            .offset((page - 1) * per_page)\
            .limit(per_page)\
            .all()
        
        total = session.query(Actividad).count()
        return actividades, total

    finally:
        session.close()

def get_actividad_por_id(actividad_id):
    session = SessionLocal()
    try:
        actividad = session.query(Actividad)\
            .options(
                joinedload(Actividad.comuna).joinedload(Comuna.region),
                joinedload(Actividad.fotos),
                joinedload(Actividad.temas),
                joinedload(Actividad.contactos)
            )\
            .filter_by(id=actividad_id)\
            .first()
        return actividad

    finally:
        session.close()

def get_fotos_por_actividad(actividad_id):
    session = SessionLocal()
    try:
        fotos = session.query(Foto)\
            .filter(Foto.actividad_id==actividad_id)\
            .all()
        return fotos
    
    finally:
        session.close()

def get_contar_actividades_por_tema():
    session = SessionLocal()
    try:
        cantidad = session.query(
            ActividadTema.tema, 
            func.count(ActividadTema.id).label('cantidad')
            ).group_by(ActividadTema.tema).all()
        return cantidad
    finally:
        session.close()

def get_contar_actividades_por_comuna():
    session = SessionLocal()
    try:
        cantidad = session.query(
            Comuna.nombre, 
            func.count(Actividad.id).label('cantidad')
            ).join(Actividad)\
            .group_by(Comuna.nombre)\
            .order_by(func.count(Actividad.id).desc())\
            .all()
        return cantidad
    finally:
        session.close()

def get_temas():
    return [
        "musica",
        "deporte",
        "ciencias",
        "religion",
        "politica",
        "tecnologia",
        "juegos",
        "baile",
        "comida",
        "otro"
    ]