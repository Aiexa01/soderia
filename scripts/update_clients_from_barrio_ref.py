import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BASE_DIR / 'mi_proyecto'

sys.path.insert(0, str(PROJECT_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')

import django  # noqa: E402

django.setup()

from Proyecto_Soderia.models import Client  # noqa: E402


def main():
    updated = 0
    total = 0
    missing_ref = 0

    qs = Client.objects.select_related('barrio_ref')
    for client in qs.iterator():
        total += 1
        if not client.barrio_ref:
            missing_ref += 1
            continue

        new_barrio = client.barrio_ref.nombre
        new_zona = client.barrio_ref.zona

        if client.barrio != new_barrio or client.zona != new_zona:
            client.barrio = new_barrio
            client.zona = new_zona
            client.save(update_fields=['barrio', 'zona'])
            updated += 1

    print(f'Total clientes: {total}')
    print(f'Actualizados: {updated}')
    print(f'Sin barrio_ref: {missing_ref}')


if __name__ == '__main__':
    main()
