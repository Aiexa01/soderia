import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1] / "mi_proyecto"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mi_proyecto.settings")

import django  # noqa: E402

django.setup()

from Proyecto_Soderia.models import Camioneta  # noqa: E402


CAMIONETAS = [
    {"nombre": "Master 1", "patente": "AD100MA"},
    {"nombre": "Master 2", "patente": "AD101MA"},
    {"nombre": "Master 3", "patente": "AD102MA"},
    {"nombre": "Foton 1", "patente": "AD200FO"},
    {"nombre": "Foton 2", "patente": "AD201FO"},
    {"nombre": "Sprinter 1", "patente": "AD300SP"},
    {"nombre": "Sprinter 2", "patente": "AD301SP"},
    {"nombre": "Sprinter 3", "patente": "AD302SP"},
]


def main():
    created = 0
    updated = 0

    for item in CAMIONETAS:
        _, was_created = Camioneta.objects.update_or_create(
            patente=item["patente"],
            defaults={
                "nombre": item["nombre"],
                "repartidor": None,
                "active": True,
                "estado": Camioneta.Estados.DISPONIBLE,
            },
        )
        if was_created:
            created += 1
        else:
            updated += 1

    print(f"Camionetas creadas: {created}")
    print(f"Camionetas actualizadas: {updated}")
    print(f"Total camionetas: {Camioneta.objects.count()}")


if __name__ == "__main__":
    main()
