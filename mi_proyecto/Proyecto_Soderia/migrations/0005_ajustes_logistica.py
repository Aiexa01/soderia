from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proyecto_Soderia', '0004_despacho_despachopedido'),
    ]

    operations = [
        # 1. Agrega REINTENTAR a los choices de Pedido.estado
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(
                choices=[
                    ('CREADO', 'Creado'),
                    ('ASIGNADO', 'Asignado'),
                    ('DESPACHADO', 'Despachado'),
                    ('EN_REPARTO', 'En reparto'),
                    ('ENTREGADO', 'Entregado'),
                    ('DEVUELTO', 'Devuelto'),
                    ('PAGADO', 'Pagado'),
                    ('REINTENTAR', 'Reintentar'),
                ],
                default='CREADO',
                max_length=20,
            ),
        ),
        # 2. Agrega REINTENTAR a PedidoEstado.estado
        migrations.AlterField(
            model_name='pedidoestado',
            name='estado',
            field=models.CharField(
                choices=[
                    ('CREADO', 'Creado'),
                    ('ASIGNADO', 'Asignado'),
                    ('DESPACHADO', 'Despachado'),
                    ('EN_REPARTO', 'En reparto'),
                    ('ENTREGADO', 'Entregado'),
                    ('DEVUELTO', 'Devuelto'),
                    ('PAGADO', 'Pagado'),
                    ('REINTENTAR', 'Reintentar'),
                ],
                max_length=20,
            ),
        ),
        # 3. Agrega UniqueConstraint condicional en Despacho
        migrations.AddConstraint(
            model_name='despacho',
            constraint=models.UniqueConstraint(
                condition=models.Q(estado__in=['ABIERTO', 'EN_RUTA']),
                fields=['camioneta', 'fecha'],
                name='unique_despacho_activo_por_camioneta_dia',
            ),
        ),
        # 4. Agrega campo extra (JSONField) a AuditLog
        migrations.AddField(
            model_name='auditlog',
            name='extra',
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text='Contexto estructurado: estado_anterior, estado_nuevo, despacho_id, etc.',
            ),
        ),
    ]
