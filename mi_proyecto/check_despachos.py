import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from Proyecto_Soderia.models import Despacho
qs = Despacho.objects.filter(estado__in=['ABIERTO','EN_RUTA'])
for d in qs:
    print(f"ID:{d.id} Camioneta:{d.camioneta.nombre} Estado:{d.estado}")
