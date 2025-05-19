# Tarea 2 – Desarrollo de Aplicaciones Web  

## Descripción del Proyecto

Desarrollada con Flask y MySQL

## Estructura del Proyecto

El repositorio tiene la siguiente estructura:
```
├── database/
│   ├── db.py            # Funciones de acceso a datos
│   ├── models.py        # Modelos SQLAlchemy
│   └── *.sql            # Scripts de base de datos
├── templates/
│   └── *.html           # Plantillas Jinja2
├── static/
│   ├── css/             # Estilos CSS
│   ├── js/              # Scripts JavaScript
│   └── uploads/         # Imágenes subidas
├── utils/
│   └── validations.py   # Validaciones del servidor
├── app.py               # Aplicación principal
└── requirements.txt     # Dependencias
```
## Desiciones del Proyecto:

- Separación modular del proyecto
- Validación de archivos
- Estilos simples