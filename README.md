docker-compose build
docker-compose up
# mvc_adios_al_silencio

Aplicación web sencilla basada en el patrón MVC pensada para gestionar el acceso de tutores y niños a un conjunto de vistas de lecciones e información. Incluye flujo de registro, inicio de sesión, área de administración y manejo de sesiones persistentes sobre un backend de datos en Supabase.

El objetivo del proyecto es servir como base de una plataforma educativa ligera donde:
- Un administrador/tutor puede registrarse, iniciar sesión y gestionar su perfil.
- Se pueden registrar niños asociados a un tutor.
- Los niños pueden acceder con sus credenciales a un conjunto de pantallas de presentación y lecciones.
- Se sirven recursos estáticos (imágenes y audio) para acompañar las actividades.

---

## Tecnologías utilizadas

- **Lenguaje:** Python 3
- **Framework web:** [web.py](https://webpy.org/) (enfoque minimalista tipo MVC)
- **Base de datos / BaaS:** [Supabase](https://supabase.com/) vía SDK de Python
- **Gestión de sesiones:** `web.session` con almacenamiento en disco
- **Plantillas y vistas:** `web.template` con HTML en `aplicacion/views/`
- **Recursos estáticos:** imágenes y audio servidos desde `aplicacion/static/`
- **Contenedores:** Docker + `docker-compose` para construcción y ejecución

---

## Qué problema resuelve

Este proyecto aborda necesidades típicas de una aplicación web educativa básica:

- **Gestión de usuarios tutores:** registro, autenticación y edición de perfil.
- **Asociación tutor–niño:** registro de niños vinculados a un tutor.
- **Acceso diferenciado:** rutas y vistas para administradores/tutores y para niños.
- **Organización de contenido educativo:** páginas de introducción, lecciones y pantallas de presentación.
- **Persistencia en la nube:** almacenamiento de tutores y niños sobre Supabase, evitando gestionar una base de datos propia.

No pretende ser una solución completa en producción, sino una base clara y extensible para seguir aprendiendo sobre desarrollo web backend, manejo de sesiones y despliegue con Docker.

---

## Estructura del proyecto

La carpeta principal de la aplicación es `aplicacion/`:

- `aplicacion/app.py`: punto de entrada de la aplicación web, configuración de rutas, sesiones y servidor.
- `aplicacion/controllers/`: controladores que manejan las rutas (inicio, registro, login, perfil, lecciones, páginas estáticas, etc.).
- `aplicacion/models/db.py`: integración con Supabase y operaciones sobre tutores y niños.
- `aplicacion/views/`: plantillas HTML para las distintas pantallas (inicio, introducción, lecciones, perfil administrador, registro de tutor/niño, etc.).
- `aplicacion/static/`: recursos estáticos (imágenes y audio) utilizados por las vistas.

En la raíz del repositorio se encuentran además:

- `Dockerfile`: definición de la imagen Docker de la aplicación.
- `docker-compose.yaml`: orquestación para desarrollo/ejecución local.
- `requirements.txt`: dependencias de Python.

---

## Endpoints principales

Los controladores definidos en `aplicacion/app.py` exponen los siguientes endpoints HTTP principales (método `GET` salvo que el formulario use `POST` para enviar datos):

| Ruta                    | Método(s)        | Descripción                                                   |
|-------------------------|------------------|----------------------------------------------------------------|
| `/`                     | GET              | Página principal / inicio.                                   |
| `/registrar_tutor`      | GET, POST        | Formulario de registro de tutor/administrador.               |
| `/registrar_chiquillo`  | GET, POST        | Registro de niños asociados a un tutor.                      |
| `/inicio_administrador` | GET, POST        | Inicio de sesión para administradores/tutores.               |
| `/perfil_admin`         | GET              | Perfil de administrador/tutor autenticado.                   |
| `/editar_perfil`        | GET, POST        | Edición de datos del perfil de administrador/tutor.          |
| `/iniciar_sesion`       | GET, POST        | Inicio de sesión para niños.                                 |
| `/saludo_admin`         | GET              | Pantalla de saludo para administrador.                       |
| `/saludo_chiquillo`     | GET              | Pantalla de saludo para niño.                                |
| `/presentacion_lucas`   | GET              | Presentación del personaje principal.                        |
| `/presentacion_pagina`  | GET              | Presentación general de la página.                           |
| `/lecciones`            | GET              | Listado de lecciones disponibles.                            |
| `/introduccion`         | GET              | Lección de introducción.                                     |
| `/leccion_coordinacion` | GET              | Lección de coordinación.                                     |
| `/leccion_completada`   | GET              | Pantalla de lección completada.                              |
| `/quienes_somos`        | GET              | Página "Quiénes somos".                                     |
| `/cerrar_sesion`        | GET              | Cierre de sesión y limpieza de datos de usuario.             |
| `/static/*`             | GET              | Archivos estáticos (imágenes, audio, CSS, etc.).             |
| `/favicon.ico`          | GET              | Icono del sitio.                                             |

---

## Requisitos previos

- Docker instalado
- Docker Compose instalado
- Cuenta y proyecto configurado en Supabase
- Variables de entorno de Supabase:
	- `SUPABASE_URL`
	- `SUPABASE_KEY`

Estas variables pueden definirse directamente en el entorno o en un archivo `.env` en la raíz de `aplicacion/` (la carga básica ya está implementada en `aplicacion/models/db.py`).

---

	## Instalación local (sin Docker)

	1. Crear y activar un entorno virtual (opcional pero recomendado):

		```bash
		python -m venv .venv
		source .venv/bin/activate
		```

	2. Instalar dependencias de Python:

		```bash
		pip install -r requirements.txt
		```

	3. Configurar las variables de entorno de Supabase (`SUPABASE_URL`, `SUPABASE_KEY`).

	4. Ejecutar la aplicación desde la carpeta `aplicacion/`:

		```bash
		cd aplicacion
		python app.py
		```

	La aplicación se expondrá en el puerto configurado en `app.py` (por defecto `8080`).

	---

## Puesta en marcha con Docker Compose

Construir la imagen localmente:

```bash
docker-compose build
```

Levantar la aplicación:

```bash
docker-compose up
```

Por defecto, el servidor se expone en `http://0.0.0.0:8080` (según la configuración en `aplicacion/app.py`), aunque puedes ajustar las variables de entorno `HOST` y `PORT` si lo necesitas.

---

## Uso de la imagen publicada

También puedes partir de la imagen pública ya construida:

```bash
docker pull christian7777/mvc_adios_al_silencio:v1
```

Y luego ejecutarla (ajustando variables de entorno para Supabase y el puerto si es necesario):

```bash
docker run --env SUPABASE_URL=... \
					 --env SUPABASE_KEY=... \
					 -p 8080:8080 \
					 christian7777/mvc_adios_al_silencio:v1
```

---

## Autores

- Christian Eduardo Navarro Curiel
- Landy Alberto Tolentino Olmedo
- Aracely Perez Rodriguez


---

Este repositorio queda así como un punto de partida claro para seguir iterando sobre un proyecto realista de backend web en Python.
