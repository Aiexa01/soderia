# 📱 Documentación del Panel Móvil (Soderia PWA)

Este documento resume el progreso de la implementación de la aplicación móvil (PWA) de Soda y Agua Tres Cerritos, detallando las funcionalidades operativas actuales y el roadmap de desarrollo (lo que falta para alcanzar la madurez del producto).

---

## ✅ Lo que YA ESTÁ HECHO (Fase 1 y 2 COMPLETADAS)

Hemos desarrollado una PWA interactiva que no requiere una APK nativa, utilizando el patrón "Mobile-First". 

### 1. Núcleo PWA y Arquitectura
- **Ruteo Diferenciado:** Todos los flujos móviles operan bajo el prefijo `http://dominio.com/m/...` sin interferir con la lógica de escritorio de la oficina.
- **Service Worker (`sw.js`) y `manifest.json`:** Funcionalidad PWA preparada para que cualquier dispositivo iOS o Android lance un banner de "Añadir a Inicio" o "Instalar Aplicación".
- **Bottom Navigation Bar Dinámica:** La barra de navegación inferior detecta automáticamente el Rol del trabajador (Repartidor vs. EAC) para mostrar botones y funcionalidades estrictamente relevantes para su departamento.
- **Estándares de Interfaz Móvil (`mobile.css`):** Inputs amigables al tacto, fuentes gigantes legibles al mediodía bajo el sol y transiciones de carga entre páginas.

### 2. Flujo del Repartidor / Logística (Fase 1)
Todo lo que un chofer necesita usar arriba de la Master 1 está concluido:
- **📍 Dashboard Inteligente del Repartidor:** Muestra estado de la jornada actual (Cant. Pendientes, Completadas y Devueltas).
- **📍 Lista de Entregas Organizada:** Ordena las entregas asignadas visualmente por Barrio utilizando tarjetas expansibles interactivas.
- **🚀 Entrega Ultrarrápida (1 click):** Un botón verde exclusivo para que el chofer baje la mercadería, anote que le pagaron en la mano y todo el sistema se descuente (stock en vehículo incluido) con un solo toque y auto-refresco a la siguiente entrega.
- **⚙️ Operación Parcial:** Interfaz con "steppers" (+ y - grandes) en vez de teclados digitales en pantalla para ingresar de forma manual entregas parciales, y un apartado directo de "Cobrado en Efectivo".
- **📦 Stock del Vehículo ("Mi Camioneta"):** Herramientas para que el chofer consulte dinámicamente cuántos sifones o botellas debe tener físicamente en este preciso momento de la jornada.

### 3. Flujo Presencial / Atención al Cliente (Fase 2 - EAC)
Para el personal responsable de recibir llamadas o WhatsApp:
- **📩 Bandeja de Consultas Modificada:** Interfaz al estilo bandeja de correos o red social con un globo rojo para notificar "Consultas no leídas".
- **📱 Integración de WhatsApp Remota:** Botón que captura el teléfono del lead desde un Form Web (Landing page) y abre directamente la app de WP con el texto de saludo semi-programado: *"Hola Miguel, somos de Tres Cerritos..."*.
- **🛒 Pedidos Exprés a 2 Dedos:** Asistente ágil de pedidos donde con tres toques (Cliente, Producto, "+" cantidad) un pedido se impacta como "CREADO" en la base, listo para designarse a la furgoneta, evitando el tecleo de formularios complejos al borde del mostrador.

---

## 🕒 LO QUE FALTA (Fase 3: Roadmap de Cierre Final)

Estas son las características necesarias para un cierre completo de producción empresarial y modernización total.

### 🛑 Obligatorio / Esencial para salir al mercado:
- **Certificado SSL Activo (HTTPS)**: Requisito de infraestructura puro. Sin `https://`, los navegadores modernos bloquearán la caché en frío y el prompt nativo de "Instalar como Aplicación", afectando la experiencia final.

### 📊 Altamente Recomendado a Corto Plazo:
- **Cierre Diario de Caja ("Mi Jornada Final"):** Necesitamos una pestaña que corra una fórmula algorítmica donde cruce lo que se vendió, los estados marcados en "Efectivo" versus "MercadoPago", y le dispare al repartidor una métrica limpia de lo que le tiene que dar en dinero físico al cajero en base, y cuántos bidones exactos tiene que descargar al depósito. 

### 💡 Features Avanzados que podemos agregar luego:
- **GPS / Tracking Lat-Lon Oculto:** Guardar la Georreferenciación (GPS) en la tabla base cada vez que el chofer presiona "Entregado" para poder resolver problemas de zonas de reclamos ("Yo te entregué a las 11AM acá").
- **Toma Fotográfica:** Permitir mediante `<input type="file" capture="camera">` que el chofer guarde una foto rápida donde se vea el "Local Cerrado" lo cual evitaría conflictos de validación con comercios.
- **Base de Datos Local (Offline Mode):** Construir una estructura a través de Base de Datos Nativa del navegador (IndexedDB) donde un usuario sin servicio 4G marque un pedido "Entregado", y que apenas encuentre una señal de celular o WiFi, el trabajador del Service Worker envíe el POST automáticamente en segundo plano.

---
*Documento autogenerado en referencia a los hitos alcanzados por el plan de arquitectura PWA — Abril 2026.*
