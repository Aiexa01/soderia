import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BASE_DIR / 'mi_proyecto'

sys.path.insert(0, str(PROJECT_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')

import django  # noqa: E402

django.setup()

from Proyecto_Soderia.models import Barrio, Client  # noqa: E402


def norm(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s


def main():
    barrios = list(Barrio.objects.all())
    barrios_norm = [(b, norm(b.nombre)) for b in barrios]

    updated = 0
    no_match = 0
    multiple = 0
    total = 0

    for client in Client.objects.iterator():
        total += 1
        if client.barrio_ref_id:
            continue
        raw = (client.barrio or '').strip()
        if not raw:
            no_match += 1
            continue
        c_norm = norm(raw)

        matches = []
        for b, b_norm in barrios_norm:
            if b_norm and b_norm in c_norm:
                matches.append(b)

        if not matches:
            no_match += 1
            continue

        if len(matches) > 1:
            multiple += 1
            # choose shortest name
            matches.sort(key=lambda x: len(x.nombre))

        chosen = matches[0]
        client.barrio_ref = chosen
        client.barrio = chosen.nombre
        client.zona = chosen.zona
        client.save(update_fields=['barrio_ref', 'barrio', 'zona'])
        updated += 1

    print(f'Total clientes: {total}')
    print(f'Actualizados: {updated}')
    print(f'Sin match: {no_match}')
    print(f'Multiples matches: {multiple}')


if __name__ == '__main__':
    main()
