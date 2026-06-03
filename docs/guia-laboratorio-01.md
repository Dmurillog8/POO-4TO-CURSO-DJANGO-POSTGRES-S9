# Guía de Laboratorio 01 — Configuración base y proyecto Django

> **Parte 1 de 3** · ⏱ Duración estimada: **1.5 – 2 horas**
> **Asignatura:** Programación Orientada a Objetos (4to curso)
> **Stack del laboratorio completo:** Django 5 + DRF · Vite + React + TypeScript · PostgreSQL o MySQL
> **Alcance de esta parte:** preparar el entorno, crear el proyecto Django, instalar dependencias, dividir settings y conectar la base de datos. El proyecto queda listo para empezar a modelar.
> **Recomendado antes de empezar:** leer la [Referencia del Framework Django](./referencias-django.md) para tener el mapa mental completo (MVT, ORM, Views, Middleware).

| 📘 Esta guía | ➡️ Siguiente | 🏁 Cierre |
|---|---|---|
| **01** Configuración base | [02 — Backend Django (modelos, API, JWT)](./guia-laboratorio-02.md) | [03 — Frontend React + UML](./guia-laboratorio-03.md) |

---

## Tabla de contenido

1. [Objetivos de aprendizaje](#1-objetivos-de-aprendizaje)
2. [Prerrequisitos](#2-prerrequisitos)
3. [Convenciones del laboratorio](#3-convenciones-del-laboratorio)
4. [Arquitectura objetivo](#4-arquitectura-objetivo)
5. [Fase 0 — Preparación del entorno](#5-fase-0--preparación-del-entorno)
6. [Fase 1 — Backend: entorno virtual y proyecto base](#6-fase-1--backend-entorno-virtual-y-proyecto-base)
7. [Fase 2 — Backend: dependencias, .env y settings divididos](#7-fase-2--backend-dependencias-env-y-settings-divididos)
8. [Fase 3 — Backend: base de datos (PostgreSQL o MySQL)](#8-fase-3--backend-base-de-datos-postgresql-o-mysql)

> **Punto de control al final de esta guía:** el servidor Django arranca, la base de datos está conectada y `python manage.py check` no reporta errores. Listo para empezar a modelar en la **Parte 2**.

---

## 1. Objetivos de aprendizaje

Al finalizar **esta primera parte**, el estudiante será capaz de:

- **Configurar** un entorno virtual de Python (`venv`) y justificar su uso dentro del paradigma de encapsulamiento y aislamiento.
- **Crear** un proyecto Django desde cero y verificar su arranque.
- **Estructurar** un proyecto Django modular separando configuración de dominio (`config/` + `apps/`).
- **Aplicar** el patrón de *settings divididos* (base/dev/prod) y leer configuración desde variables de entorno — primera aplicación práctica de **Inversión de Dependencias (DIP)**.
- **Conectar** el proyecto a una base de datos relacional seleccionable por configuración.

Los objetivos restantes (modelado, API REST, JWT, React, UML) se cubren en las **Partes 2 y 3**.

---

## 2. Prerrequisitos

| Herramienta | Versión | Verificación |
|---|---|---|
| Python | 3.12.x | `python --version` |
| pip    | 24.x  | `pip --version` |
| Node.js | 20 LTS o superior (mínimo 18) | `node --version` |
| npm    | 10.x | `npm --version` |
| Git    | 2.40+ | `git --version` |
| PowerShell | 5.1+ (incluido en Windows 10/11) | `$PSVersionTable.PSVersion` |
| PostgreSQL | 14+ *(opcional — puede usar MySQL)* | `psql --version` |
| MySQL/MariaDB | 8.0+ *(opcional — puede usar Postgres)* | `mysql --version` |
| Visual Studio Code | 1.85+ | Extensiones recomendadas: *Python*, *Pylance*, *ESLint*, *PlantUML* |

> Si no dispone de Postgres o MySQL, puede usar SQLite como reemplazo temporal (no recomendado para producción), cambiando `DB_ENGINE=django.db.backends.sqlite3` en `.env`.

### 2.1 ¿Cómo instalar o actualizar a la versión requerida?

Si al ejecutar el comando de *Verificación* de la tabla anterior obtiene una versión más antigua (o un error de "comando no encontrado"), siga las instrucciones de esta subsección. Todos los métodos están pensados para **Windows**.

#### Ruta rápida (recomendada para el laboratorio): usar `winget`

`winget` es el gestor de paquetes oficial de Windows 10/11. Si no lo tiene, instale *App Installer* desde la Microsoft Store.

Abra **PowerShell como Administrador** y ejecute (puede omitir lo que ya tenga actualizado):

```powershell
# Python 3.12
winget install -e --id Python.Python.3.12 --source winget

# Node.js 20 LTS
winget install -e --id OpenJS.NodeJS.LTS --source winget

# Git
winget install -e --id Git.Git --source winget

# Visual Studio Code
winget install -e --id Microsoft.VisualStudioCode --source winget

# PostgreSQL 16
winget install -e --id PostgreSQL.PostgreSQL.16 --source winget

# MySQL 8 (Server + Workbench)
winget install -e --id Oracle.MySQL --source winget
```

> Después de instalar, **cierre y vuelva a abrir PowerShell** para que reconozca los nuevos `PATH`. Luego verifique con los comandos de la tabla de prerrequisitos.

#### Ruta avanzada: gestores de versión (recomendado si trabaja con varios proyectos)

| Herramienta | Gestor de versiones | Comando clave |
|---|---|---|
| Python | [**pyenv-win**](https://github.com/pyenv-win/pyenv-win) | `pyenv install 3.12.4` · `pyenv global 3.12.4` |
| Node.js | [**nvm-windows**](https://github.com/coreybutler/nvm-windows) | `nvm install 20.11.0` · `nvm use 20.11.0` |

**Ventaja clave**: el archivo `backend/.python-version` (3.12.4) y `frontend/.nvmrc` (20.11.0) que ya existen en el proyecto hacen que estos gestores cambien **automáticamente** a la versión correcta al entrar a cada carpeta:

```powershell
# Dentro de backend/
pyenv local 3.12.4
python --version
# Python 3.12.4

# Dentro de frontend/
nvm use           # lee el .nvmrc y cambia a 20.11.0
node --version
# v20.11.0
```

#### Ruta manual: descarga directa del instalador

| Herramienta | URL | Notas |
|---|---|---|
| Python | <https://www.python.org/downloads/windows/> | Marque **"Add Python to PATH"** en el instalador |
| Node.js | <https://nodejs.org/en/download> | Elija la pestaña **20.x.x LTS** |
| Git | <https://git-scm.com/download/win> | Use las opciones por defecto |
| PostgreSQL | <https://www.postgresql.org/download/windows/> | Recuerde la contraseña del superusuario `postgres` |
| MySQL | <https://dev.mysql.com/downloads/installer/> | Elija *Custom* y seleccione Server + Workbench |
| MariaDB | <https://mariadb.org/download/> | Alternativa 100% open source a MySQL |
| Visual Studio Code | <https://code.visualstudio.com/download> | — |

#### Actualizar `pip` y `npm` (ya incluidos con Python/Node)

```powershell
# pip
python -m pip install --upgrade pip

# npm (requiere Node >= 18.17 o >= 20.17 según la versión de npm)
npm install -g npm
```

---

## 3. Convenciones del laboratorio

- **Ruta base** del proyecto: `D:\UNEMI\2026\PERIODO-ABRIL-JUNIO\POO\POO-4TO-CURSO-DJANGO-POSTGRES-REACT`
- **Nombres en snake_case** para archivos Python (`user_serializer.py`).
- **Nombres en PascalCase** para clases y componentes React (`LoginPage`).
- **Indentación:** 4 espacios en Python, 2 espacios en TypeScript/JSON.
- Cada bloque de código muestra la **ruta** del archivo donde se pega el contenido.
- Los bloques que comienzan con `$` son comandos de **PowerShell**.

> **Buena práctica (POO):** cada archivo debe tener una única responsabilidad. Si un archivo crece más allá de ~200 líneas, es una señal para dividirlo.

### 3.1 ¿Terminal, explorador de Windows o editor? ¿Cuándo usar cada uno?

Esta guía muestra los comandos en **PowerShell** porque es la forma reproducible y profesional de trabajar. Sin embargo, **no todas las operaciones requieren la terminal**. A continuación se resume cuándo usar cada herramienta:

| Operación | ¿Se puede hacer en GUI? | Herramienta recomendada |
|---|---|---|
| Abrir / explorar carpetas | ✅ Sí (doble clic en el Explorador de Windows) | **Explorador de Windows** o terminal |
| Crear carpetas nuevas | ✅ Sí (clic derecho → *Nuevo* → *Carpeta*) | **Explorador de Windows** o terminal |
| Crear archivos vacíos | ✅ Sí (clic derecho → *Nuevo* → *Documento de texto*; luego renombrar) | **VSCode** o terminal |
| Crear archivos con contenido | ✅ Sí (en VSCode: *Archivo* → *Nuevo*, pegar, guardar) | **VSCode** |
| Editar `.env` o cualquier archivo de texto | ✅ Sí | **VSCode** o *Bloc de notas* |
| Crear/activar el entorno virtual (`venv`) | ❌ **No** — requiere intérprete Python | **PowerShell** |
| Instalar dependencias (`pip install`, `npm install`) | ❌ **No** — requiere gestores de paquetes | **PowerShell** |
| Ejecutar comandos de Django (`manage.py ...`) | ❌ **No** | **PowerShell** (con venv activo) |
| Ejecutar comandos de Node (`npm run ...`) | ❌ **No** | **PowerShell** |
| Renderizar diagramas `.puml` | ✅ Sí (extensión PlantUML) | **VSCode** o CLI |

**Recomendación práctica para el laboratorio:**

1. Mantenga **una terminal de PowerShell abierta** durante toda la práctica, con el venv activado (en `backend/`) o sin activar (en `frontend/`).
2. Use **VSCode** para crear/editar todos los archivos (arrastre la carpeta del proyecto a VSCode para tener un árbol lateral de archivos).
3. Use el **Explorador de Windows** solo si necesita mover, renombrar o eliminar varios archivos a la vez.

> En las secciones siguientes, los comandos PowerShell van acompañados de su **ruta de archivo** (`📄 ruta/archivo.py`) para que pueda decidir si los ejecuta en la terminal, los crea en VSCode, o una combinación de ambos.

---

## 4. Arquitectura objetivo

```
+--------------------------+        HTTP/JSON (JWT)        +--------------------------+         SQL        +---------------------+
|  Navegador (Cliente)     |  <--------------------------> |  Servidor (Django)       |  <------------->  |  PostgreSQL o MySQL |
|  React + TypeScript      |     /api/v1/auth/...          |  Django REST Framework   |                  |                     |
|  Vite (dev) / Nginx (prod)|    /api/v1/notes/...         |  + SimpleJWT             |                  |                     |
+--------------------------+                                +--------------------------+                  +---------------------+
```

**Capas (de afuera hacia adentro):**

1. **Presentación** — `views.py` / `viewsets.py` (DRF) y componentes React.
2. **Aplicación** — serializadores y servicios (lógica de negocio).
3. **Dominio** — `models.py` (entidades del problema).
4. **Infraestructura** — ORM, drivers de BD, configuración.

Los diagramas UML de referencia se generan en la **Parte 3 (Fase 10)**.

---

## 5. Fase 0 — Preparación del entorno

### 5.1 Abrir la carpeta del proyecto

**Opción A — PowerShell (recomendado):**

```powershell
$root = "D:\UNEMI\2026\PERIODO-ABRIL-JUNIO\POO\POO-4TO-CURSO-DJANGO-POSTGRES-REACT"
Set-Location $root
Get-ChildItem -Force | Select-Object Name, Mode
```

**Opción B — Manual con el Explorador de Windows:**

1. Abra el Explorador de Windows.
2. Navegue a `D:\UNEMI\2026\PERIODO-ABRIL-JUNIO\POO\POO-4TO-CURSO-DJANGO-POSTGRES-REACT`.
3. Confirme visualmente que existen `.git/` (oculta), `.gitignore` y `README.md`.

> **Debería ver:**
>
> ```
> .git        (carpeta oculta)
> .gitignore
> README.md
> ```

### 5.2 Crear la estructura de carpetas

**Opción A — PowerShell (recomendado, una sola línea crea las cinco):**

```powershell
New-Item -ItemType Directory -Path backend, frontend, docs, docs\uml, scripts -Force
```

**Opción B — Manual con el Explorador de Windows:**

1. Dentro de la carpeta del proyecto, clic derecho → *Nuevo* → *Carpeta* → nómbrela `backend`.
2. Repita para `frontend`, `docs` y `scripts`.
3. Dentro de `docs`, cree una subcarpeta llamada `uml`.

**Opción C — Híbrida (la más usada en la práctica real):** PowerShell para crear las carpetas raíz y Explorador para subcarpetas que surjan más adelante (p. ej. `apps/accounts/migrations/`).

Estructura esperada:

```
.
├── backend/         # servidor Django
├── frontend/        # cliente Vite + React
├── docs/            # documentación
│   └── uml/         # diagramas PlantUML
├── scripts/         # automatización PowerShell
├── .gitignore
└── README.md
```

### ✅ Checkpoint Fase 0

- [x] Las carpetas `backend`, `frontend`, `docs`, `docs\uml` y `scripts` existen en la raíz.

---

## 6. Fase 1 — Backend: entorno virtual y proyecto base

> **Concepto POO:** el entorno virtual encapsula un "contexto" de dependencias. Es el equivalente a un módulo cerrado que expone una API pública (`python`, `pip`) sin contaminar el sistema global.

### 6.1 Crear el entorno virtual

```powershell
Set-Location backend
py -3.12 -m venv .venv
```

Si `py -3.12` no está disponible, localice el intérprete con:

```powershell
# Muestra la ruta del Python 3.12 que se está usando
$pythonExe = (Get-Command python).Source
Write-Host "Usando: $pythonExe"

# Úselo explícitamente para crear el venv
& $pythonExe -m venv .venv
```

### 6.2 Activar el entorno

El comando de activación cambia según el shell que esté usando. Todos activan el mismo `venv`, solo varía el *script* que se ejecuta.

**Opción A — PowerShell (recomendado en Windows):**

```powershell
.\.venv\Scripts\Activate.ps1
```

> **Error frecuente:** si PowerShell muestra *"la ejecución de scripts está deshabilitada"*, ejecute **una sola vez**:
>
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
>
> Confirme con `Y` y vuelva a activar.

**Opción B — CMD (Símbolo del sistema):**

```cmd
.venv\Scripts\activate.bat
```

**Opción C — Git Bash (incluido con Git para Windows):**

```bash
source .venv/Scripts/activate
```

> En Git Bash, el separador de rutas es `/` (no `\`) y se antepone `source` porque es un shell tipo *Bourne*. Si obtiene *"No such file or directory"*, verifique que está dentro de `backend/` (`pwd` debe terminar en `/backend`).

**Opción D — WSL, Linux o macOS:**

```bash
source .venv/bin/activate
```

> Aquí la ruta es `bin/` (no `Scripts/`) porque en sistemas *nix los venv no usan el sufijo `Scripts/`.

**Verificación (común a todas las opciones):**

El prompt mostrará el prefijo `(.venv)` confirmando que está activo, y los binarios apuntarán a la ruta del venv:

```bash
# Linux/macOS/Git Bash
which python
# esperado: /.../backend/.venv/bin/python

# PowerShell
Get-Command python
# esperado: ...backend\.venv\Scripts\python.exe

# Verificación común a todos los shells
python -c "import sys; print(sys.prefix)"
# debe terminar en: ...\backend\.venv  (o .../backend/.venv)
```

> **Concepto POO:** activar un venv es el equivalente en Python de *montar* un módulo en un contenedor de dependencias: cambia el `PATH` y el `sys.prefix` de la sesión sin tocar el sistema global. El aislamiento es la **encapsulación** aplicada al entorno de ejecución.

### 6.3 Actualizar `pip`

```powershell
python -m pip install --upgrade pip
```

### 6.4 Instalar Django y crear el proyecto

```powershell
pip install "Django>=5.1,<6.0"
django-admin startproject config .
```

Verifique la estructura:

```powershell
Get-ChildItem
```

```
.venv/
config/         <- paquete del proyecto
manage.py
```

### 6.5 Verificar el servidor de desarrollo

```powershell
python manage.py migrate
python manage.py runserver
```

Abra `http://127.0.0.1:8000/` en el navegador. Debe ver la página de inicio de Django.

> **Para detener el servidor:** `Ctrl + C` en la terminal.

### ✅ Checkpoint Fase 1

- [x] Existe `backend/.venv/`.
- [x] Existe `backend/manage.py` y `backend/config/`.
- [x] El servidor arranca sin errores y muestra la página "The install worked successfully!".

---

## 7. Fase 2 — Backend: dependencias, .env y settings divididos

### 7.1 Crear `requirements.txt`

📄 **`backend/requirements.txt`**

```
Django>=5.1,<6.0
djangorestframework>=3.15,<3.16
djangorestframework-simplejwt>=5.3,<6.0
django-cors-headers>=4.4,<5.0
python-decouple>=3.8
psycopg[binary]>=3.2
mysqlclient>=2.2,<3.0
django-extensions>=3.2
```

Instale todo:

```powershell
pip install -r requirements.txt
```

### 7.2 Crear `.env.example`

📄 **`backend/.env.example`**

```ini
DJANGO_SECRET_KEY=change-me-in-production-please-use-a-long-random-string
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=config.settings.dev

DB_ENGINE=django.db.backends.postgresql
DB_NAME=poo_db
DB_USER=poo_user
DB_PASSWORD=poo_pass
DB_HOST=127.0.0.1
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

JWT_ACCESS_LIFETIME_MINUTES=60
JWT_REFRESH_LIFETIME_DAYS=7
```

Copie a `.env` (es el archivo que Django leerá):

```powershell
Copy-Item .env.example .env
```

Edite `.env` y reemplace `DJANGO_SECRET_KEY` por una cadena aleatoria de al menos 50 caracteres. Puede generarla con:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 7.3 Refactorizar `settings.py` en un paquete

Ejecute estos comandos para preparar la nueva estructura:

```powershell
# 1) Crear la carpeta config/settings/
New-Item -ItemType Directory -Path config\settings -Force

# 2) Eliminar el archivo settings.py original (será reemplazado por el paquete)
Remove-Item config\settings.py -Force

# 3) Crear los archivos vacíos (se llenan en los siguientes bloques)
New-Item -ItemType File -Path config\settings\__init__.py, config\settings\dev.py, config\settings\prod.py -Force

# 4) Crear el paquete apps/ con sus subpaquetes (vacíos por ahora —
#    las clases User y Note se añaden en la Parte 2, Fase 4).
#    Esto evita un ModuleNotFoundError al ejecutar `manage.py check`,
#    ya que base.py ya referencia `apps.accounts` y `apps.core`.
New-Item -ItemType Directory -Path apps, apps\accounts\migrations, apps\core\migrations -Force
New-Item -ItemType File -Path apps\__init__.py, apps\accounts\__init__.py, apps\accounts\migrations\__init__.py, apps\accounts\models.py, apps\core\__init__.py, apps\core\migrations\__init__.py, apps\core\models.py -Force
```

Ahora edite cada archivo con VSCode (`code config\settings\base.py`) y pegue el contenido que se muestra a continuación.

📄 **`backend/config/settings/__init__.py`** — vacío.

📄 **`backend/config/settings/base.py`**

```python
"""
Settings comunes a todos los entornos.
Los valores sensibles se leen del .env con python-decouple.
"""
from datetime import timedelta
from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_extensions",
]

LOCAL_APPS = [
    "apps.accounts",
    "apps.core",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # antes de CommonMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DB_ENGINE = config("DB_ENGINE", default="django.db.backends.postgresql")

SUPPORTED_ENGINES = {
    "django.db.backends.postgresql": ("5432", "psycopg"),
    "django.db.backends.mysql": ("3306", "mysqlclient"),
}
if DB_ENGINE not in SUPPORTED_ENGINES:
    raise ValueError(
        f"DB_ENGINE no soportado: {DB_ENGINE!r}. "
        f"Valores válidos: {list(SUPPORTED_ENGINES)}"
    )

_default_port = SUPPORTED_ENGINES[DB_ENGINE][0]

DATABASES = {
    "default": {
        "ENGINE": DB_ENGINE,
        "NAME": config("DB_NAME", default="poo_db"),
        "USER": config("DB_USER", default="poo_user"),
        "PASSWORD": config("DB_PASSWORD", default="poo_pass"),
        "HOST": config("DB_HOST", default="127.0.0.1"),
        "PORT": config("DB_PORT", default=_default_port),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-ec"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config("JWT_ACCESS_LIFETIME_MINUTES", default=60, cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config("JWT_REFRESH_LIFETIME_DAYS", default=7, cast=int)
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:5173",
    cast=Csv(),
)
CORS_ALLOW_CREDENTIALS = True
```

📄 **`backend/config/settings/dev.py`**

```python
"""Settings de desarrollo — hereda de base.py."""
from .base import *  # noqa: F401,F403

DEBUG = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

📄 **`backend/config/settings/prod.py`** *(referencia — no se usa en el laboratorio)*

> En un despliegue real, este archivo activaría HTTPS forzado, HSTS, cookies seguras y cabeceras anti-clickjacking. Ejemplo mínimo:
> ```python
> from .base import *  # noqa: F401,F403
> DEBUG = False
> SECURE_SSL_REDIRECT = True
> SESSION_COOKIE_SECURE = True
> CSRF_COOKIE_SECURE = True
> SECURE_HSTS_SECONDS = 31536000
> X_FRAME_OPTIONS = "DENY"
> ```
> Para el laboratorio basta con `dev.py` (el `.env` ya apunta a `config.settings.dev`).

### 7.4 Verificar

```powershell
# Debe estar en backend/ con el venv activo
.\.venv\Scripts\Activate.ps1
python manage.py check
```

Salida esperada: `System check identified no issues (0 silenced).`

> Por ahora verá un error `auth.E004: AUTH_USER_MODEL refers to model 'accounts.User' that has not been installed`. Es **normal**: la clase `User` se crea en la **Parte 2 (Fase 4)**.

### ✅ Checkpoint Fase 2

- [x] Existe `backend/config/settings/{__init__,base,dev,prod}.py`.
- [x] `requirements.txt` contiene todas las dependencias.
- [x] `.env` existe y `manage.py check` no tiene errores de configuración.

---

## 8. Fase 3 — Backend: base de datos (PostgreSQL o MySQL)

> **Concepto POO:** el código de negocio (`models.py`) no debe conocer el motor concreto. El módulo `DATABASES` actúa como **abstracción** (interfaz) — el principio de **Inversión de Dependencias** se aplica mediante la variable `DB_ENGINE`.

Elija **una** de las dos rutas:

### Ruta A — PostgreSQL

Conéctese como superusuario (`psql -U postgres` o pgAdmin) y ejecute:

```sql
CREATE USER poo_user WITH PASSWORD 'poo_pass';
CREATE DATABASE poo_db OWNER poo_user ENCODING 'UTF8';

-- En PostgreSQL 15+ el esquema 'public' ya no es propiedad del rol,
-- por lo que Django no puede crear tablas ahí sin este GRANT extra:
\c poo_db
GRANT ALL ON SCHEMA public TO poo_user;
```

En `.env`:

```ini
DB_ENGINE=django.db.backends.postgresql
DB_PORT=5432
```

### Ruta B — MySQL / MariaDB

```sql
CREATE DATABASE poo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'poo_user'@'localhost' IDENTIFIED BY 'poo_pass';
GRANT ALL PRIVILEGES ON poo_db.* TO 'poo_user'@'localhost';
FLUSH PRIVILEGES;
```

En `.env`:

```ini
DB_ENGINE=django.db.backends.mysql
DB_PORT=3306
```

### Verificar la conexión

```powershell
python manage.py check
```

Si la conexión es correcta, no se reportan errores de base de datos.

### ✅ Checkpoint Fase 3

- [x] El usuario y la base de datos existen en el motor elegido.
- [x] `python manage.py check` no reporta errores de configuración de BD.

---

## Cierre de la Parte 1

Ha completado la configuración base:

- [x] Entorno virtual creado y activado.
- [x] Dependencias instaladas.
- [x] Proyecto Django arrancando en `http://127.0.0.1:8000/`.
- [x] Settings divididos (`base` / `dev` / `prod`) con variables de entorno.
- [x] Base de datos PostgreSQL o MySQL creada y conectada.

**Siguiente paso:** ➡️ [Parte 2 — Backend Django (apps, modelos, API, JWT)](./guia-laboratorio-02.md)

En la Parte 2 creará las apps `accounts` y `core`, definirá los modelos y expondrá el API REST con autenticación JWT.
