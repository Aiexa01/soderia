"""
seed_all.py — Carga TODOS los datos iniciales del sistema.

Ejecutar dentro del contenedor:
    cd /opt/back_end/mi_proyecto
    python ../scripts/seed_all.py

Carga:
  1. Zonas y barrios
  2. Productos
  3. Usuarios con roles (admin, EAC, stock, técnico, repartidores)
  4. Camionetas (asignadas a repartidores)
  5. Clientes
  6. Depósito central
  7. Consultas web de ejemplo

Es idempotente: se puede ejecutar varias veces sin duplicar datos.
"""

import os
import sys
from decimal import Decimal
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1] / "mi_proyecto"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mi_proyecto.settings")

import django  # noqa: E402
django.setup()

from django.contrib.auth.models import Group, User  # noqa: E402
from Proyecto_Soderia.models import (  # noqa: E402
    Barrio,
    Camioneta,
    Client,
    ConsultaWeb,
    DatosPersonales,
    Deposito,
    Producto,
    Zona,
)


# ═══════════════════════════════════════════════════════════
#  1. ROLES
# ═══════════════════════════════════════════════════════════

ROLE_NAMES = [
    "Administrador",
    "Encargado de Atencion al Cliente",
    "Encargado de Stock",
    "Tecnico",
    "Repartidor",
]


def seed_roles():
    print("\n── Roles ──")
    for name in ROLE_NAMES:
        _, created = Group.objects.get_or_create(name=name)
        tag = "✓ creado" if created else "  existe"
        print(f"  {tag}: {name}")


# ═══════════════════════════════════════════════════════════
#  2. USUARIOS
# ═══════════════════════════════════════════════════════════

USERS = [
    {
        "username": "marlene",
        "password": "admin123",
        "first_name": "Marlene",
        "last_name": "Jerusalen",
        "email": "marlene@trescerritos.com",
        "is_staff": True,
        "is_superuser": True,
        "roles": ["Administrador"],
        "dni": "30000001",
    },
    {
        "username": "admin",
        "password": "admin123",
        "first_name": "Admin",
        "last_name": "Sistema",
        "email": "admin@trescerritos.com",
        "is_staff": True,
        "is_superuser": True,
        "roles": ["Administrador"],
        "dni": "30000002",
    },
    {
        "username": "carolina",
        "password": "carolina123",
        "first_name": "Carolina",
        "last_name": "Pérez",
        "email": "carolina@trescerritos.com",
        "is_staff": False,
        "is_superuser": False,
        "roles": ["Encargado de Atencion al Cliente"],
        "dni": "30000003",
    },
    {
        "username": "jorge",
        "password": "jorge123",
        "first_name": "Jorge",
        "last_name": "Medina",
        "email": "jorge@trescerritos.com",
        "is_staff": False,
        "is_superuser": False,
        "roles": ["Encargado de Stock"],
        "dni": "30000004",
    },
    {
        "username": "mario",
        "password": "mario123",
        "first_name": "Mario",
        "last_name": "Suárez",
        "email": "mario@trescerritos.com",
        "is_staff": False,
        "is_superuser": False,
        "roles": ["Repartidor"],
        "dni": "30000005",
    },
    {
        "username": "ricardo",
        "password": "ricardo123",
        "first_name": "Ricardo",
        "last_name": "Flores",
        "email": "ricardo@trescerritos.com",
        "is_staff": False,
        "is_superuser": False,
        "roles": ["Repartidor"],
        "dni": "30000006",
    },
    {
        "username": "roberto",
        "password": "roberto123",
        "first_name": "Roberto",
        "last_name": "Castro",
        "email": "roberto@trescerritos.com",
        "is_staff": False,
        "is_superuser": False,
        "roles": ["Tecnico"],
        "dni": "30000007",
    },
]


