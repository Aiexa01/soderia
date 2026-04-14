import os
import sys
from django.utils import timezone
import random

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../mi_proyecto'))
sys.path.insert(0, PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mi_proyecto.settings")

import django
django.setup()

from Proyecto_Soderia.models import Camioneta, Client, Producto, Pedido, PedidoDetalle, PedidoEstado
from django.contrib.auth.models import User

def generate_orders():
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.first()

    camionetas = Camioneta.objects.filter(active=True)
    clientes = list(Client.objects.filter(activo=True))
    productos = list(Producto.objects.filter(active=True))

    if not camionetas or not clientes or not productos:
        print("Error: faltan camionetas, clientes o productos para generar pedidos.")
        return

    for camioneta in camionetas:
        print(f"Generando pedidos para la camioneta: {camioneta.nombre}")
        for i in range(5):
            cliente = random.choice(clientes)
            pedido = Pedido.objects.create(
                cliente=cliente,
                camioneta=camioneta,
                estado=Pedido.Estados.EN_REPARTO,
                creado_por=admin_user,
                total=0
            )
            PedidoEstado.objects.create(
                pedido=pedido,
                estado=Pedido.Estados.EN_REPARTO,
                usuario=admin_user
            )
            
            producto = random.choice(productos)
            cantidad = random.randint(1, 4)
            detalle = PedidoDetalle.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )
            pedido.total = detalle.subtotal()
            pedido.save(update_fields=['total'])
            print(f"  - Pedido #{pedido.id} para cliente {cliente.name} con {cantidad}x {producto.nombre}")

    print("Se han generado exitosamente los pedidos de prueba.")

if __name__ == "__main__":
    generate_orders()
