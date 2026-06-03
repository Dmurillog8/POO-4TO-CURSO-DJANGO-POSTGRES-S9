# Guía de Laboratorio 02 — Backend Django (apps, modelos, API, JWT)

> **Parte 2 de 3** · ⏱ Duración estimada: **1 – 1.5 horas**
> **Asignatura:** Programación Orientada a Objetos (4to curso)
> **Prerrequisito:** haber completado la [Parte 1 — Configuración base](./guia-laboratorio-01.md) y tener el servidor Django arrancando con la base de datos conectada.
> **Alcance de esta parte:** crear las apps `accounts` y `core`, modelar entidades y exponer el API REST con autenticación JWT (CORS ya quedó configurado en la Parte 1).

| ⬅️ Anterior | 📘 Esta guía | ➡️ Siguiente |
|---|---|---|
| [01 — Configuración base](./guia-laboratorio-01.md) | **02** Backend Django | [03 — Frontend React + UML](./guia-laboratorio-03.md) |

---

## Tabla de contenido

9. [Fase 4 — Backend: apps `accounts` y `core` (modelos y admin)](#9-fase-4--backend-apps-accounts-y-core-modelos-y-admin)
10. [Fase 5 — Backend: API REST + autenticación JWT](#10-fase-5--backend-api-rest--autenticación-jwt)

> **Punto de control al final de esta guía:** el backend responde a `register`, `token`, `me` y `notes` con JWT, y está listo para ser consumido por el cliente React en la **Parte 3**.

---

## 9. Fase 4 — Backend: apps `accounts` y `core` (modelos y admin)

> **Concepto POO:** cada app Django es un **paquete cohesivo** que agrupa modelos, vistas y serializadores de un único bounded context. SRP en acción.

### Antes de empezar

Asegúrese de estar en `backend/` con el entorno virtual activo (si cerró la terminal tras la Parte 1):

```powershell
Set-Location backend
.\.venv\Scripts\Activate.ps1
python --version    # debe mostrar 3.12.x
```

### 9.1 Crear la carpeta `apps/` y los paquetes

```powershell
# Estructura de carpetas
New-Item -ItemType Directory -Path apps, apps\accounts\migrations, apps\core\migrations -Force

# Archivos __init__.py (marcadores de paquete Python)
New-Item -ItemType File -Path apps\__init__.py -Force
New-Item -ItemType File -Path apps\accounts\__init__.py, apps\accounts\migrations\__init__.py, apps\accounts\apps.py, apps\accounts\models.py, apps\accounts\admin.py, apps\accounts\serializers.py, apps\accounts\views.py, apps\accounts\urls.py -Force
New-Item -ItemType File -Path apps\core\__init__.py, apps\core\migrations\__init__.py, apps\core\apps.py, apps\core\models.py, apps\core\admin.py, apps\core\serializers.py, apps\core\views.py, apps\core\urls.py -Force
```

Todos los `__init__.py` quedan vacíos. El contenido de los demás archivos se pega en los siguientes pasos.

### 9.2 Registrar las apps en `INSTALLED_APPS`

Las apps `apps.accounts` y `apps.core` ya están registradas en `base.py` (Parte 1, Fase 2). Si omitió esa parte, añádalas a `LOCAL_APPS` en `config/settings/base.py`.

### 9.3 Modelo `User` personalizado

📄 **`backend/apps/accounts/apps.py`**

```python
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "Cuentas de usuario"
```

📄 **`backend/apps/accounts/models.py`**

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField("correo electrónico", unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ("-date_joined",)

    def __str__(self) -> str:
        return self.username
```

### 9.4 Modelo `Note` (app demo)

📄 **`backend/apps/core/apps.py`**

```python
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Núcleo (app demo)"
```

📄 **`backend/apps/core/models.py`**

```python
from django.conf import settings
from django.db import models


class Note(models.Model):
    """Nota personal asociada a un usuario."""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "nota"
        verbose_name_plural = "notas"

    def __str__(self) -> str:
        return f"{self.title} ({self.owner_id})"
```

### 9.5 Registrar en el admin

📄 **`backend/apps/accounts/admin.py`**

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Metadatos", {"fields": ("created_at",)}),
    )
    readonly_fields = ("created_at", "last_login", "date_joined")
```

📄 **`backend/apps/core/admin.py`**

```python
from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "created_at")
    list_filter = ("owner",)
    search_fields = ("title", "body", "owner__username")
    readonly_fields = ("created_at", "updated_at")
```

### 9.6 Generar migraciones

```powershell
python manage.py makemigrations
python manage.py migrate
```

Salida esperada: migración inicial para `accounts` y `core`.

### 9.7 Crear superusuario

```powershell
python manage.py createsuperuser
```

Django le pedirá, en este orden:

```
Username: admin
Email address: admin@example.com
Password: ********          # la contraseña no se muestra al teclear
Password (again): ********
Superuser created successfully.
```

### 9.8 Verificar el admin

```powershell
python manage.py runserver
```

Abra `http://127.0.0.1:8000/admin/` e ingrese con el superusuario. Debe ver los modelos **Usuarios** y **Notas**.

### ✅ Checkpoint Fase 4

- [x] Migraciones aplicadas sin errores.
- [x] Admin accesible y muestra las dos apps.
- [x] Puede crear un usuario y una nota desde el admin.

---

## 10. Fase 5 — Backend: API REST + autenticación JWT

> **Concepto POO:** el *serializer* es un **adaptador** entre el modelo (representación interna) y la representación JSON (interfaz pública del API). Es una **fachada** que también valida datos de entrada.

### 10.1 Serializers de `accounts`

📄 **`backend/apps/accounts/serializers.py`**

```python
"""Serializers para registro y representación del usuario."""
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "created_at")
        read_only_fields = ("id", "created_at")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirm",
                  "first_name", "last_name")

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Las contraseñas no coinciden."}
            )
        return attrs

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        return value

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
```

### 10.2 Vistas de `accounts`

📄 **`backend/apps/accounts/views.py`**

```python
"""Vistas: registro y datos del usuario autenticado."""
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """POST /api/v1/auth/register/ — crea un usuario nuevo."""
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)


class MeView(APIView):
    """GET /api/v1/auth/me/ — datos del usuario autenticado."""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
```

📄 **`backend/apps/accounts/urls.py`**

```python
"""URLs de la app accounts."""
from django.urls import path

from .views import MeView, RegisterView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
]
```

### 10.3 Serializers y ViewSet de `core`

📄 **`backend/apps/core/serializers.py`**

```python
"""Serializers de Note."""
from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Note
        fields = ("id", "title", "body", "owner", "created_at", "updated_at")
        read_only_fields = ("id", "owner", "created_at", "updated_at")
```

📄 **`backend/apps/core/views.py`**

```python
"""ViewSet de Note: CRUD restringido al usuario autenticado."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Note
from .serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

📄 **`backend/apps/core/urls.py`**

```python
"""URLs de la app core."""
from rest_framework.routers import DefaultRouter

from .views import NoteViewSet

app_name = "core"

router = DefaultRouter()
router.register(r"notes", NoteViewSet, basename="note")

urlpatterns = router.urls
```

### 10.4 Enrutamiento principal

> **Reemplace todo el contenido** del archivo `config/urls.py` (Django genera uno mínimo en `startproject`; lo sustituimos por el enrutamiento API + JWT).

📄 **`backend/config/urls.py`**

```python
"""URL routing principal del proyecto."""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

api_v1_patterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/", include("apps.accounts.urls")),
    path("", include("apps.core.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include((api_v1_patterns, "api"), namespace="v1")),
]
```

### 10.5 Probar la API con curl

> **Importante para Windows/PowerShell:** el alias `curl` de PowerShell apunta a `Invoke-WebRequest`, no al binario `curl.exe`. Si escribe `curl -X POST ...` obtendrá errores. Use siempre `curl.exe` (incluido en `C:\Windows\System32\` desde Windows 10 1803).
>
> Antes de empezar confirme que el **servidor Django está corriendo** en otra terminal: `python manage.py runserver`. Los comandos de esta sección envían peticiones HTTP al servidor, no a la base de datos directamente.

**Paso 1 — Registrar un usuario:**

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/v1/auth/register/ `
     -H "Content-Type: application/json" `
     -d '{"username":"ada","email":"ada@example.com","password":"Strong-Pass-123","password_confirm":"Strong-Pass-123"}'
```

**Paso 2 — Obtener tokens (login) y guardarlos en variables de PowerShell** (así se evita copiar/pegar el token a mano):

```powershell
$login = curl.exe -s -X POST http://127.0.0.1:8000/api/v1/auth/token/ `
     -H "Content-Type: application/json" `
     -d '{"username":"ada","password":"Strong-Pass-123"}' | ConvertFrom-Json

$access = $login.access
$refresh = $login.refresh
Write-Host "access token (primeros 20 chars): $($access.Substring(0,20))..."
```

**Paso 3 — Acceder a `/me/` con el token:**

```powershell
curl.exe http://127.0.0.1:8000/api/v1/auth/me/ -H "Authorization: Bearer $access"
```

**Paso 4 — Crear una nota:**

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/v1/notes/ `
     -H "Authorization: Bearer $access" `
     -H "Content-Type: application/json" `
     -d '{"title":"Hola","body":"Mi primera nota"}'
```

**Paso 5 — Listar notas:**

```powershell
curl.exe http://127.0.0.1:8000/api/v1/notes/ -H "Authorization: Bearer $access"
```

### ✅ Checkpoint Fase 5

- [x] `register`, `token`, `me` y `notes` responden según la tabla de endpoints.
- [x] `GET /notes/` sin token retorna **401**.
- [x] `POST /notes/` con token crea una nota y el `owner` es el usuario autenticado.
- [x] CORS configurado: `CORS_ALLOWED_ORIGINS` en `.env` incluye `http://localhost:5173` (ya está en el `.env.example` de la Parte 1; reinicie el servidor si lo modifica).

> **Concepto POO:** CORS es una **política de seguridad** del navegador. El servidor debe declarar explícitamente qué orígenes externos pueden consumir sus recursos (Principio de Mínimo Privilegio). El middleware `corsheaders` ya quedó instalado y configurado en `base.py` durante la Parte 1.

---

## Cierre de la Parte 2

Ha completado la implementación del backend:

- [x] Apps `accounts` y `core` creadas, con modelos registrados en el admin.
- [x] API REST con autenticación JWT funcionando en `/api/v1/`.
- [x] CORS configurado para permitir el origen del frontend React.

**Siguiente paso:** ➡️ [Parte 3 — Frontend React + UML + Verificación](./guia-laboratorio-03.md)

En la Parte 3 creará el cliente con Vite + React + TypeScript, implementará la autenticación contra el API, construirá un dashboard que consuma las notas, y generará los diagramas UML de la arquitectura.