def seed_users():
    print("\n── Usuarios ──")
    created_count = 0
    for data in USERS:
        user, created = User.objects.get_or_create(
            username=data["username"],
            defaults={
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "email": data["email"],
                "is_staff": data["is_staff"],
                "is_superuser": data["is_superuser"],
                "is_active": True,
            },
        )
        if created:
            user.set_password(data["password"])
            user.save()
            created_count += 1

        # Asignar roles
        for role_name in data["roles"]:
            group = Group.objects.get(name=role_name)
            user.groups.add(group)

        # Crear DatosPersonales
        DatosPersonales.objects.get_or_create(
            user=user,
            defaults={"numero_documento": data.get("dni", "")},
        )

        roles_str = ", ".join(data["roles"])
        tag = "✓ creado" if created else "  existe"
        print(f"  {tag}: {data['username']} ({roles_str}) [pass: {data['password']}]")

    print(f"  Total usuarios: {User.objects.count()}")
    return created_count


# ═══════════════════════════════════════════════════════════
#  3. ZONAS Y BARRIOS
# ═══════════════════════════════════════════════════════════

ZONAS_BARRIOS = {
    "Centro": [
        "Centro", "Casco Histórico", "Balcarce", "Florida",
    ],
    "Norte": [
        "Tres Cerritos", "Grand Bourg", "Castañares",
        "Portal de los Cerros", "City",
    ],
    "Sur": [
        "San Benito", "Santa Ana", "Atocha",
        "Miguel Ortiz", "Villa Cristina",
    ],
    "Este": [
        "Limache", "La Loma", "El Tribuno",
        "Villa Lavalle", "Parque Belgrano",
    ],
    "Oeste": [
        "San Lorenzo", "Vaqueros", "La Caldera",
        "Villa San Antonio", "20 de Febrero",
    ],
}


def seed_zonas_barrios():
    print("\n── Zonas y Barrios ──")
    for zona_nombre, barrios in ZONAS_BARRIOS.items():
        zona, z_created = Zona.objects.get_or_create(
            nombre=zona_nombre,
            defaults={"active": True},
        )
        tag = "✓ creada" if z_created else "  existe"
        print(f"  {tag}: Zona '{zona_nombre}' ({len(barrios)} barrios)")
        for barrio_nombre in barrios:
            Barrio.objects.get_or_create(
                nombre=barrio_nombre,
                zona=zona,
                defaults={"active": True},
            )
    print(f"  Total zonas: {Zona.objects.count()} | Total barrios: {Barrio.objects.count()}")


# ═══════════════════════════════════════════════════════════
#  4. PRODUCTOS
# ═══════════════════════════════════════════════════════════

PRODUCTS = [
    {
        "nombre": "Bidón Azul 10L",
        "capacidad_litros": Decimal("10.00"),
        "tipo_envase": Producto.TipoEnvase.BIDON,
        "retornable": True,
        "precio": Decimal("3200.00"),
        "max_por_camioneta": 50,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": True,
        "deposito_envase": Decimal("5000.00"),
    },
    {
        "nombre": "Bidón Azul 20L",
        "capacidad_litros": Decimal("20.00"),
        "tipo_envase": Producto.TipoEnvase.BIDON,
        "retornable": True,
        "precio": Decimal("5800.00"),
        "max_por_camioneta": 30,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": True,
        "deposito_envase": Decimal("8000.00"),
    },
    {
        "nombre": "Bidón Baja en Sodio 10L",
        "capacidad_litros": Decimal("10.00"),
        "tipo_envase": Producto.TipoEnvase.BIDON,
        "retornable": True,
        "precio": Decimal("3800.00"),
        "max_por_camioneta": 40,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": True,
        "deposito_envase": Decimal("5500.00"),
    },
    {
        "nombre": "Bidón Baja en Sodio 20L",
        "capacidad_litros": Decimal("20.00"),
        "tipo_envase": Producto.TipoEnvase.BIDON,
        "retornable": True,
        "precio": Decimal("6500.00"),
        "max_por_camioneta": 25,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": True,
        "deposito_envase": Decimal("9000.00"),
    },
    {
        "nombre": "Sifón de Soda 1.5L",
        "capacidad_litros": Decimal("1.50"),
        "tipo_envase": Producto.TipoEnvase.SIFON,
        "retornable": True,
        "precio": Decimal("2500.00"),
        "max_por_camioneta": 120,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": True,
        "deposito_envase": Decimal("3500.00"),
    },
    {
        "nombre": "Agua No Retornable 500ml",
        "capacidad_litros": Decimal("0.50"),
        "tipo_envase": Producto.TipoEnvase.BOTELLA,
        "retornable": False,
        "precio": Decimal("800.00"),
        "max_por_camioneta": 200,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": False,
        "deposito_envase": None,
    },
    {
        "nombre": "Dispenser Común",
        "capacidad_litros": Decimal("0.00"),
        "tipo_envase": Producto.TipoEnvase.BIDON,
        "retornable": False,
        "precio": Decimal("45000.00"),
        "max_por_camioneta": 5,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": False,
        "deposito_envase": None,
    },
    {
        "nombre": "Dispenser Frío Calor",
        "capacidad_litros": Decimal("0.00"),
        "tipo_envase": Producto.TipoEnvase.BIDON,
        "retornable": False,
        "precio": Decimal("85000.00"),
        "max_por_camioneta": 3,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": False,
        "deposito_envase": None,
    },
    {
        "nombre": "Bidón Descartable 8L",
        "capacidad_litros": Decimal("8.00"),
        "tipo_envase": Producto.TipoEnvase.BIDON,
        "retornable": False,
        "precio": Decimal("2800.00"),
        "max_por_camioneta": 60,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": False,
        "deposito_envase": None,
    },
]


