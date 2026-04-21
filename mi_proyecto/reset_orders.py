import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from Proyecto_Soderia.models import Pedido
Pedido.objects.filter(estado__in=['EN_REPARTO', 'DESPACHADO']).update(estado='ASIGNADO')
print("Pedidos actualizados correctamente.")
