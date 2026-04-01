# 🚰 Soda y Agua Tres Cerritos — Sistema de Gestión

Sistema integral de gestión para la distribución de soda y agua, desarrollado con **Django 3.2** y **MySQL**, dockerizado para un despliegue rápido y sencillo.

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Módulos del Sistema](#-módulos-del-sistema)
- [Roles de Usuario](#-roles-de-usuario)
- [Variables de Entorno](#-variables-de-entorno)
- [Scripts de Carga de Datos](#-scripts-de-carga-de-datos)
- [Acceso al Sistema](#-acceso-al-sistema)
- [Notas Adicionales](#-notas-adicionales)

---

## 📝 Descripción

Sistema web para la empresa **Soda y Agua Tres Cerritos** de Salta Capital, Argentina. Permite gestionar:

- Clientes (personas y comercios)
- Pedidos y ventas
- Productos (sifones, bidones, dispensers)
- Logística y reparto con camionetas
- Stock por camioneta y depósito
- Usuarios con roles diferenciados
- Zonas y barrios de cobertura
- Landing page pública con información de la empresa

---

## 🛠 Tecnologías

| Componente       | Tecnología                  |
|------------------|-----------------------------|
| **Backend**      | Python 3.9.5 / Django 3.2.2 |
| **Base de Datos** | MySQL 5.7+                  |
| **Frontend**     | HTML5, CSS3, JavaScript     |
| **Tipografía**   | Google Fonts (Inter)        |
| **Contenedor**   | Docker / Docker Compose     |
| **Reportes**     | ReportLab (PDF), Matplotlib |
| **Otros**        | QR Code, Pillow             |

---

## ✅ Requisitos Previos

Antes de comenzar, asegurate de tener instalado:

1. **Docker Desktop** — [Descargar](https://www.docker.com/products/docker-desktop/)
2. **MySQL Server** — Corriendo en tu máquina local (puerto `3306`)
3. **Git** (opcional) — Para clonar el repositorio

### Base de Datos

El sistema espera una base de datos MySQL llamada `soderia`. Creala manualmente antes de iniciar:

```sql
CREATE DATABASE IF NOT EXISTS soderia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Si tenés el archivo de respaldo, podés restaurarlo:

```bash
mysql -u root -p soderia < soderia_backup.sql
```

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd soderia
```

### 2. Levantar el contenedor Docker

```bash
docker compose up -d
```

Esto crea un contenedor llamado `soderia` con Python 3.9.5 y mapea el puerto **8004** (local) → **8000** (contenedor).

### 3. Entrar al contenedor

```bash
docker exec -it soderia bash
```

### 4. Instalar dependencias

Dentro del contenedor:

```bash
cd /opt/back_end
pip install -r requirements.txt
```

### 5. Ejecutar migraciones

```bash
cd /opt/back_end/mi_proyecto
python manage.py migrate
```

### 6. Crear superusuario (primera vez)

```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

### 8. Acceder al sistema

Abrir el navegador en:

| Página            | URL                                  |
|-------------------|--------------------------------------|
| **Landing Page**  | http://localhost:8004/               |
| **Iniciar Sesión**| http://localhost:8004/login/         |
| **Panel Home**    | http://localhost:8004/home/          |
| **Django Admin**  | http://localhost:8004/admin/         |

---

## 📁 Estructura del Proyecto

```
soderia/
├── docker-compose.yml          # Configuración de Docker
├── requirements.txt            # Dependencias Python
├── soderia_backup.sql          # Backup de la base de datos
├── barrios.txt                 # Datos de barrios para importación
├── scripts/                    # Scripts de carga de datos
│   ├── load_barrios.py
│   ├── load_sample_clients_salta.py
│   ├── load_sample_products.py
│   ├── load_sample_camionetas.py
│   ├── update_barrios_zonas.py
│   ├── assign_barrio_ref_from_text.py
│   └── update_clients_from_barrio_ref.py
│
└── mi_proyecto/                # Proyecto Django
    ├── manage.py
    ├── mi_proyecto/            # Configuración Django
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    │
    └── Proyecto_Soderia/       # App principal
        ├── models.py           # Modelos de datos
        ├── views.py            # Vistas (lógica de negocio)
        ├── urls.py             # Rutas de la aplicación
        ├── admin.py
        ├── templates/          # Plantillas HTML
        │   ├── landing.html        # Página pública
        │   ├── base.html           # Layout base del sistema
        │   ├── home.html           # Dashboard principal
        │   ├── registration/       # Login
        │   ├── clients_*.html      # CRUD de clientes
        │   ├── orders_*.html       # Gestión de pedidos
        │   ├── productos_*.html    # Gestión de productos
        │   ├── camionetas_*.html   # Gestión de camionetas
        │   ├── barrios_*.html      # Gestión de barrios
        │   ├── stock_*.html        # Control de stock
        │   ├── logistica_panel.html # Panel de logística
        │   ├── mis_entregas.html   # Vista del repartidor
        │   ├── mi_stock.html       # Stock del repartidor
        │   ├── mi_camioneta.html   # Camioneta asignada
        │   └── admin_users*.html   # Gestión de usuarios
        │
        └── static/             # Archivos estáticos
            ├── css/
            │   ├── styles.css      # Estilos del sistema interno
            │   ├── landing.css     # Estilos de la landing page
            │   └── logistica.css   # Estilos de logística
            └── images/             # Imágenes de la empresa
```

---

## 📦 Módulos del Sistema

### 🌐 Landing Page Pública (`/`)
Página institucional con información de la empresa, productos, valores, contacto y redes sociales.

### 🏠 Home / Dashboard (`/home/`)
Panel principal con accesos rápidos según el rol del usuario.

### 👥 Gestión de Clientes (`/clientes/`)
- Listado con búsqueda y filtros
- Alta, edición y baja de clientes
- Tipos: Persona / Comercio
- Asignación de zona y barrio

### 🛒 Gestión de Pedidos (`/ventas/`)
- Creación de pedidos con detalle de productos
- Flujo de estados: Creado → Asignado → En Reparto → Entregado → Pagado
- Asignación a camioneta
- Registro de pagos (efectivo, transferencia, tarjeta, Mercado Pago)

### 🚚 Logística (`/logistica/`)
- Panel de control de repartos
- Asignación de pedidos a camionetas
- Seguimiento en tiempo real del estado de entregas

### 📦 Stock (`/stock/`)
- Stock general por camioneta
- Carga de productos a camionetas
- Movimientos de stock (entrega, devolución, ajuste)
- Stock por depósito

### 🚛 Gestión de Camionetas (`/admin-panel/camionetas/`)
- Alta, edición y baja de camionetas
- Asignación de repartidor
- Asignación de zonas de reparto
- Estados: Disponible / En Ruta / Fuera de Servicio

### 📋 Gestión de Productos (`/admin-panel/productos/`)
- CRUD completo de productos
- Tipos de envase: Botella, Sifón, Bidón
- Control de retornables y depósitos de envase
- Unidades de venta: Unidad, Pack, Caja

### 🗺 Zonas y Barrios (`/admin-panel/barrios/`)
- Organización geográfica por zonas
- Barrios dentro de cada zona
- Asignación a clientes y camionetas

### 👤 Gestión de Usuarios (`/admin-panel/usuarios/`)
- Alta, edición y gestión de usuarios
- Asignación de roles/grupos
- Estados: Habilitado / Suspendido / Baja
- Cambio de contraseña
- Listado de usuarios dados de baja con opción de reactivar

---

## 🔐 Roles de Usuario

El sistema utiliza **grupos de Django** para gestionar permisos:

| Rol              | Acceso                                                    |
|------------------|-----------------------------------------------------------|
| **Administrador** | Acceso total: usuarios, productos, camionetas, barrios, pedidos, stock |
| **Operador**     | Gestión de clientes, pedidos, stock y logística            |
| **Repartidor**   | Mis entregas, mi stock, mi camioneta                      |

---

## ⚙ Variables de Entorno

Definidas en `docker-compose.yml`:

| Variable       | Valor por defecto       | Descripción                         |
|----------------|-------------------------|-------------------------------------|
| `DB_NAME`      | `soderia`               | Nombre de la base de datos          |
| `DB_USER`      | `root`                  | Usuario de MySQL                    |
| `DB_PASSWORD`  | `admin`                 | Contraseña de MySQL                 |
| `DB_HOST`      | `host.docker.internal`  | Host de la base de datos            |
| `DB_PORT`      | `3306`                  | Puerto de MySQL                     |

> **Nota:** `host.docker.internal` permite al contenedor Docker conectarse al MySQL instalado en tu máquina local (Windows/Mac). En Linux, usá la IP de tu máquina o configurá la red de Docker.

---

## 📊 Scripts de Carga de Datos

Ejecutar dentro del contenedor (`docker exec -it soderia bash`):

```bash
cd /opt/back_end/mi_proyecto
```

| Script                              | Descripción                                      |
|-------------------------------------|--------------------------------------------------|
| `python ../scripts/load_barrios.py` | Carga barrios desde `barrios.txt`                |
| `python ../scripts/load_sample_products.py` | Carga productos de ejemplo                |
| `python ../scripts/load_sample_clients_salta.py` | Carga clientes de ejemplo           |
| `python ../scripts/load_sample_camionetas.py` | Carga camionetas de ejemplo             |
| `python ../scripts/update_barrios_zonas.py` | Actualiza asignación de barrios a zonas  |
| `python seed_payment_methods.py`    | Carga métodos de pago                            |

---

## 🔗 Acceso al Sistema

### URLs Principales

| Sección          | URL                                           |
|------------------|-----------------------------------------------|
| Landing          | `http://localhost:8004/`                      |
| Login            | `http://localhost:8004/login/`                |
| Home             | `http://localhost:8004/home/`                 |
| Clientes         | `http://localhost:8004/clientes/`             |
| Ventas/Pedidos   | `http://localhost:8004/ventas/`               |
| Logística        | `http://localhost:8004/logistica/`            |
| Stock            | `http://localhost:8004/stock/`                |
| Mis Entregas     | `http://localhost:8004/mis-entregas/`         |
| Admin Usuarios   | `http://localhost:8004/admin-panel/usuarios/` |
| Admin Camionetas | `http://localhost:8004/admin-panel/camionetas/` |
| Admin Productos  | `http://localhost:8004/admin-panel/productos/`  |
| Admin Barrios    | `http://localhost:8004/admin-panel/barrios/`    |

---

## 📌 Notas Adicionales

- El sistema usa **Django 3.2 LTS** por estabilidad.
- Los archivos estáticos se sirven directamente desde Django en modo desarrollo (`DEBUG=True`).
- El puerto de acceso externo es **8004** (mapeado al 8000 interno del contenedor).
- La base de datos se gestiona de forma **externa al contenedor** (MySQL local).
- El código fuente se monta como volumen, por lo que los cambios en archivos se reflejan inmediatamente.

---

## 🏢 Información de la Empresa

| Dato         | Valor                                  |
|--------------|----------------------------------------|
| **Empresa**  | Soda y Agua Tres Cerritos              |
| **Dirección**| Las Heras 1443, Salta Capital          |
| **Teléfono** | 4393920                                |
| **WhatsApp** | +54 9 387 439-3920                     |
| **Facebook** | [sodayaguatrescerritos](https://www.facebook.com/sodayaguatrescerritos) |
| **Instagram**| [@trescerritos.srl](https://www.instagram.com/trescerritos.srl/) |

---

<p align="center">
  Desarrollado por <strong>Nodo Dev</strong> · © 2026
</p>