def seed_productos():
    print("\n── Productos ──")
    created = 0
    for item in PRODUCTS:
        _, was_created = Producto.objects.update_or_create(
            nombre=item["nombre"],
            defaults={**item, "active": True},
        )
        if was_created:
            created += 1
        tag = "✓" if was_created else " "
        print(f"  {tag} {item['nombre']} — ${item['precio']}")
    print(f"  Creados: {created} | Total: {Producto.objects.count()}")


# ═══════════════════════════════════════════════════════════
#  5. CAMIONETAS
# ═══════════════════════════════════════════════════════════

CAMIONETAS = [
    {"nombre": "Master 1", "patente": "AD100MA", "repartidor_username": "mario"},
    {"nombre": "Master 2", "patente": "AD101MA", "repartidor_username": "ricardo"},
    {"nombre": "Foton 1", "patente": "AD200FO", "repartidor_username": None},
    {"nombre": "Sprinter 1", "patente": "AD300SP", "repartidor_username": None},
    {"nombre": "Sprinter 2", "patente": "AD301SP", "repartidor_username": None},
]


def seed_camionetas():
    print("\n── Camionetas ──")
    created = 0
    for item in CAMIONETAS:
        repartidor = None
        if item["repartidor_username"]:
            repartidor = User.objects.filter(username=item["repartidor_username"]).first()

        cam, was_created = Camioneta.objects.update_or_create(
            patente=item["patente"],
            defaults={
                "nombre": item["nombre"],
                "repartidor": repartidor,
                "active": True,
                "estado": Camioneta.Estados.DISPONIBLE,
            },
        )
        if was_created:
            created += 1

        # Asignar todas las zonas a la camioneta
        zonas = Zona.objects.filter(active=True)
        cam.zonas.set(zonas)

        rep = repartidor.username if repartidor else "sin asignar"
        tag = "✓" if was_created else " "
        print(f"  {tag} {item['nombre']} ({item['patente']}) → {rep}")
    print(f"  Creadas: {created} | Total: {Camioneta.objects.count()}")


# ═══════════════════════════════════════════════════════════
#  6. CLIENTES
# ═══════════════════════════════════════════════════════════

