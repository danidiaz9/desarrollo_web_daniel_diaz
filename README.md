# Tarea 3 – Desarrollo de Aplicaciones Web

## Descripción del Proyecto

Esta aplicación web ha sido desarrollada con **Flask** (backend) y **MySQL** (base de datos) para gestionar actividades sociales. Sus principales características son:

- Registro y listado de actividades.
- Visualización detallada de cada actividad (incluyendo fotos y contactos).
- Comentarios en tiempo real (vía AJAX).
- Generación dinámica de estadísticas con gráficos.
- Validaciones robustas tanto en el cliente como en el servidor para datos y archivos.

## Estructura del Proyecto

```
flask_app/
├── app.py                         # Punto de entrada de la aplicación Flask
├── database/
│   ├── db.py                      # CRUD con SQLAlchemy y manejo de sesiones
│   └── models.py                  # Modelos declarativos de la base de datos
├── static/
│   ├── css/                       # Estilos (styles.css)
│   ├── js/                        # Lógica del frontend:
│   │   ├── formulario.js          # Validaciones y envíos de formularios
│   │   ├── listado.js             # Muestra detalles y amplía imágenes
│   │   └── estadisticas.js        # Carga y renderiza gráficos con Chart.js
│   ├── img/                       # Gráficos estáticos y assets
│   ├── icon/                      # Favicon e íconos
│   └── uploads/                   # Fotos subidas por usuarios
├── templates/
│   ├── base.html                  # Layout general con bloques Jinja2
│   ├── index.html                 # Página de inicio (últimas actividades)
│   ├── listado-actividades.html   # Listado con paginación y detalle AJAX
│   ├── detalle-actividad.html     # Vista detalle con formulario de comentarios AJAX
│   ├── informar-actividad.html    # Formulario de creación de actividad
│   └── estadisticas.html          # Dashboard de estadísticas (gráficos)
├── utils/
│   └── validations.py             # Validaciones de campos, fechas y archivos
├── requirements.txt               # Dependencias del proyecto
└── README.md                      # Documentación principal
```

## Puntos Clave y Decisiones

### 1. Separación Modular

- **`app.py`** contiene solo las rutas y la lógica de orquestación.
- **`database/db.py`** maneja sesiones y operaciones de base de datos con SQLAlchemy.

### 2. Validaciones

- Cliente: [`formulario.js`](flask_app/static/js/formulario.js) valida email, teléfono, fechas, fotos, temas y contactos antes de enviar.
- Servidor: [`validations.py`](flask_app/utils/validations.py) replica y refuerza esas validaciones, devolviendo listas de errores.

### 3. Comentarios en Tiempo Real (AJAX)

- Se creó la ruta **`GET/POST /api/actividad/<id>/comentarios`** que devuelve y recibe JSON.
- [`detalle-actividad.html`](flask_app/templates/detalle-actividad.html) usa `fetch()` en [`listado.js`](flask_app/static/js/listado.js) para:
  1. Cargar el listado inicial de comentarios.
  2. Enviar nuevos comentarios sin recargar la página.

### 4. Estadísticas Dinámicas

- Se expone **`GET /api/estadisticas`** que agrupa datos de actividades por día, tipo y horarios por mes.
- [`estadisticas.html`](flask_app/templates/estadisticas.html) y [`estadisticas.js`](flask_app/static/js/estadisticas.js) utilizan **Chart.js** para mostrar:
  - Gráfico de líneas (actividades por día).
  - Gráfico de torta (actividades por tipo).
  - Gráfico de barras (actividades por horario y mes).

### 5. Manejo de Archivos

- Rutas seguras con `secure_filename` y nombres hasheados (`hashlib.sha256`) para evitar colisiones.
- Validación de extensiones y MIME type usando la librería `filetype`.
