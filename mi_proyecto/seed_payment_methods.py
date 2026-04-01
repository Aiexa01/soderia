import os
import sys
import django

# Add current directory to Python path
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minisuper.settings')
    try:
        django.setup()
    except Exception as e:
        print(f"❌ Django Setup Validation Error: {e}")
        sys.exit(1)

from catalogos.models import MetodoPago
from core.models import Tenant

def seed_payments():
    tenant = Tenant.objects.first()
    if not tenant:
        print("❌ No tenant found.")
        return

    methods = [
        {'tipo': 'EFECTIVO', 'nombre': 'Efectivo', 'activo': True},
        {'tipo': 'TRANSFERENCIA', 'nombre': 'Transferencia / QR', 'activo': True},
        {'tipo': 'TARJETA', 'nombre': 'Tarjeta Crédito/Débito', 'activo': True},
    ]

    print(f"🌱 Seeding Payment Methods for Tenant: {tenant.name}")

    for m in methods:
        obj, created = MetodoPago.objects.get_or_create(
            tenant=tenant,
            tipo=m['tipo'],
            defaults={
                'nombre_metodo': m['nombre'],
                'activo': m['activo']
            }
        )
        if created:
            print(f"   ✅ Created: {m['nombre']}")
        else:
            print(f"   ok Exists: {m['nombre']}")

    # Verify
    count = MetodoPago.objects.filter(tenant=tenant).count()
    print(f"\nTotal Payment Methods: {count}")

if __name__ == '__main__':
    seed_payments()
