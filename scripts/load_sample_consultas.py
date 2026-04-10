import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1] / "mi_proyecto"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mi_proyecto.settings")

import django  # noqa: E402

django.setup()

from Proyecto_Soderia.models import ConsultaWeb  # noqa: E402


CONSULTAS = [
    {
        "nombre": "Carlos Mendoza",
        "email": "carlos.mendoza@gmail.com",
        "telefono": "3874551234",
        "mensaje": "Hola, necesito 2 bidones de 20 litros para mi oficina en centro. ¿Hacen entregas los sábados? También me interesa un dispenser frío/calor.",
        "estado": "NUEVA",
    },
    {
        "nombre": "Laura Gutiérrez",
        "email": "laura.g@hotmail.com",
        "telefono": "3874782910",
        "mensaje": "Buenas tardes, quería consultar precios de soda sifón por cajón. Somos un restaurante en la zona de Tres Cerritos y necesitaríamos entrega semanal.",
        "estado": "NUEVA",
    },
    {
        "nombre": "Roberto Álvarez",
        "email": "",
        "telefono": "3874123456",
        "mensaje": "Quiero empezar a pedir agua mineral para mi casa. ¿Cuáles son las opciones de bidón y el costo del depósito? Estoy por barrio Grand Bourg.",
        "estado": "NUEVA",
    },
    {
        "nombre": "Mariana Villagrán",
        "email": "mariana.villagran@yahoo.com.ar",
        "telefono": "3874995511",
        "mensaje": "Buenas! Necesito saber si hacen instalación de dispenser. Tengo uno marca Tres Cerritos que me vendieron hace años y no enfría bien.",
        "estado": "LEIDA",
    },
    {
        "nombre": "Eduardo Paz",
        "email": "edu_paz@gmail.com",
        "telefono": "3874667788",
        "mensaje": "Hola, soy dueño de un kiosco en barrio Santa Ana. Me interesa revender sus productos. ¿Tienen precios mayoristas?",
        "estado": "CONTACTADA",
    },
    {
        "nombre": "Silvia Romero",
        "email": "silvia.romero@outlook.com",
        "telefono": "3874334455",
        "mensaje": "Hola buenas tardes, necesito 4 cajones de soda sifón 1.5L y 1 bidón de 20L baja en sodio. Estoy en calle Mitre al 900. ¿Cuándo pueden pasar?",
        "estado": "LEIDA",
    },
    {
        "nombre": "Martín Casas",
        "email": "",
        "telefono": "3874228899",
        "mensaje": "Buenas, me pasaron su número del Facebook. Quería saber si entregan por la zona de San Lorenzo. Necesitaría bidones todas las semanas.",
        "estado": "NUEVA",
    },
    {
        "nombre": "Analía Figueroa",
        "email": "analia.fig@gmail.com",
        "telefono": "3874551177",
        "mensaje": "Hola! Me mudé hace poco a Salta y en mi anterior ciudad usaba soda Tres Cerritos. ¿Cómo hago para darme de alta como cliente? Estoy en barrio Castañares.",
        "estado": "CONTACTADA",
        "notas_internas": "Se la contactó por WhatsApp, pide que pasen el lunes a las 9hs.",
    },
]


def main():
    created = 0
    skipped = 0

    for data in CONSULTAS:
        # Evitar duplicados por nombre + teléfono
        exists = ConsultaWeb.objects.filter(
            nombre=data["nombre"],
            telefono=data["telefono"],
        ).exists()

        if exists:
            skipped += 1
            continue

        ConsultaWeb.objects.create(
            nombre=data["nombre"],
            email=data.get("email", ""),
            telefono=data["telefono"],
            mensaje=data["mensaje"],
            estado=data.get("estado", "NUEVA"),
            notas_internas=data.get("notas_internas", ""),
        )
        created += 1

    print(f"Consultas web creadas: {created}")
    if skipped:
        print(f"Consultas web omitidas (ya existían): {skipped}")


if __name__ == "__main__":
    main()
