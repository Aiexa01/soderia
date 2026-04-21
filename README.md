# 🚰 Soda y Agua Tres Cerritos — Sistema de Gestión

Sistema integral de gestión para la distribución de soda y agua, desarrollado con Django 3.2 y MySQL, dockerizado para un despliegue rápido y sencillo.

Este sistema combina un entorno público (Landing Page) para la captación de clientes con un potente ERP interno optimizado para operaciones en tiempo real, control de flotas y seguimiento logístico y financiero.

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
- [Scripts de Carga de Datos](#-carga-de-datos-iniciales)
- [Acceso al Sistema](#-acceso-al-sistema)
- [Notas Adicionales](#-notas-adicionales)

---

## 📝 Descripción
Sistema web para la empresa **Soda y Agua Tres Cerritos** de Salta Capital, Argentina. Permite gestionar:

- **Clientes** (personas y comercios) con validación inteligente anti-duplicados (DNI, Email, Teléfono).
- **Consultas web:** captación de potenciales clientes desde la landing page.
- **Pedidos y ventas** con estados operativos trazables (Creado → Asignado → Despachado → En Reparto → Entregado → Pagado).
- **Logística y reparto (Hoja de Ruta)** con seguimiento unívoco por despacho y métricas financieras (Cobrado vs Pendiente).
- **Productos** (sifones, bidones, dispensers).
- **Stock** por camioneta y depósito centralizado.
- **Usuarios** con roles diferenciados y permisos estrictos.
- **Zonas y barrios** de cobertura.

---

## 🛠 Tecnologías

| Componente | Tecnología |
|---|---|
| **Backend** | Python 3.9.5 / Django 3.2.2 |
| **Base de Datos** | MySQL 5.7+ |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla + jQuery/Select2) |
| **Tipografía** | Google Fonts (Inter) |
| **Infraestructura** | Docker / Docker Compose |
| **Reportes** | ReportLab (PDF), Matplotlib |
| **Otros** | QR Code, Pillow |

---

## ✅ Requisitos Previos

Antes de comenzar, asegurate de tener instalado:

1. **Docker Desktop** — [Descargar](https://www.docker.com/)
2. **MySQL Server** — Corriendo en tu máquina local (puerto 3306)
3. **Git (opcional)** — Para clonar el repositorio

### Base de Datos
El sistema espera una base de datos MySQL llamada `soderia`. Creala manualmente antes de iniciar el contenedor:

```sql
CREATE DATABASE IF NOT EXISTS soderia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

_Si tenés el archivo de respaldo, podés restaurarlo:_
```bash
mysql -u root -p soderia < soderia_backup.sql
```

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar el repositorio
```bash
git clone https://github.com/Aiexa01/soderia.git
cd soderia
```

### 2. Levantar el contenedor Docker
Esto crea un contenedor llamado `soderia` con Python 3.9.5 y mapea el puerto 8004 (local) → 8000 (contenedor).
```bash
docker compose up -d
```

### 3. Entrar al contenedor
```bash
docker exec -it soderia bash
```

### 4. Instalar dependencias (Dentro del contenedor)
```bash
cd /opt/back_end
pip install -r requirements.txt
```

### 5. Ejecutar migraciones
```bash
cd /opt/back_end/mi_proyecto
python manage.py migrate
```

### 6. Crear superusuario (Primera vez)
```bash
python manage.py createsuperuser
```

### 7. Acceder al sistema
Abre el navegador en `http://localhost:8004/`

---

## 📦 Módulos del Sistema

### 🌐 Landing Page Pública (`/`)
Página institucional optimizada con información de la empresa, productos, valores y datos en vivo:
- Estadísticas automáticas (años, clientes activos, vehículos).
- Formulario de contacto integrado (`POST /api/contacto/`).
- Botón flotante de WhatsApp.

### 🏠 Home / Dashboard (`/home/`)
Panel principal con accesos rápidos según el rol del usuario, y notificaciones de nuevas Consultas Web en tiempo real.

### 📩 Consultas Web (`/consultas/`)
Módulo CRM para gestionar prospectos derivados del contacto público:
- Trazabilidad y flujo de estados: _Nueva → Leída → Contactada → Convertida / Descartada_.
- **Convertir a Cliente:** Pase directo con auto-completado de formulario.
- Separación estricta de la base de clientes reales.

### 👥 Gestión de Clientes (`/clientes/`)
- Alta de Personas o Comercios.
- Control estricto anti-duplicados por ID fiscal, celular o email.
- Relación geográfica (Zona y Barrio).

### 🛒 Gestión de Pedidos (`/ventas/`)
Flujo altamente controlado para pedidos:
- **Estados Operativos:** _Creado → Asignado → Despachado → En Reparto → Entregado → Pagado_.
- Bloqueos de seguridad server-side para evitar alterar un pedido finalizado o cancelado.
- Seguimiento de saldos adeudados.

### 🚚 Logística y Hoja de Ruta (`/logistica/`)
- Monitor visual de Camionetas con contadores de rendimiento en vivo.
- **Hoja de Ruta por Despacho:** Agrupación unívoca para trazabilidad sin fallos.
- **Métricas Financieras en Vivo:** Distinción clara entre **Cobrado** (Pedidos Pagados) y **Pendiente de Cobro** (Pedidos Entregados).
- Cambio rápido de estados (ej. marcar devolución) con registro de auditoría automática (`_audit`).

### 📦 Stock (`/stock/`)
- **Depósito Central:** Indicadores de estado visuales (OK, Bajo, Crítico).
- Movimientos internos, cargas a depósito y transferencias directas a vehículos.
- **Descuento automático:** El stock de la camioneta se descuenta solo cuando el pedido es `Entregado` o `Pagado`.
- Trazabilidad total de movimientos de mercadería por fecha y usuario.

### 🚛 Gestión de Camionetas (`/admin-panel/camionetas/`)
Alta de flotas, control de patentes, asignación de chofer responsable y zonas asiduas de reparto.

### 📋 Gestión de Productos (`/admin-panel/productos/`)
Control de catálogo: precio, si es retornable o descartable, medida de volumen (Pack, Bidón, Sifón).

### 👤 Usuarios y Seguridad (`/admin-panel/usuarios/`)
Asignación de credenciales limitadas por el esquema de roles de Django (Grupos).

---

## 🔐 Roles de Usuario

| Rol | Código | Acceso |
|---|---|---|
| **Administrador** | ADM | Acceso total: usuarios, productos, camionetas, logística, auditorías |
| **Encargado de Atención** | EAC | Gestión de clientes, CRM de consultas, pedidos y ventas |
| **Encargado de Stock** | EST | Gestión de stock, transferencias y trazabilidad de depósito |
| **Técnico** | TEC | Reparaciones y mantenimientos (Service) |
| **Repartidor** | REP | Interfaz móvil simplificada: mis entregas, mi stock, operar cierres |

---

## ⚙ Variables de Entorno
Definidas en `docker-compose.yml`:

| Variable | Valor por defecto | Descripción |
|---|---|---|
| `DB_NAME` | soderia | Nombre de la base de datos |
| `DB_USER` | root | Usuario de MySQL |
| `DB_PASSWORD` | admin | Contraseña de MySQL |
| `DB_HOST` | host.docker.internal | Host de la base de datos (conecta al host local) |
| `DB_PORT` | 3306 | Puerto de MySQL |

---

## 📊 Carga de Datos Iniciales (Seed)

Para poblar el sistema rápidamente con usuarios, productos, zonas y pedidos demo, ejecuta dentro del contenedor bash:

```bash
cd /opt/back_end/mi_proyecto
python ../scripts/seed_all.py
```
_Nota: El script es idempotente (no duplica si lo corres dos veces)._

### 🔑 Credenciales de Demo Generadas
| Usuario | Contraseña | Rol |
|---|---|---|
| marlene / admin | admin123 | Administrador |
| carolina | carolina123 | Encarg. Atención al Cliente |
| jorge | jorge123 | Encarg. de Stock |
| mario / ricardo | *[nombre]123* | Repartidor |

*(Existen más scripts granulares en la carpeta `/scripts/` si se desea popular información por pieza).*

---

## 🔗 Acceso Rápido al Sistema

| Sección | URL |
|---|---|
| Landing | `http://localhost:8004/` |
| Home ERP | `http://localhost:8004/home/` |
| Consultas CRM | `http://localhost:8004/consultas/` |
| Logística | `http://localhost:8004/logistica/` |
| Stock Central | `http://localhost:8004/stock/` |

---

## 📌 Notas Adicionales
- Funciona sobre la versión de largo soporte (LTS) **Django 3.2**.
- Todos los assets (imágenes, CSS) se sirven convencionalmente para entornos sin Cloud Storages (`DEBUG=True` para desarrollo rápido).
- Timezone configurado en `America/Argentina/Buenos_Aires` (fundamental para los cierres diarios de reparto).
- Se cuenta con prevención activa contra vulnerabilidades (Protección CSRF, restricciones server-side contra manipulación de POST/URL).

---

### 🏢 Información de la Empresa
**Soda y Agua Tres Cerritos**  
📍 Las Heras 1443, Salta Capital  
☎️ 4393920 | 📱 +54 9 387 439-3920  
Desarrollado y mantenido por **Nodo Dev** · © 2026.