CLIENTS = [
    ("Ana Gómez", "DNI", "30100001", "3875001001", "ana@email.com", "Av. Belgrano 1250", "Centro"),
    ("Luis Fernández", "DNI", "30100002", "3875001002", "", "Caseros 842", "Centro"),
    ("María López", "DNI", "30100003", "3875001003", "maria.lopez@gmail.com", "Dean Funes 1145", "Centro"),
    ("Carlos Ruiz", "DNI", "30100004", "3875001004", "", "Alvarado 1678", "Norte"),
    ("Sofía Herrera", "DNI", "30100005", "3875001005", "sofi.h@hotmail.com", "Mitre 932", "Norte"),
    ("Javier Sosa", "DNI", "30100006", "3875001006", "", "España 1451", "Norte"),
    ("Lucía Torres", "DNI", "30100007", "3875001007", "lucia.t@gmail.com", "Leguizamón 621", "Sur"),
    ("Pablo Díaz", "DNI", "30100008", "3875001008", "", "San Martín 1733", "Sur"),
    ("Valeria Cruz", "DNI", "30100009", "3875001009", "vale.cruz@yahoo.com", "20 de Febrero 518", "Oeste"),
    ("Diego Navarro", "DNI", "30100010", "3875001010", "", "Urquiza 1389", "Este"),
    ("Paula Molina", "DNI", "30100011", "3875001011", "paula.m@outlook.com", "Ituzaingó 744", "Este"),
    ("Martín Vega", "DNI", "30100012", "3875001012", "", "Corrientes 1610", "Sur"),
    ("Julieta Pereyra", "DNI", "30100013", "3875001013", "juli.p@gmail.com", "Florida 980", "Centro"),
    ("Nicolás Castillo", "DNI", "30100014", "3875001014", "", "Zabala 420", "Oeste"),
    ("Camila Romero", "DNI", "30100015", "3875001015", "cami.rom@gmail.com", "Balcarce 1555", "Centro"),
    # Comercios
    ("Restaurante Don Pedro", "CUIT", "20301000161", "3874550101", "donpedro@email.com", "Caseros 1200", "Centro"),
    ("Kiosco El Sol", "CUIT", "20301000172", "3874550102", "", "San Martín 890", "Sur"),
    ("Hotel Salta Premium", "CUIT", "20301000183", "3874550103", "hotel@saltapremium.com", "Buenos Aires 340", "Centro"),
    ("Gimnasio Fit Zone", "CUIT", "20301000194", "3874550104", "info@fitzone.com", "Pellegrini 1500", "Norte"),
    ("Farmacia Central", "CUIT", "20301000205", "3874550105", "", "España 800", "Norte"),
]


def seed_clientes():
    print("\n── Clientes ──")
    created = 0
    for name, tipo_doc, num_doc, telefono, email, direccion, zona_nombre in CLIENTS:
        zona = Zona.objects.filter(nombre=zona_nombre).first()
        tipo_cliente = Client.TipoCliente.COMERCIO if tipo_doc == "CUIT" else Client.TipoCliente.PERSONA

        _, was_created = Client.objects.update_or_create(
            numero_documento=num_doc,
            defaults={
                "name": name,
                "tipo_cliente": tipo_cliente,
                "tipo_documento": tipo_doc,
                "telefono": telefono,
                "email": email,
                "direccion": direccion,
                "zona": zona,
                "activo": True,
            },
        )
        if was_created:
            created += 1
    print(f"  Creados: {created} | Total: {Client.objects.count()}")
    print(f"  Personas: {Client.objects.filter(tipo_cliente='PERSONA').count()} | Comercios: {Client.objects.filter(tipo_cliente='COMERCIO').count()}")


# ═══════════════════════════════════════════════════════════
#  7. DEPÓSITO CENTRAL
# ═══════════════════════════════════════════════════════════

def seed_deposito():
    print("\n── Depósito ──")
    from django.utils import timezone
    now = timezone.now()
    dep, created = Deposito.objects.get_or_create(
        nombre="Depósito Central",
        defaults={
            "direccion": "Las Heras 1443, Salta Capital",
            "activo": True,
            "created_at": now,
            "updated_at": now,
        },
    )
    tag = "✓ creado" if created else "  existe"
    print(f"  {tag}: {dep.nombre}")


# ═══════════════════════════════════════════════════════════
#  8. CONSULTAS WEB
# ═══════════════════════════════════════════════════════════

