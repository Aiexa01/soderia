from django.db import models
from django.contrib.auth.models import Group, User




class Client(models.Model):
    class TipoCliente(models.TextChoices):
        PERSONA = 'PERSONA', 'Persona'
        COMERCIO = 'COMERCIO', 'Comercio'

    class TipoDocumento(models.TextChoices):
        DNI = 'DNI', 'DNI'
        CUIT = 'CUIT', 'CUIT'

    name = models.CharField(max_length=120)
    tipo_cliente = models.CharField(max_length=20, choices=TipoCliente.choices, default=TipoCliente.PERSONA)
    tipo_documento = models.CharField(max_length=10, choices=TipoDocumento.choices, default=TipoDocumento.DNI)
    numero_documento = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    zona = models.ForeignKey('Zona', null=True, blank=True, on_delete=models.SET_NULL, related_name='clientes')
    barrio = models.ForeignKey('Barrio', null=True, blank=True, on_delete=models.SET_NULL, related_name='clientes')
    referencias = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        db_table = 'client'

    def __str__(self):
        return self.name

    @property
    def documento(self):
        return self.numero_documento


class Zona(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        db_table = 'zona'

    def __str__(self):
        return self.nombre


class Barrio(models.Model):
    nombre = models.CharField(max_length=80)
    zona = models.ForeignKey(Zona, on_delete=models.PROTECT, related_name='barrios')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        unique_together = ('nombre', 'zona')
        db_table = 'barrio'

    def __str__(self):
        return self.nombre


class DatosPersonales(models.Model):
    id_datos_personales = models.AutoField(primary_key=True, db_column='id_datos_personales')
    ESTADO_CHOICES = [
        ('habilitado', 'Habilitado'),
        ('suspendido', 'Suspendido'),
        ('baja', 'Baja'),
    ]

    user = models.OneToOneField(User, db_column='user_id', on_delete=models.CASCADE, related_name='datos_personales', null=True)
    tipo_documento = models.CharField(max_length=10, blank=True, null=True)
    numero_documento = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    
    class Meta:
        db_table = 'datos_personales'
        managed = True

    def __str__(self):
        return f'{self.user} - {self.estado}'

    @property
    def estado(self):
        if self.user and self.user.is_active:
            return 'habilitado'
        return 'suspendido'




class Camioneta(models.Model):
    class Estados(models.TextChoices):
        DISPONIBLE = 'DISPONIBLE', 'Disponible'
        EN_RUTA = 'EN_RUTA', 'En ruta'
        FUERA = 'FUERA', 'Fuera de servicio'

    nombre = models.CharField(max_length=120)
    patente = models.CharField(max_length=20, unique=True)
    repartidor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='camionetas')
    active = models.BooleanField(default=True)
    estado = models.CharField(max_length=20, choices=Estados.choices, default=Estados.DISPONIBLE)
   
    zonas = models.ManyToManyField(
        'Zona',
        blank=True,
        related_name='camionetas',
        db_table='camioneta_zonas',
    )

    class Meta:
        ordering = ['nombre']
        db_table = 'camioneta'

    def __str__(self):
        return f'{self.nombre} ({self.patente})'


class Pedido(models.Model):
    class Estados(models.TextChoices):
        CREADO = 'CREADO', 'Creado'
        ASIGNADO = 'ASIGNADO', 'Asignado'
        EN_REPARTO = 'EN_REPARTO', 'En reparto'
        ENTREGADO = 'ENTREGADO', 'Entregado'
        DEVUELTO = 'DEVUELTO', 'Devuelto'
        PAGADO = 'PAGADO', 'Pagado'

    class FormasPago(models.TextChoices):
        EFECTIVO = 'efectivo', 'Efectivo'
        TRANSFERENCIA = 'transferencia', 'Transferencia'
        TARJETA = 'tarjeta', 'Tarjeta'
        MERCADOPAGO = 'mercadopago', 'Mercado Pago'

    cliente = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='pedidos')
    camioneta = models.ForeignKey(Camioneta, null=True, blank=True, on_delete=models.SET_NULL, related_name='pedidos')
    estado = models.CharField(max_length=20, choices=Estados.choices, default=Estados.CREADO)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    forma_pago = models.CharField(max_length=60, choices=FormasPago.choices, blank=True)
    pago_monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pago_motivo = models.CharField(max_length=200, blank=True)
    pago_fecha = models.DateTimeField(null=True, blank=True)
    creado_por = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='pedidos_creados')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'pedido'

    @property
    def repartidor(self):
        return self.camioneta.repartidor if self.camioneta else None

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente}'


