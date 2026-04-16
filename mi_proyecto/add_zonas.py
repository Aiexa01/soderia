import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from Proyecto_Soderia.models import Zona

zonas = ['zona Norte', 'zona Sur', 'zona Este', 'Zona Oeste', 'zona Sudeste']
for z in zonas:
    obj, created = Zona.objects.get_or_create(nombre=z)
    if created:
        print(f"Created Zona: {z}")
    else:
        print(f"Zona already exists: {z}")
