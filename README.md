# Tarea 4 – Desarrollo de Aplicaciones Web

## Descripción del Proyecto

Esta aplicación web permite evaluar actividades sociales. Está desarrollada con **Spring Boot** (Java), **Thymeleaf** para las vistas y **MySQL** como base de datos.

## Estructura del Proyecto

```
tarea4/
├── db/                        # Scripts SQL para la creación y carga de la base de datos
│   └── *.sql
├── pom.xml                    # Archivo de configuración de Maven (dependencias y build)
├── README.md                  # Documentación y guía del proyecto
└── src/
    ├── main/
    │   ├── java/
    │   │   └── appsweb/
    │   │       └── tareas/
    │   │           └── tarea4/
    │   │               ├── controllers/    # Controladores web y API (Spring MVC)
    │   │               ├── models/         # Entidades JPA (mapeo de tablas)
    │   │               ├── repositories/   # Interfaces de acceso a datos (Spring Data JPA)
    │   │               └── services/       # Lógica de servicios de la aplicación
    │   └── resources/
    │       ├── static/
    │       │   ├── css/                   # Archivos CSS estáticos
    │       │   └── js/                    # Archivos JavaScript estáticos
    │       ├── templates/                 # Vistas Thymeleaf (HTML)
    │       └── application.properties     # Configuración de la aplicación (DB, puerto, etc.)
    └── test/
        └── java/
            └── appsweb/
                └── tareas/
                    └── tarea4/
```

## Principales Características

- **Evaluación de actividades**: Se pueden asignar notas (1 a 7) a cada actividad finalizada, calculando el promedio automáticamente.
- **Frontend dinámico**: El listado de actividades y la evaluación de notas se realiza mediante AJAX, sin recargar la página.
- **Validaciones robustas**: Tanto en el backend (restricciones de notas, integridad de datos) como en el frontend (validación de rango y tipo de nota).

## Decisiones de Diseño y Detalles Técnicos

### 1. Separación de Capas

- **Controladores**: Gestionan las rutas web y API, separando claramente las vistas (Thymeleaf) de los endpoints REST.
- **Servicios**: Encapsulan la lógica de negocio, como el cálculo de promedios y la validación de notas.
- **Repositorios**: Usan Spring Data JPA para acceder a la base de datos de forma declarativa.

### 2. AJAX y Experiencia de Usuario

- El frontend utiliza JavaScript para cargar y actualizar la tabla de actividades mediante fetch y JSON, permitiendo una experiencia fluida y sin recargas.
- Al evaluar una actividad, la tabla se actualiza automáticamente.

### 3. Validaciones

- **Backend**: Se valida que las notas estén en el rango permitido (1 a 7).
- **Frontend**: Se valida el input del usuario antes de enviar la nota, mostrando mensajes claros en caso de error.

## Cómo Ejecutar

1. Configura la base de datos MySQL y ejecuta los scripts en `db/`.
2. Ajusta las credenciales en `src/main/resources/application.properties` si es necesario.
3. Compila y ejecuta con Maven:
   ```sh
   ./mvnw spring-boot:run
   ```
4. Accede a la aplicación en [http://localhost:8080](http://localhost:8080).

---