class PedidoEstado(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='historial')
    estado = models.CharField(max_length=20, choices=Pedido.Estados.choices)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='pedido_estados')
    motivo = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'pedidoestado'

    def __str__(self):
        return f'{self.pedido} -> {self.estado}'


class Producto(models.Model):
    class TipoEnvase(models.TextChoices):
        BOTELLA = 'BOTELLA', 'Botella'
        SIFON = 'SIFON', 'Sifon'
        BIDON = 'BIDON', 'Bidon'

    class UnidadVenta(models.TextChoices):
        UNIDAD = 'UNIDAD', 'Unidad'
        PACK = 'PACK', 'Pack'
        CAJA = 'CAJA', 'Caja'

    nombre = models.CharField(max_length=120)
    capacidad_litros = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tipo_envase = models.CharField(max_length=20, choices=TipoEnvase.choices, default=TipoEnvase.BOTELLA)
    retornable = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_por_camioneta = models.IntegerField(null=True, blank=True)
    unidad_venta = models.CharField(max_length=20, choices=UnidadVenta.choices, default=UnidadVenta.UNIDAD)
    requiere_envase = models.BooleanField(default=False)
    deposito_envase = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        db_table = 'producto'

    def __str__(self):
        return self.nombre


class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='detalles')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f'{self.pedido} - {self.producto}'

    class Meta:
        db_table = 'pedidodetalle'


class StockCamioneta(models.Model):
    camioneta = models.ForeignKey(Camioneta, on_delete=models.CASCADE, related_name='stock')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='stock_camionetas')
    cantidad_actual = models.IntegerField(default=0)

    class Meta:
        unique_together = ('camioneta', 'producto')
        ordering = ['producto__nombre']
        db_table = 'stockcamioneta'

    def __str__(self):
        return f'{self.camioneta} - {self.producto}'


class StockMovimiento(models.Model):
    class Tipos(models.TextChoices):
        ENTREGA = 'ENTREGA', 'Entrega'
        DEVOLUCION = 'DEVOLUCION', 'Devolucion'
        AJUSTE = 'AJUSTE', 'Ajuste'

    camioneta = models.ForeignKey(Camioneta, on_delete=models.CASCADE, related_name='movimientos')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='movimientos')
    pedido = models.ForeignKey(Pedido, null=True, blank=True, on_delete=models.SET_NULL, related_name='movimientos')
    tipo = models.CharField(max_length=20, choices=Tipos.choices)
    cantidad = models.IntegerField()
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='movimientos')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'stockmovimiento'

    def __str__(self):
        return f'{self.camioneta} - {self.producto} ({self.tipo})'
class Deposito(models.Model):
    nombre = models.CharField(max_length=120)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'deposito'

    def __str__(self):
        return self.nombre

class StockDeposito(models.Model):
    deposito = models.ForeignKey(
        Deposito,
        on_delete=models.CASCADE,
        db_column='deposito_id',
        related_name='stocks'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        db_column='producto_id',
        related_name='stocks_deposito'
    )
    cantidad_actual = models.IntegerField()

    class Meta:
        db_table = 'stockdeposito'
        unique_together = ('deposito', 'producto')

    def __str__(self):
        return f'{self.deposito} - {self.producto}'
