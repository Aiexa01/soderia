from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Elimina el UniqueConstraint condicional que no funciona en MySQL.
    La validación de doble despacho se maneja en la capa de views.
    """

    dependencies = [
        ('Proyecto_Soderia', '0005_ajustes_logistica'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='despacho',
            name='unique_despacho_activo_por_camioneta_dia',
        ),
    ]