CONSULTAS = [
    {
        "nombre": "Carlos Mendoza",
        "email": "carlos.mendoza@gmail.com",
        "telefono": "3874551234",
        "mensaje": "Hola, necesito 2 bidones de 20 litros para mi oficina en centro. ¿Hacen entregas los sábados? También me interesa un dispenser frío/calor.",
        "estado": "NUEVA",
    },
    {
        "nombre": "Laura Gutiérrez",
        "email": "laura.g@hotmail.com",
        "telefono": "3874782910",
        "mensaje": "Buenas tardes, quería consultar precios de soda sifón por cajón. Somos un restaurante en la zona de Tres Cerritos y necesitaríamos entrega semanal.",
        "estado": "NUEVA",
    },
    {
        "nombre": "Roberto Álvarez",
        "email": "",
        "telefono": "3874123456",
        "mensaje": "Quiero empezar a pedir agua mineral para mi casa. ¿Cuáles son las opciones de bidón y el costo del depósito? Estoy por barrio Grand Bourg.",
        "estado": "NUEVA",
    },
    {
        "nombre": "Mariana Villagrán",
        "email": "mariana.villagran@yahoo.com.ar",
        "telefono": "3874995511",
        "mensaje": "Buenas! Necesito saber si hacen instalación de dispenser. Tengo uno marca Tres Cerritos que me vendieron hace años y no enfría bien.",
        "estado": "LEIDA",
    },
    {
        "nombre": "Eduardo Paz",
        "email": "edu_paz@gmail.com",
        "telefono": "3874667788",
        "mensaje": "Hola, soy dueño de un kiosco en barrio Santa Ana. Me interesa revender sus productos. ¿Tienen precios mayoristas?",
        "estado": "CONTACTADA",
        "notas_internas": "Se habló por WhatsApp. Quiere lista de precios mayorista. Enviar catálogo.",
    },
    {
        "nombre": "Silvia Romero",
        "email": "silvia.romero@outlook.com",
        "telefono": "3874334455",
        "mensaje": "Hola buenas tardes, necesito 4 cajones de soda sifón 1.5L y 1 bidón de 20L baja en sodio. Estoy en calle Mitre al 900.",
        "estado": "LEIDA",
    },
    {
        "nombre": "Martín Casas",
        "email": "",
        "telefono": "3874228899",
        "mensaje": "Buenas, me pasaron su número del Facebook. Quería saber si entregan por la zona de San Lorenzo. Necesitaría bidones todas las semanas.",
        "estado": "NUEVA",
    },
    {
        "nombre": "Analía Figueroa",
        "email": "analia.fig@gmail.com",
        "telefono": "3874551177",
        "mensaje": "Hola! Me mudé hace poco a Salta y en mi anterior ciudad usaba soda Tres Cerritos. ¿Cómo hago para darme de alta como cliente? Estoy en barrio Castañares.",
        "estado": "CONTACTADA",
        "notas_internas": "Se la contactó por WhatsApp, pide que pasen el lunes a las 9hs.",
    },
]


def seed_consultas():
    print("\n── Consultas Web ──")
    created = 0
    for data in CONSULTAS:
        exists = ConsultaWeb.objects.filter(
            nombre=data["nombre"],
            telefono=data["telefono"],
        ).exists()
        if exists:
            continue

        ConsultaWeb.objects.create(
            nombre=data["nombre"],
            email=data.get("email", ""),
            telefono=data["telefono"],
            mensaje=data["mensaje"],
            estado=data.get("estado", "NUEVA"),
            notas_internas=data.get("notas_internas", ""),
        )
        created += 1
    print(f"  Creadas: {created} | Total: {ConsultaWeb.objects.count()}")


# ═══════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════

def main():
    print("=" * 55)
    print("  SEED ALL — Soda y Agua Tres Cerritos")
    print("=" * 55)

    seed_roles()
    seed_users()
    seed_zonas_barrios()
    seed_productos()
    seed_camionetas()
    seed_clientes()
    seed_deposito()
    seed_consultas()

    print("\n" + "=" * 55)
    print("  ✅ Datos iniciales cargados correctamente.")
    print("=" * 55)
    print("\n  Usuarios creados:")
    print("  ─────────────────────────────────────────")
    for u in USERS:
        print(f"  │ {u['username']:<12} │ pass: {u['password']:<14} │ {', '.join(u['roles'])}")
    print("  ─────────────────────────────────────────")
    print()


if __name__ == "__main__":
    main()
