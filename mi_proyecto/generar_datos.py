import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from Proyecto_Soderia.models import Client, Pedido, PedidoDetalle, Producto, Camioneta

def run():
    print("🚀 Generando 10 clientes de prueba y pedidos...")

    nombres = ["Martín Silva", "Lucía Fernández", "Jorge Castro", "Camila Gómez", "Esteban Quiroga",
               "Valeria Torres", "Andrés Romero", "Sofía Medina", "Diego Herrera", "Micaela Paz"]
    
    direcciones = ["San Martín 123", "Belgrano 456", "Mitre 789", "Sarmiento 101", "Av. Roca 202",
                   "Moreno 303", "Rivadavia 404", "Av. Libertador 505", "Pueyrredón 606", "Brown 707"]

    # Traemos productos y camionetas
    productos = list(Producto.objects.filter(active=True))
    camionetas = list(Camioneta.objects.filter(active=True))

    if not productos:
        print("❌ No hay productos activos.")
        return
    if not camionetas:
        print("❌ No hay camionetas activas.")
        return

    clientes_creados = []
    
    for i in range(10):
        cliente, created = Client.objects.get_or_create(
            name=nombres[i],
            defaults={
                'direccion': direcciones[i],
                'telefono': f"11-4567-{1000+i}",
                'referencias': "Casa puerta blanca",
                'numero_documento': f"{20000000+i}",
                'activo': True
            }
        )
        if created:
            print(f"✅ Cliente creado: {cliente.name}")
        clientes_creados.append(cliente)

    # Generamos pedidos (1 a 3 por cliente)
    for cliente in clientes_creados:
        num_pedidos = random.randint(1, 3)
        for _ in range(num_pedidos):
            camioneta = random.choice(camionetas)
            # 70% ASIGNADO, 30% CREADO
            estado = Pedido.Estados.ASIGNADO if random.random() < 0.7 else Pedido.Estados.CREADO
            
            pedido = Pedido.objects.create(
                cliente=cliente,
                camioneta=camioneta if estado == Pedido.Estados.ASIGNADO else None,
                estado=estado,
                total=0  # Se calcula abajo
            )
            
            # 1 a 2 productos por pedido
            total_pedido = 0
            prods = random.sample(productos, random.randint(1, min(2, len(productos))))
            for prod in prods:
                cantidad = random.randint(1, 4)
                precio = prod.precio
                subt = cantidad * precio
                
                PedidoDetalle.objects.create(
                    pedido=pedido,
                    producto=prod,
                    cantidad=cantidad,
                    precio_unitario=precio
                )
                total_pedido += subt
            
            pedido.total = total_pedido
            pedido.save(update_fields=['total'])
            
            print(f"📦 Pedido #{pedido.id} creado para {cliente.name} ({estado}) - ${total_pedido}")

    print("✅ Generación completada exitosamente.")

if __name__ == '__main__':
    run()
