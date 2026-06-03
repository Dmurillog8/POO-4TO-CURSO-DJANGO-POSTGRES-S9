# POO-4TO-CURSO-DJANGO-POSTGRES-REACT

Laboratorio de **Programación Orientada a Objetos (4to curso)** — aplicación cliente/servidor full-stack con Django + React.

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Django 5 · Django REST Framework · SimpleJWT · django-cors-headers |
| Frontend | Vite · React 18 · TypeScript · React Router 6 · Axios |
| Base de datos | PostgreSQL 14+ **o** MySQL 8 / MariaDB 10 (seleccionable por `.env`) |
| Lenguajes | Python 3.12 · Node.js 20 LTS |
| Documentación | PlantUML (diagramas UML) |

## Estructura del repositorio

```
.
├── backend/         # servidor Django (se crea durante la práctica)
├── frontend/        # cliente Vite + React (se crea durante la práctica)
├── docs/
│   ├── guia-laboratorio-01.md
│   ├── guia-laboratorio-02.md
│   ├── guia-laboratorio-03.md
│   └── uml/         # diagramas PlantUML (Fase 10)
└── scripts/         # automatización opcional
```

## Guía de laboratorio

La práctica se divide en **3 guías** que se siguen **en orden**. Cada guía termina con un *checkpoint* que el estudiante debe verificar antes de pasar a la siguiente.

| # | Guía | Fases | Resultado al finalizar |
|---|---|---|---|
| [01](./docs/guia-laboratorio-01.md) | **Configuración base y proyecto Django** | 0 → 3 | Proyecto Django arrancando con BD conectada |
| [02](./docs/guia-laboratorio-02.md) | **Backend Django (apps, modelos, API, JWT)** | 4 → 5 | API REST con JWT funcional |
| [03](./docs/guia-laboratorio-03.md) | **Frontend React + UML + Verificación** | 7 → 10 + checklist | Sistema cliente/servidor completo + diagramas |

> **Recomendación:** complete la 01, verifique el checkpoint, y solo entonces pase a la 02. Cada guía referencia explícitamente la anterior y la siguiente.

## Documentación adicional

- [Referencia del Framework Django — MVT, componentes y arquitectura](./docs/referencias-django.md)
  Companion teórico de las 3 guías. Explica Django MVT, ORM, Views, DRF, Middleware, Settings y el mapeo a principios POO. Léalo **antes** de la práctica para tener el mapa mental completo.

## Requisitos

- Windows 10/11 con PowerShell 5.1+
- Python 3.12 (`python --version`)
- Node.js 20 LTS (`node --version`)
- PostgreSQL 14+ **o** MySQL 8 / MariaDB 10
- Git, Visual Studio Code (extensiones: *Python*, *Pylance*, *ESLint*, *PlantUML*)

> ¿Falta alguna herramienta? La **Fase 0 / Sección 2.1** de la guía 01 incluye los comandos `winget` para instalar todo lo necesario en Windows.

## Inicio rápido

1. Clone o descargue este repositorio en `D:\UNEMI\2026\PERIODO-ABRIL-JUNIO\POO\POO-4TO-CURSO-DJANGO-POSTGRES-REACT`.
2. Abra la [Guía 01](./docs/guia-laboratorio-01.md) y siga las fases 0 a 3.
3. Continúe con la [Guía 02](./docs/guia-laboratorio-02.md) (fases 4 y 5).
4. Termine con la [Guía 03](./docs/guia-laboratorio-03.md) (fases 7 a 10 + verificación final).
