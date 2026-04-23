from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Proyecto_Soderia', '0003_auto_20260420_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Despacho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.date.today, help_text='Fecha de reparto')),
                ('estado', models.CharField(
                    choices=[('ABIERTO', 'Abierto'), ('EN_RUTA', 'En ruta'), ('CERRADO', 'Cerrado')],
                    default='ABIERTO',
                    max_length=20,
                )),
                ('notas', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('camioneta', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='despachos',
                    to='Proyecto_Soderia.camioneta',
                )),
                ('creado_por', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='despachos_creados',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'db_table': 'despacho',
                'ordering': ['-fecha', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='DespachoPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden_entrega', models.PositiveIntegerField(default=0, help_text='Posición en la ruta (1 = primero)')),
                ('despacho', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='items',
                    to='Proyecto_Soderia.despacho',
                )),
                ('pedido', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='despacho_items',
                    to='Proyecto_Soderia.pedido',
                )),
            ],
            options={
                'db_table': 'despacho_pedido',
                'ordering': ['orden_entrega'],
                'unique_together': {('despacho', 'pedido')},
            },
        ),
    ]
