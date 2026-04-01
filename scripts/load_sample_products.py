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

from Proyecto_Soderia.models import Producto  # noqa: E402


PRODUCTS = [
    {
        "nombre": "Soda 1.5L",
        "capacidad_litros": Decimal("1.50"),
        "tipo_envase": Producto.TipoEnvase.BOTELLA,
        "retornable": False,
        "precio": Decimal("1800.00"),
        "max_por_camioneta": 120,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": False,
        "deposito_envase": None,
    },
    {
        "nombre": "Soda 2L",
        "capacidad_litros": Decimal("2.00"),
        "tipo_envase": Producto.TipoEnvase.BOTELLA,
        "retornable": False,
        "precio": Decimal("2200.00"),
        "max_por_camioneta": 100,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": False,
        "deposito_envase": None,
    },
    {
        "nombre": "Sifon Soda 1.25L",
        "capacidad_litros": Decimal("1.25"),
        "tipo_envase": Producto.TipoEnvase.SIFON,
        "retornable": True,
        "precio": Decimal("2500.00"),
        "max_por_camioneta": 120,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": True,
        "deposito_envase": Decimal("3500.00"),
    },
    {
        "nombre": "Bidon Agua 12L",
        "capacidad_litros": Decimal("12.00"),
        "tipo_envase": Producto.TipoEnvase.BIDON,
        "retornable": True,
        "precio": Decimal("4200.00"),
        "max_por_camioneta": 40,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": True,
        "deposito_envase": Decimal("6000.00"),
    },
    {
        "nombre": "Bidon Agua 20L",
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
        "nombre": "Agua Mineral 500ml Pack x6",
        "capacidad_litros": Decimal("0.50"),
        "tipo_envase": Producto.TipoEnvase.BOTELLA,
        "retornable": False,
        "precio": Decimal("3200.00"),
        "max_por_camioneta": 80,
        "unidad_venta": Producto.UnidadVenta.PACK,
        "requiere_envase": False,
        "deposito_envase": None,
    },
    {
        "nombre": "Agua Mineral 1.5L Pack x6",
        "capacidad_litros": Decimal("1.50"),
        "tipo_envase": Producto.TipoEnvase.BOTELLA,
        "retornable": False,
        "precio": Decimal("5400.00"),
        "max_por_camioneta": 60,
        "unidad_venta": Producto.UnidadVenta.PACK,
        "requiere_envase": False,
        "deposito_envase": None,
    },
    {
        "nombre": "Agua Saborizada 1.5L",
        "capacidad_litros": Decimal("1.50"),
        "tipo_envase": Producto.TipoEnvase.BOTELLA,
        "retornable": False,
        "precio": Decimal("2100.00"),
        "max_por_camioneta": 80,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": False,
        "deposito_envase": None,
    },
    {
        "nombre": "Gaseosa Cola 2.25L",
        "capacidad_litros": Decimal("2.25"),
        "tipo_envase": Producto.TipoEnvase.BOTELLA,
        "retornable": False,
        "precio": Decimal("3100.00"),
        "max_por_camioneta": 70,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": False,
        "deposito_envase": None,
    },
    {
        "nombre": "Gaseosa Lima Limon 2.25L",
        "capacidad_litros": Decimal("2.25"),
        "tipo_envase": Producto.TipoEnvase.BOTELLA,
        "retornable": False,
        "precio": Decimal("3050.00"),
        "max_por_camioneta": 70,
        "unidad_venta": Producto.UnidadVenta.UNIDAD,
        "requiere_envase": False,
        "deposito_envase": None,
    },
]


def main():
    created = 0
    updated = 0

    for item in PRODUCTS:
        _, was_created = Producto.objects.update_or_create(
            nombre=item["nombre"],
            defaults={**item, "active": True},
        )
        if was_created:
            created += 1
        else:
            updated += 1

    total = Producto.objects.count()
    print(f"Productos creados: {created}")
    print(f"Productos actualizados: {updated}")
    print(f"Total productos: {total}")


if __name__ == "__main__":
    main()
