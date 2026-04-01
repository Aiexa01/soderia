import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1] / "mi_proyecto"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mi_proyecto.settings")

import django  # noqa: E402

django.setup()

from Proyecto_Soderia.models import Client, Zona  # noqa: E402


CLIENTS = [
    ("Ana Gomez", "DNI", "30100001", "3875001001", "Av. Belgrano 1250"),
    ("Luis Fernandez", "DNI", "30100002", "3875001002", "Caseros 842"),
    ("Maria Lopez", "DNI", "30100003", "3875001003", "Dean Funes 1145"),
    ("Carlos Ruiz", "DNI", "30100004", "3875001004", "Alvarado 1678"),
    ("Sofia Herrera", "DNI", "30100005", "3875001005", "Mitre 932"),
    ("Javier Sosa", "DNI", "30100006", "3875001006", "España 1451"),
    ("Lucia Torres", "DNI", "30100007", "3875001007", "Leguizamon 621"),
    ("Pablo Diaz", "DNI", "30100008", "3875001008", "San Martin 1733"),
    ("Valeria Cruz", "DNI", "30100009", "3875001009", "20 de Febrero 518"),
    ("Diego Navarro", "DNI", "30100010", "3875001010", "Urquiza 1389"),
    ("Paula Molina", "DNI", "30100011", "3875001011", "Ituzaingo 744"),
    ("Martin Vega", "DNI", "30100012", "3875001012", "Corrientes 1610"),
    ("Julieta Pereyra", "DNI", "30100013", "3875001013", "Florida 980"),
    ("Nicolas Castillo", "DNI", "30100014", "3875001014", "Zabala 420"),
    ("Camila Romero", "DNI", "30100015", "3875001015", "Balcarce 1555"),
    ("Federico Ramos", "DNI", "30100016", "3875001016", "Ameghino 890"),
    ("Micaela Vargas", "DNI", "30100017", "3875001017", "Pellegrini 1332"),
    ("Gonzalo Medina", "DNI", "30100018", "3875001018", "Alsina 705"),
    ("Florencia Acosta", "DNI", "30100019", "3875001019", "Rivadavia 1499"),
    ("Sebastian Ibarra", "DNI", "30100020", "3875001020", "San Juan 812"),
    ("Gabriela Silva", "DNI", "30100021", "3875001021", "Tucuman 1246"),
    ("Matias Arias", "DNI", "30100022", "3875001022", "Mendoza 975"),
    ("Noelia Cardozo", "DNI", "30100023", "3875001023", "La Rioja 1418"),
    ("Leandro Correa", "DNI", "30100024", "3875001024", "Vicente Lopez 633"),
    ("Rocio Figueroa", "DNI", "30100025", "3875001025", "Catamarca 1564"),
    ("Emanuel Aguirre", "DNI", "30100026", "3875001026", "Santiago del Estero 845"),
    ("Brenda Paz", "DNI", "30100027", "3875001027", "Jujuy 1290"),
    ("Facundo Salas", "DNI", "30100028", "3875001028", "Olavarria 560"),
    ("Daniela Toledo", "DNI", "30100029", "3875001029", "Adolfo Guemes 1711"),
    ("Ignacio Rojas", "DNI", "30100030", "3875001030", "Entre Rios 1188"),
]


def main():
    zona, _ = Zona.objects.get_or_create(nombre="Salta Capital", defaults={"active": True})
    if not zona.active:
        zona.active = True
        zona.save(update_fields=["active"])

    created = 0
    updated = 0

    for name, tipo_documento, numero_documento, telefono, direccion in CLIENTS:
        _, was_created = Client.objects.update_or_create(
            numero_documento=numero_documento,
            defaults={
                "name": name,
                "tipo_cliente": Client.TipoCliente.PERSONA,
                "tipo_documento": tipo_documento,
                "telefono": telefono,
                "email": "",
                "direccion": direccion,
                "zona": zona,
                "barrio": None,
                "referencias": "",
                "activo": True,
            },
        )
        if was_created:
            created += 1
        else:
            updated += 1

    print(f"Zona usada: {zona.nombre} (id={zona.id})")
    print(f"Clientes creados: {created}")
    print(f"Clientes actualizados: {updated}")


if __name__ == "__main__":
    main()
