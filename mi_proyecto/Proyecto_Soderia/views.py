from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import timedelta

from .models import (
    Barrio,
    Camioneta,
    Client,
    ConsultaWeb,
    Deposito,
    Pedido,
    PedidoDetalle,
    PedidoEstado,
    Producto,
    DatosPersonales,
    StockCamioneta,
    StockDeposito,
    StockMovimiento,
    Zona,
)

ROLE_NAMES = [
    'Administrador',
    'Encargado de Atencion al Cliente',
    'Encargado de Stock',
    'Tecnico',
    'Repartidor',
]
ROLE_META = {
    'Administrador': {
        'code': 'ADM',
        'desc': 'Acceso total al sistema.',
        'warn': 'No combinar con roles operativos.',
    },
    'Encargado de Atencion al Cliente': {
        'code': 'EAC',
        'desc': 'Clientes, ventas e instalaciones.',
        'warn': 'No combinar con Tecnico.',
    },
    'Encargado de Stock': {
        'code': 'EST',
        'desc': 'Gestion de stock en depositos y camionetas.',
        'warn': 'No combinar con Administrador.',
    },
    'Tecnico': {
        'code': 'TEC',
        'desc': 'Reparaciones y mantenimiento.',
        'warn': 'No combinar con EAC.',
    },
    'Repartidor': {
        'code': 'REP',
        'desc': 'Reparto, stock de camioneta y servicios.',
        'warn': 'No combinar con Administrador.',
    },
}
LEGACY_ROLE_ALIASES = {
    'Repartidor': ['Repartidor / Instalador'],
}


def _has_any_role(user, roles):
    if user.is_superuser:
        return True
    expanded = set(roles)
    for role in roles:
        expanded.update(LEGACY_ROLE_ALIASES.get(role, []))
    return user.groups.filter(name__in=expanded).exists()


def _is_admin(user):
    return user.is_superuser or user.is_staff or _has_any_role(user, ['Administrador'])


def _can_manage_clients(user):
    return _is_admin(user) or _has_any_role(user, ['Encargado de Atencion al Cliente'])

def _can_manage_orders(user):
    return _is_admin(user) or _has_any_role(user, ['Encargado de Atencion al Cliente', 'Repartidor'])

def _can_manage_logistics(user):
    return _is_admin(user)

def _is_encargado_stock(user):
    return _has_any_role(user, ['Encargado de Stock'])

def _can_manage_stock(user):
    return _is_admin(user) or _is_encargado_stock(user)

def _get_user_camioneta(user):
    return Camioneta.objects.filter(repartidor=user, active=True).first()

def _role_context(user):
    is_admin = _is_admin(user)
    is_eac = _has_any_role(user, ['Encargado de Atencion al Cliente'])
    is_encargado_stock = _is_encargado_stock(user)
    is_tecnico = _has_any_role(user, ['Tecnico'])
    is_repartidor = _has_any_role(user, ['Repartidor'])
    if is_admin:
        role_label = 'Administrador'
    elif is_eac:
        role_label = 'Encargado de Atencion al Cliente'
    elif is_encargado_stock:
        role_label = 'Encargado de Stock'
    elif is_tecnico:
        role_label = 'Tecnico'
    elif is_repartidor:
        role_label = 'Repartidor'
    else:
        role_label = 'Usuario'
    return {
        'is_admin': is_admin,
        'is_eac': is_eac,
        'is_encargado_stock': is_encargado_stock,
        'is_tecnico': is_tecnico,
        'is_repartidor': is_repartidor,
        'role_label': role_label,
    }


def _stock_status(quantity):
    if quantity <= 0:
        return 'status-critical'
    if quantity <= 5:
        return 'status-low'
    return 'status-ok'


def _descontar_stock_pedido(pedido, usuario):
    """Descuenta stock de la camioneta al entregar un pedido.
    Solo descuenta si no se hizo ya (evita doble descuento)."""
    if not pedido.camioneta:
        return
    ya_descontado = StockMovimiento.objects.filter(
        pedido=pedido,
        tipo=StockMovimiento.Tipos.ENTREGA,
    ).exists()
    if ya_descontado:
        return
    for detalle in pedido.detalles.select_related('producto').all():
        stock, _ = StockCamioneta.objects.get_or_create(
            camioneta=pedido.camioneta,
            producto=detalle.producto,
            defaults={'cantidad_actual': 0},
        )
        stock.cantidad_actual -= detalle.cantidad
        stock.save(update_fields=['cantidad_actual'])
        StockMovimiento.objects.create(
            camioneta=pedido.camioneta,
            producto=detalle.producto,
            pedido=pedido,
            tipo=StockMovimiento.Tipos.ENTREGA,
            cantidad=detalle.cantidad,
            usuario=usuario,
        )


def _ensure_roles():
    for name in ROLE_NAMES:
        group, _ = Group.objects.get_or_create(name=name)


def landing(request):
    return render(request, 'landing.html')


@login_required
def home(request):
    ctx = _role_context(request.user)
    if ctx['is_admin'] or ctx['is_eac']:
        ctx['consultas_nuevas'] = ConsultaWeb.objects.filter(
            estado=ConsultaWeb.Estados.NUEVA,
        ).count()
    return render(request, 'home.html', ctx)


class UserForm(forms.ModelForm):
    dni = forms.CharField(label='DNI', max_length=20, required=False)
    estado = forms.ChoiceField(
        choices=DatosPersonales.ESTADO_CHOICES,
        required=True,
        label='Estado'
    )
    roles = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _ensure_roles()
        self.fields['roles'].queryset = Group.objects.all().order_by('name')
        
        # Set default estado for new users
        if not self.instance.pk:
            self.fields['estado'].initial = 'habilitado'

        if self.instance.pk:
            self.fields['roles'].initial = self.instance.groups.all()
            # Cargar datos desde DatosPersonales
            try:
                if hasattr(self.instance, 'datos_personales'):
                    datos = self.instance.datos_personales
                    self.fields['dni'].initial = datos.numero_documento
                    self.fields['estado'].initial = datos.estado
            except DatosPersonales.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Sincronizar is_active con estado
        estado = self.cleaned_data.get('estado')
        if estado == 'habilitado':
            user.is_active = True
        else:
            user.is_active = False

        if commit:
            user.save()
            user.groups.set(self.cleaned_data['roles'])
            
            # Guardar DatosPersonales (DNI)
            dni = self.cleaned_data.get('dni')
            
            datos, _ = DatosPersonales.objects.get_or_create(user=user)
            datos.numero_documento = dni
            datos.save(update_fields=['numero_documento'])
        else:
            self._pending_roles = self.cleaned_data['roles']
            self._pending_dni = self.cleaned_data.get('dni')
            self._pending_estado = self.cleaned_data.get('estado')
        return user


class UserCreateForm(UserForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta(UserForm.Meta):
        fields = UserForm.Meta.fields

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            raise forms.ValidationError('Las contrasenas no coinciden.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        # Estado por defecto para nuevos usuarios
        estado = self.cleaned_data.get('estado', 'habilitado')
        if estado == 'habilitado':
            user.is_active = True
        else:
            user.is_active = False

        if commit:
            user.save()
            user.groups.set(self.cleaned_data['roles'])
            
            # Guardar DatosPersonales
            dni = self.cleaned_data.get('dni')
            DatosPersonales.objects.update_or_create(
                user=user,
                defaults={
                    'numero_documento': dni,
                },
            )
        return user


class ClientForm(forms.ModelForm):
    barrio = forms.CharField(
        required=False,
        label='Barrio',
        widget=forms.TextInput(attrs={'list': 'barrios_list', 'autocomplete': 'off'})
    )
    zona = forms.ModelChoiceField(
        queryset=Zona.objects.none(),
        required=True,
        empty_label='Selecciona zona',
        label='Zona',
    )

    class Meta:
        model = Client
        fields = [
            'tipo_cliente',
            'name',
            'tipo_documento',
            'numero_documento',
            'telefono',
            'email',
            'direccion',
            'zona',
            'barrio',
            'referencias',
            'activo',
        ]
        widgets = {
            'referencias': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['zona'].queryset = Zona.objects.filter(active=True).order_by('nombre')
        if self.instance and self.instance.pk:
            if self.instance.barrio:
                self.fields['barrio'].initial = self.instance.barrio.nombre
            if self.instance.zona:
                self.fields['zona'].initial = self.instance.zona

    @staticmethod
    def _normalize_barrio(text):
        text = ' '.join((text or '').strip().split())
        if not text:
            return ''
        roman = {
            'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
            'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx',
        }
        words = []
        for raw in text.split(' '):
            lower = raw.lower()
            if lower in roman:
                words.append(lower.upper())
            else:
                words.append(raw.capitalize())
        return ' '.join(words)

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('name'):
            raise forms.ValidationError('El nombre es obligatorio.')
        if not cleaned.get('telefono'):
            raise forms.ValidationError('El telefono es obligatorio.')
        if not cleaned.get('numero_documento'):
            raise forms.ValidationError('El numero de documento es obligatorio.')
        zona = cleaned.get('zona')
        if not zona:
            raise forms.ValidationError('La zona es obligatoria.')
        barrio_text = self._normalize_barrio(cleaned.get('barrio'))
        if barrio_text:
            barrio = Barrio.objects.filter(nombre__iexact=barrio_text, zona=zona).first()
            if not barrio:
                barrio = Barrio.objects.create(nombre=barrio_text, zona=zona, active=True)
            cleaned['barrio'] = barrio
        else:
            cleaned['barrio'] = None
        return cleaned


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            raise forms.ValidationError('Las contrasenas no coinciden.')
        return cleaned


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'forma_pago']


class PedidoCreateForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Client.objects.all().order_by('name'))
    producto = forms.ModelChoiceField(queryset=Producto.objects.filter(active=True).order_by('nombre'))
    cantidad = forms.IntegerField(min_value=1)
    precio_unitario = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    forma_pago = forms.ChoiceField(choices=Pedido.FormasPago.choices, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['precio_unitario'].widget.attrs['readonly'] = True
        self.fields['producto'].queryset = Producto.objects.filter(active=True).order_by('nombre')
        self.fields['producto'].label_from_instance = lambda obj: f'{obj.nombre} - ${obj.precio}'
        producto_inicial = None
        if self.is_bound:
            producto_id = self.data.get('producto')
            if producto_id:
                producto_inicial = self.fields['producto'].queryset.filter(pk=producto_id).first()
        elif self.fields['producto'].queryset.exists():
            producto_inicial = self.fields['producto'].queryset.first()
        if producto_inicial:
            self.fields['precio_unitario'].initial = producto_inicial.precio

    def clean(self):
        cleaned = super().clean()
        producto = cleaned.get('producto')
        if producto:
            cleaned['precio_unitario'] = producto.precio
        return cleaned


class PedidoAssignForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['camioneta']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['camioneta'].queryset = Camioneta.objects.filter(active=True).order_by('nombre')


class PedidoStatusForm(forms.Form):
    estado = forms.ChoiceField(choices=Pedido.Estados.choices)
    motivo = forms.CharField(required=False, max_length=200)


class PedidoPagoForm(forms.Form):
    pago_monto = forms.DecimalField(max_digits=10, decimal_places=2)
    forma_pago = forms.ChoiceField(choices=Pedido.FormasPago.choices, required=False)
    pago_motivo = forms.CharField(max_length=200, required=False)

    def __init__(self, *args, **kwargs):
        self.pedido = kwargs.pop('pedido', None)
        super().__init__(*args, **kwargs)
        if self.pedido:
            self.fields['forma_pago'].initial = self.pedido.forma_pago
            if self.pedido.total:
                self.fields['pago_monto'].initial = self.pedido.total

    def clean(self):
        cleaned = super().clean()
        if self.pedido and self.pedido.estado == Pedido.Estados.DEVUELTO:
            if not cleaned.get('pago_motivo'):
                raise forms.ValidationError('Debes indicar el motivo del cobro para pedidos devueltos.')
        return cleaned


@login_required
@user_passes_test(_is_admin)
def admin_users(request):
    users = User.objects.select_related('datos_personales').order_by('username')
    
    total_users = users.count()
    active_users = users.filter(is_active=True).count()
    inactive_users = total_users - active_users
    
    context = {
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
    }
    context.update(_role_context(request.user))
    return render(request, 'admin_users.html', context)


@login_required
@user_passes_test(_is_admin)
def usuarios_baja(request):
    users = User.objects.filter(
        is_active=False
    ).select_related('datos_personales').order_by('username')

    context = {
        'users': users,
    }
    context.update(_role_context(request.user))
    return render(request, 'admin_users_baja.html', context)


@login_required
@user_passes_test(_is_admin)
def dar_baja_usuario(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save(update_fields=['is_active'])
    return redirect('admin_users')


@login_required
@user_passes_test(_is_admin)
def reactivar_usuario(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save(update_fields=['is_active'])

    return redirect('usuarios_baja')


@login_required
@user_passes_test(_is_admin)
def admin_user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('admin_users')
    else:
        form = UserCreateForm()
    context = {
        'form': form,
        'title': 'Crear usuario',
        'is_create': True,
        'role_names': ROLE_NAMES,
        'role_meta': ROLE_META,
        'target_user': None,
    }
    context.update(_role_context(request.user))
    return render(request, 'admin_user_form.html', context)


@login_required
@user_passes_test(_is_admin)
def admin_user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_users')
    else:
        form = UserForm(instance=user)
    context = {
        'form': form,
        'title': 'Editar usuario',
        'is_create': False,
        'role_names': ROLE_NAMES,
        'role_meta': ROLE_META,
        'target_user': user,
    }
    context.update(_role_context(request.user))
    return render(request, 'admin_user_form.html', context)


@login_required
@user_passes_test(_is_admin)
def admin_user_toggle(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    return redirect('admin_users')


@login_required
@user_passes_test(_is_admin)
def admin_user_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password1'])
            user.save(update_fields=['password'])
            return redirect('admin_users')
    else:
        form = PasswordResetForm()
    context = {'form': form, 'target_user': user}
    context.update(_role_context(request.user))
    return render(request, 'admin_user_password.html', context)





@login_required
@user_passes_test(_can_manage_clients)
def clients_list(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', 'all')

    base_queryset = Client.objects.all()
    total_clients = base_queryset.count()
    active_clients = base_queryset.filter(activo=True).count()
    inactive_clients = total_clients - active_clients

    clients = base_queryset
    if query:
        clients = clients.filter(
            Q(name__icontains=query)
            | Q(numero_documento__icontains=query)
            | Q(telefono__icontains=query)
            | Q(email__icontains=query)
            | Q(direccion__icontains=query)
            | Q(barrio__nombre__icontains=query)
            | Q(zona__nombre__icontains=query)
        )

    if status == 'active':
        clients = clients.filter(activo=True)
    elif status == 'inactive':
        clients = clients.filter(activo=False)

    clients = clients.order_by('name')

    context = {
        'clients': clients,
        'query': query,
        'status': status,
        'total_clients': total_clients,
        'active_clients': active_clients,
        'inactive_clients': inactive_clients,
    }
    context.update(_role_context(request.user))
    return render(request, 'clients_list.html', context)


@login_required
@user_passes_test(_can_manage_clients)
def clients_create(request):
    prefill = request.session.pop('consulta_prefill', None)
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            # Si viene de una consulta web, marcarla como convertida
            consulta_id = request.POST.get('consulta_id')
            if consulta_id:
                try:
                    consulta = ConsultaWeb.objects.get(pk=consulta_id)
                    consulta.estado = ConsultaWeb.Estados.CONVERTIDA
                    consulta.cliente_convertido = client
                    consulta.save(update_fields=['estado', 'cliente_convertido', 'updated_at'])
                except ConsultaWeb.DoesNotExist:
                    pass
            return redirect('clients_list')
    else:
        initial = {'activo': True}
        if prefill:
            initial.update({
                'name': prefill.get('name', ''),
                'email': prefill.get('email', ''),
                'telefono': prefill.get('telefono', ''),
                'referencias': prefill.get('referencias', ''),
            })
        form = ClientForm(initial=initial)
    context = {
        'form': form,
        'title': 'Nuevo cliente',
        'is_create': True,
        'consulta_id': prefill.get('consulta_id') if prefill else None,
        'barrios_autocomplete': list(
            Barrio.objects.filter(active=True, clientes__isnull=False)
            .select_related('zona')
            .order_by('nombre')
            .values('nombre', 'zona_id')
            .distinct()
        ),
    }
    context.update(_role_context(request.user))
    return render(request, 'clients_form.html', context)


@login_required
@user_passes_test(_can_manage_clients)
def clients_edit(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients_list')
    else:
        form = ClientForm(instance=client)
    context = {
        'form': form,
        'title': 'Editar cliente',
        'is_create': False,
        'client': client,
        'barrios_autocomplete': list(
            Barrio.objects.filter(active=True, clientes__isnull=False)
            .select_related('zona')
            .order_by('nombre')
            .values('nombre', 'zona_id')
            .distinct()
        ),
    }
    context.update(_role_context(request.user))
    return render(request, 'clients_form.html', context)


@login_required
@user_passes_test(_can_manage_clients)
def clients_toggle(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client.activo = not client.activo
    client.save(update_fields=['activo'])
    return redirect('clients_list')


@login_required
@user_passes_test(_can_manage_orders)
def orders_list(request):
    orders = Pedido.objects.select_related('cliente', 'camioneta', 'camioneta__repartidor')
    status = request.GET.get('status', 'all')
    cliente_id = request.GET.get('cliente', '').strip()
    camioneta_id = request.GET.get('camioneta', '').strip()
    date_from = request.GET.get('from', '').strip()
    date_to = request.GET.get('to', '').strip()

    if status != 'all':
        orders = orders.filter(estado=status)
    if cliente_id:
        orders = orders.filter(cliente_id=cliente_id)
    if camioneta_id:
        orders = orders.filter(camioneta_id=camioneta_id)
    if date_from:
        orders = orders.filter(created_at__date__gte=date_from)
    if date_to:
        orders = orders.filter(created_at__date__lte=date_to)
    total_orders = orders.count()
    assigned_orders = orders.filter(estado__in=[Pedido.Estados.ASIGNADO, Pedido.Estados.EN_REPARTO]).count()
    delivered_orders = orders.filter(estado=Pedido.Estados.ENTREGADO).count()
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'assigned_orders': assigned_orders,
        'delivered_orders': delivered_orders,
        'status': status,
        'cliente_id': cliente_id,
        'camioneta_id': camioneta_id,
        'date_from': date_from,
        'date_to': date_to,
        'clientes': Client.objects.all().order_by('name'),
        'estado_choices': Pedido.Estados.choices,
    }
    context.update(_role_context(request.user))
    return render(request, 'orders_list.html', context)


@login_required
@user_passes_test(_can_manage_orders)
def orders_create(request):
    if request.method == 'POST':
        form = PedidoCreateForm(request.POST)
        if form.is_valid():
            pedido = Pedido(
                cliente=form.cleaned_data['cliente'],
                forma_pago=form.cleaned_data.get('forma_pago', ''),
            )
            pedido.creado_por = request.user
            pedido.save()
            detalle = PedidoDetalle.objects.create(
                pedido=pedido,
                producto=form.cleaned_data['producto'],
                cantidad=form.cleaned_data['cantidad'],
                precio_unitario=form.cleaned_data['precio_unitario'],
            )
            pedido.total = detalle.subtotal()
            pedido.save(update_fields=['total'])
            PedidoEstado.objects.create(
                pedido=pedido,
                estado=Pedido.Estados.CREADO,
                usuario=request.user,
            )
            return redirect('orders_detail', order_id=pedido.id)
    else:
        form = PedidoCreateForm()
    context = {'form': form, 'title': 'Nuevo pedido'}
    context.update(_role_context(request.user))
    return render(request, 'orders_form.html', context)


@login_required
@user_passes_test(_can_manage_orders)
def orders_detail(request, order_id):
    pedido = get_object_or_404(Pedido, pk=order_id)
    historial = pedido.historial.select_related('usuario').all()
    detalles = pedido.detalles.select_related('producto').all()
    context = {'pedido': pedido, 'historial': historial, 'detalles': detalles}
    context.update(_role_context(request.user))
    return render(request, 'orders_detail.html', context)


@login_required
@user_passes_test(_can_manage_orders)
def orders_assign(request, order_id):
    pedido = get_object_or_404(Pedido, pk=order_id)
    if pedido.estado in (Pedido.Estados.ENTREGADO, Pedido.Estados.PAGADO):
        return redirect('orders_detail', order_id=pedido.id)
    suggested = Camioneta.objects.none()
    if pedido.cliente and pedido.cliente.zona_id:
        suggested = Camioneta.objects.filter(
            active=True,
           
            zonas=pedido.cliente.zona,
        ).distinct().order_by('nombre')
    all_camionetas = Camioneta.objects.filter(active=True).order_by('nombre')
    if suggested.exists():
        suggested_ids = list(suggested.values_list('id', flat=True))
        remaining = all_camionetas.exclude(id__in=suggested_ids)
        all_camionetas = list(suggested) + list(remaining)
    if request.method == 'POST':
        form = PedidoAssignForm(request.POST, instance=pedido)
        form.fields['camioneta'].queryset = Camioneta.objects.filter(active=True)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.estado = Pedido.Estados.ASIGNADO
            pedido.save()
            PedidoEstado.objects.create(
                pedido=pedido,
                estado=Pedido.Estados.ASIGNADO,
                usuario=request.user,
            )
            return redirect('orders_detail', order_id=pedido.id)
    else:
        form = PedidoAssignForm(instance=pedido)
        form.fields['camioneta'].queryset = Camioneta.objects.filter(active=True)
    if suggested.exists():
        form.fields['camioneta'].queryset = Camioneta.objects.filter(id__in=[c.id for c in all_camionetas])
        form.fields['camioneta'].choices = [(c.id, str(c)) for c in all_camionetas]
    context = {
        'form': form,
        'pedido': pedido,
        'suggested_camionetas': suggested,
        'cliente_zona': pedido.cliente.zona if pedido.cliente else None,
    }
    context.update(_role_context(request.user))
    return render(request, 'orders_assign.html', context)


@login_required
@user_passes_test(_can_manage_orders)
def orders_status(request, order_id):
    pedido = get_object_or_404(Pedido, pk=order_id)
    if pedido.estado in (Pedido.Estados.ENTREGADO, Pedido.Estados.PAGADO):
        return redirect('orders_detail', order_id=pedido.id)
    if request.method == 'POST':
        form = PedidoStatusForm(request.POST)
        if form.is_valid():
            estado = form.cleaned_data['estado']
            motivo = form.cleaned_data['motivo']
            pedido.estado = estado
            pedido.save(update_fields=['estado', 'updated_at'])
            PedidoEstado.objects.create(
                pedido=pedido,
                estado=estado,
                usuario=request.user,
                motivo=motivo,
            )
            if estado == Pedido.Estados.ENTREGADO:
                _descontar_stock_pedido(pedido, request.user)
            return redirect('orders_detail', order_id=pedido.id)
    else:
        form = PedidoStatusForm(initial={'estado': pedido.estado})
    context = {'form': form, 'pedido': pedido}
    context.update(_role_context(request.user))
    return render(request, 'orders_status.html', context)


@login_required
@user_passes_test(_can_manage_orders)
def orders_pay(request, order_id):
    pedido = get_object_or_404(Pedido, pk=order_id)
    if pedido.estado == Pedido.Estados.PAGADO:
        return redirect('orders_detail', order_id=pedido.id)
    if request.method == 'POST':
        form = PedidoPagoForm(request.POST, pedido=pedido)
        if form.is_valid():
            pedido.pago_monto = form.cleaned_data['pago_monto']
            pedido.forma_pago = form.cleaned_data.get('forma_pago', '')
            pedido.pago_motivo = form.cleaned_data.get('pago_motivo', '')
            pedido.pago_fecha = timezone.now()
            pedido.estado = Pedido.Estados.PAGADO
            pedido.save()
            PedidoEstado.objects.create(
                pedido=pedido,
                estado=Pedido.Estados.PAGADO,
                usuario=request.user,
                motivo=pedido.pago_motivo,
            )
            _descontar_stock_pedido(pedido, request.user)
            return redirect('orders_detail', order_id=pedido.id)
    else:
        form = PedidoPagoForm(pedido=pedido)
    context = {'form': form, 'pedido': pedido}
    context.update(_role_context(request.user))
    return render(request, 'orders_pay.html', context)


@login_required
@user_passes_test(_is_admin)
def roles_list(request):
    _ensure_roles()
    roles = Group.objects.all().order_by('name')
    context = {
        'roles': roles,
    }
    context.update(_role_context(request.user))
    return render(request, 'roles_list.html', context)





class CamionetaForm(forms.ModelForm):
    class Meta:
        model = Camioneta
        fields = ['nombre', 'patente', 'repartidor', 'estado', 'zonas', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['repartidor'].queryset = User.objects.filter(groups__name='Repartidor').order_by('username')
        self.fields['zonas'].queryset = Zona.objects.filter(active=True).order_by('nombre')
        self.fields['zonas'].widget = forms.CheckboxSelectMultiple()


@login_required
@user_passes_test(_is_admin)
def camionetas_list(request):
    camionetas = Camioneta.objects.select_related('repartidor').order_by('nombre')
    total_camionetas = camionetas.count()
    active_camionetas = camionetas.filter(active=True).count()
    inactive_camionetas = total_camionetas - active_camionetas
    context = {
        'camionetas': camionetas,
        'total_camionetas': total_camionetas,
        'active_camionetas': active_camionetas,
        'inactive_camionetas': inactive_camionetas,
    }
    context.update(_role_context(request.user))
    return render(request, 'camionetas_list.html', context)


@login_required
@user_passes_test(_is_admin)
def camionetas_create(request):
    if request.method == 'POST':
        form = CamionetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('camionetas_list')
    else:
        form = CamionetaForm(initial={'active': True})
    context = {'form': form, 'title': 'Nueva camioneta', 'is_create': True}
    context.update(_role_context(request.user))
    return render(request, 'camionetas_form.html', context)


@login_required
@user_passes_test(_is_admin)
def camionetas_edit(request, camioneta_id):
    camioneta = get_object_or_404(Camioneta, pk=camioneta_id)
    if request.method == 'POST':
        form = CamionetaForm(request.POST, instance=camioneta)
        if form.is_valid():
            form.save()
            return redirect('camionetas_list')
    else:
        form = CamionetaForm(instance=camioneta)
    context = {'form': form, 'title': 'Editar camioneta', 'is_create': False, 'camioneta': camioneta}
    context.update(_role_context(request.user))
    return render(request, 'camionetas_form.html', context)


@login_required
@user_passes_test(_is_admin)
def camionetas_toggle(request, camioneta_id):
    camioneta = get_object_or_404(Camioneta, pk=camioneta_id)
    camioneta.active = not camioneta.active
    camioneta.save(update_fields=['active'])
    return redirect('camionetas_list')


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'capacidad_litros',
            'tipo_envase',
            'retornable',
            'max_por_camioneta',
            'unidad_venta',
            'requiere_envase',
            'deposito_envase',
            'precio',
            'active',
        ]

    def clean(self):
        cleaned = super().clean()
        tipo_envase = cleaned.get('tipo_envase')
        retornable = cleaned.get('retornable')
        if retornable and tipo_envase not in [Producto.TipoEnvase.SIFON, Producto.TipoEnvase.BIDON]:
            raise forms.ValidationError('Solo Sifon o Bidon pueden ser retornables.')
        return cleaned


@login_required
@user_passes_test(_is_admin)
def productos_list(request):
    productos = Producto.objects.order_by('nombre')
    total_productos = productos.count()
    activos = productos.filter(active=True).count()
    inactivos = total_productos - activos
    context = {
        'productos': productos,
        'total_productos': total_productos,
        'activos': activos,
        'inactivos': inactivos,
    }
    context.update(_role_context(request.user))
    return render(request, 'productos_list.html', context)


@login_required
@user_passes_test(_is_admin)
def productos_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos_list')
    else:
        form = ProductoForm(initial={'active': True})
    context = {'form': form, 'title': 'Nuevo producto'}
    context.update(_role_context(request.user))
    return render(request, 'productos_form.html', context)


@login_required
@user_passes_test(_is_admin)
def productos_edit(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos_list')
    else:
        form = ProductoForm(instance=producto)
    context = {'form': form, 'title': 'Editar producto', 'producto': producto}
    context.update(_role_context(request.user))
    return render(request, 'productos_form.html', context)


@login_required
@user_passes_test(_is_admin)
def productos_toggle(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    producto.active = not producto.active
    producto.save(update_fields=['active'])
    return redirect('productos_list')


class BarrioForm(forms.ModelForm):
    class Meta:
        model = Barrio
        fields = ['nombre', 'zona', 'active']


@login_required
@user_passes_test(_is_admin)
def barrios_list(request):
    query = (request.GET.get('q') or '').strip()
    barrios = Barrio.objects.select_related('zona').order_by('nombre')
    if query:
        barrios = barrios.filter(
            Q(nombre__icontains=query)
            | Q(zona__nombre__icontains=query)
        )
    total = barrios.count()
    activos = barrios.filter(active=True).count()
    inactivos = total - activos
    context = {
        'barrios': barrios,
        'query': query,
        'total': total,
        'activos': activos,
        'inactivos': inactivos,
    }
    context.update(_role_context(request.user))
    return render(request, 'barrios_list.html', context)


@login_required
@user_passes_test(_is_admin)
def barrios_create(request):
    if request.method == 'POST':
        form = BarrioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('barrios_list')
    else:
        form = BarrioForm(initial={'active': True})
    context = {'form': form, 'title': 'Nuevo barrio'}
    context.update(_role_context(request.user))
    return render(request, 'barrios_form.html', context)


@login_required
@user_passes_test(_is_admin)
def barrios_edit(request, barrio_id):
    barrio = get_object_or_404(Barrio, pk=barrio_id)
    if request.method == 'POST':
        form = BarrioForm(request.POST, instance=barrio)
        if form.is_valid():
            form.save()
            return redirect('barrios_list')
    else:
        form = BarrioForm(instance=barrio)
    context = {'form': form, 'title': 'Editar barrio', 'barrio': barrio}
    context.update(_role_context(request.user))
    return render(request, 'barrios_form.html', context)


@login_required
@user_passes_test(_is_admin)
def barrios_toggle(request, barrio_id):
    barrio = get_object_or_404(Barrio, pk=barrio_id)
    barrio.active = not barrio.active
    barrio.save(update_fields=['active'])
    return redirect('barrios_list')


@login_required
@user_passes_test(_can_manage_logistics)
def logistica_panel(request):
    camionetas = Camioneta.objects.select_related('repartidor').order_by('nombre')
    pedidos = Pedido.objects.select_related('camioneta').all()
    resumen = []
    for cam in camionetas:
        cam_pedidos = pedidos.filter(camioneta=cam)
        resumen.append(
            {
                'camioneta': cam,
                'cantidad': cam_pedidos.count(),
                'en_ruta': cam_pedidos.filter(estado=Pedido.Estados.EN_REPARTO).count(),
            }
        )
    context = {'resumen': resumen}
    context.update(_role_context(request.user))
    return render(request, 'logistica_panel.html', context)


@login_required
@user_passes_test(_can_manage_orders)
def mis_entregas(request):
    camioneta = _get_user_camioneta(request.user)
    pedidos = Pedido.objects.none()
    historial = Pedido.objects.none()
    if camioneta:
        pedidos = Pedido.objects.filter(
            camioneta=camioneta,
            estado__in=[Pedido.Estados.ASIGNADO, Pedido.Estados.EN_REPARTO],
        ).order_by('created_at')
        cutoff = timezone.now() - timedelta(days=7)
        historial = Pedido.objects.filter(
            camioneta=camioneta,
            created_at__gte=cutoff,
            estado__in=[Pedido.Estados.ENTREGADO, Pedido.Estados.DEVUELTO, Pedido.Estados.PAGADO],
        ).order_by('-created_at')
    context = {'camioneta': camioneta, 'pedidos': pedidos, 'historial': historial}
    context.update(_role_context(request.user))
    return render(request, 'mis_entregas.html', context)


@login_required
@user_passes_test(_can_manage_orders)
def entrega_operacion(request, order_id):
    pedido = get_object_or_404(Pedido, pk=order_id)
    detalles = pedido.detalles.select_related('producto').all()
    if request.method == 'POST':
        motivo = request.POST.get('motivo', '').strip()
        operaciones = []
        errores = []
        total_devuelto = 0

        for detalle in detalles:
            try:
                entregado = int(request.POST.get(f'entregado_{detalle.id}', '0') or 0)
                devuelto = int(request.POST.get(f'devuelto_{detalle.id}', '0') or 0)
            except ValueError:
                entregado = 0
                devuelto = 0
            if entregado < 0 or devuelto < 0:
                errores.append(f'Cantidad invalida para {detalle.producto.nombre}.')
                continue
            if entregado == 0 and devuelto == 0:
                continue
            if entregado + devuelto > detalle.cantidad:
                errores.append(f'La suma supera lo pedido en {detalle.producto.nombre}.')
                continue
            operaciones.append((detalle, entregado, devuelto))
            total_devuelto += devuelto

        if not operaciones:
            errores.append('Ingresa al menos una cantidad entregada o devuelta.')

        camioneta = pedido.camioneta
        if camioneta:
            for detalle, entregado, _ in operaciones:
                if entregado <= 0:
                    continue
                stock = StockCamioneta.objects.filter(camioneta=camioneta, producto=detalle.producto).first()
                if not stock or stock.cantidad_actual < entregado:
                    errores.append(f'Stock insuficiente en {detalle.producto.nombre}.')

        if errores:
            context = {'pedido': pedido, 'detalles': detalles, 'errores': errores}
            context.update(_role_context(request.user))
            return render(request, 'entrega_operacion.html', context)

        estado = Pedido.Estados.ENTREGADO if total_devuelto == 0 else Pedido.Estados.DEVUELTO
        pedido.estado = estado
        pedido.save(update_fields=['estado'])
        PedidoEstado.objects.create(pedido=pedido, estado=estado, usuario=request.user, motivo=motivo)

        if camioneta:
            for detalle, entregado, devuelto in operaciones:
                stock, _ = StockCamioneta.objects.get_or_create(camioneta=camioneta, producto=detalle.producto)
                if entregado:
                    stock.cantidad_actual -= entregado
                    StockMovimiento.objects.create(
                        camioneta=camioneta,
                        producto=detalle.producto,
                        pedido=pedido,
                        tipo=StockMovimiento.Tipos.ENTREGA,
                        cantidad=entregado,
                        usuario=request.user,
                    )
                if devuelto:
                    stock.cantidad_actual += devuelto
                    StockMovimiento.objects.create(
                        camioneta=camioneta,
                        producto=detalle.producto,
                        pedido=pedido,
                        tipo=StockMovimiento.Tipos.DEVOLUCION,
                        cantidad=devuelto,
                        usuario=request.user,
                    )
                stock.save(update_fields=['cantidad_actual'])
        return redirect('mis_entregas')
    context = {'pedido': pedido, 'detalles': detalles}
    context.update(_role_context(request.user))
    return render(request, 'entrega_operacion.html', context)


@login_required
@user_passes_test(_can_manage_orders)
def mi_stock(request):
    camioneta = _get_user_camioneta(request.user)
    stock = StockCamioneta.objects.none()
    if camioneta:
        stock = camioneta.stock.select_related('producto').all()
    context = {'camioneta': camioneta, 'stock': stock}
    context.update(_role_context(request.user))
    return render(request, 'mi_stock.html', context)


@login_required
@user_passes_test(_can_manage_orders)
def mi_camioneta(request):
    camioneta = _get_user_camioneta(request.user)
    pedidos = Pedido.objects.none()
    if camioneta:
        cutoff = timezone.now() - timedelta(days=7)
        pedidos = Pedido.objects.filter(camioneta=camioneta, created_at__gte=cutoff).order_by('-created_at')
    context = {'camioneta': camioneta, 'pedidos': pedidos}
    context.update(_role_context(request.user))
    return render(request, 'mi_camioneta.html', context)


@login_required
@user_passes_test(_can_manage_stock)
def stock_general(request):
    deposito = Deposito.objects.filter(activo=True).order_by('id').first()
    camionetas = Camioneta.objects.select_related('repartidor').filter(active=True).order_by('nombre')
    deposito_stock_qs = StockDeposito.objects.none()
    if deposito:
        deposito_stock_qs = deposito.stocks.select_related('producto').order_by('producto__nombre')

    deposito_stock = [
        {
            'item': item,
            'status': _stock_status(item.cantidad_actual),
        }
        for item in deposito_stock_qs
    ]

    stock_por_camioneta = {}
    stock_items = (
        StockCamioneta.objects.select_related('camioneta', 'producto')
        .filter(camioneta__in=camionetas)
        .order_by('camioneta__nombre', 'producto__nombre')
    )
    for item in stock_items:
        stock_por_camioneta.setdefault(item.camioneta_id, []).append(item)

    camioneta_cards = []
    for camioneta in camionetas:
        items = stock_por_camioneta.get(camioneta.id, [])
        total_unidades = sum(item.cantidad_actual for item in items)
        camioneta_cards.append(
            {
                'camioneta': camioneta,
                'count': len(items),
                'total_unidades': total_unidades,
                'status': _stock_status(total_unidades),
            }
        )

    puede_editar = _can_manage_stock(request.user)

    context = {
        'deposito': deposito,
        'deposito_stock': deposito_stock,
        'camioneta_cards': camioneta_cards,
        'puede_editar': puede_editar,
    }
    context.update(_role_context(request.user))
    return render(request, 'stock_general.html', context)


@login_required
@user_passes_test(_can_manage_stock)
def stock_cargar(request, camioneta_id):
    camioneta = get_object_or_404(Camioneta, pk=camioneta_id)

    deposito = Deposito.objects.filter(activo=True).order_by('id').first()
    if not deposito:
        return redirect('stock_general')

    if request.method != 'POST':
        return redirect('stock_general')

    deposito_stock = deposito.stocks.select_related('producto')
    cambios = []
    for item in deposito_stock:
        key = f'qty_{item.producto_id}'
        try:
            qty = int(request.POST.get(key, '0') or 0)
        except ValueError:
            qty = 0
        if qty <= 0:
            continue
        if qty > item.cantidad_actual:
            continue
        cambios.append((item, qty))

    for item, qty in cambios:
        item.cantidad_actual -= qty
        item.save(update_fields=['cantidad_actual'])
        destino, _ = StockCamioneta.objects.get_or_create(
            camioneta=camioneta,
            producto=item.producto,
            defaults={'cantidad_actual': 0},
        )
        destino.cantidad_actual += qty
        destino.save(update_fields=['cantidad_actual'])
        StockMovimiento.objects.create(
            camioneta=camioneta,
            producto=item.producto,
            tipo=StockMovimiento.Tipos.AJUSTE,
            cantidad=qty,
            usuario=request.user,
        )
    return redirect('stock_general')


@login_required
@user_passes_test(_can_manage_stock)
def stock_camioneta(request, camioneta_id):
    camioneta = get_object_or_404(Camioneta, pk=camioneta_id)
    stock = StockCamioneta.objects.filter(camioneta=camioneta).select_related('producto')
    context = {'camioneta': camioneta, 'stock': stock}
    context.update(_role_context(request.user))
    return render(request, 'stock_camioneta.html', context)


@login_required
@user_passes_test(_can_manage_stock)
def stock_deposito_cargar(request):
    deposito = Deposito.objects.filter(activo=True).order_by('id').first()
    if not deposito:
        return redirect('stock_general')

    productos = Producto.objects.filter(active=True).order_by('nombre')
    deposito_stock = deposito.stocks.select_related('producto').order_by('producto__nombre')

    productos_en_deposito = {s.producto_id for s in deposito_stock}
    productos_sin_stock = [p for p in productos if p.id not in productos_en_deposito]

    if request.method == 'POST':
        for producto in productos:
            key = f'qty_{producto.id}'
            try:
                qty = int(request.POST.get(key, '0') or 0)
            except ValueError:
                qty = 0
            if qty <= 0:
                continue
            stock_item, created = StockDeposito.objects.get_or_create(
                deposito=deposito,
                producto=producto,
                defaults={'cantidad_actual': 0},
            )
            stock_item.cantidad_actual += qty
            stock_item.save(update_fields=['cantidad_actual'])
        return redirect('stock_general')

    deposito_stock_display = [
        {
            'item': item,
            'status': _stock_status(item.cantidad_actual),
        }
        for item in deposito_stock
    ]

    context = {
        'deposito': deposito,
        'deposito_stock': deposito_stock_display,
        'productos_sin_stock': productos_sin_stock,
    }
    context.update(_role_context(request.user))
    return render(request, 'stock_deposito_cargar.html', context)


@login_required
@user_passes_test(_can_manage_stock)
def stock_movimientos(request):
    movimientos = StockMovimiento.objects.select_related(
        'camioneta', 'producto', 'pedido', 'usuario',
    ).order_by('-created_at')

    tipo = request.GET.get('tipo', '').strip()
    camioneta_id = request.GET.get('camioneta', '').strip()
    usuario_id = request.GET.get('usuario', '').strip()
    producto_id = request.GET.get('producto', '').strip()
    date_from = request.GET.get('from', '').strip()
    date_to = request.GET.get('to', '').strip()

    if tipo:
        movimientos = movimientos.filter(tipo=tipo)
    if camioneta_id:
        movimientos = movimientos.filter(camioneta_id=camioneta_id)
    if usuario_id:
        movimientos = movimientos.filter(usuario_id=usuario_id)
    if producto_id:
        movimientos = movimientos.filter(producto_id=producto_id)
    if date_from:
        movimientos = movimientos.filter(created_at__date__gte=date_from)
    if date_to:
        movimientos = movimientos.filter(created_at__date__lte=date_to)

    total_movimientos = movimientos.count()

    context = {
        'movimientos': movimientos[:200],
        'total_movimientos': total_movimientos,
        'tipo': tipo,
        'camioneta_id': camioneta_id,
        'usuario_id': usuario_id,
        'producto_id': producto_id,
        'date_from': date_from,
        'date_to': date_to,
        'tipo_choices': StockMovimiento.Tipos.choices,
        'camionetas': Camioneta.objects.filter(active=True).order_by('nombre'),
        'usuarios': User.objects.filter(is_active=True).order_by('username'),
        'productos': Producto.objects.filter(active=True).order_by('nombre'),
    }
    context.update(_role_context(request.user))
    return render(request, 'stock_movimientos.html', context)


# ─────────────────────────────────────────────────────────
#  CONSULTAS WEB
# ─────────────────────────────────────────────────────────

@csrf_exempt
@require_POST
def contacto_submit(request):
    """Endpoint público que recibe el formulario de contacto de la landing."""
    import json
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    nombre = (data.get('nombre') or '').strip()
    email = (data.get('email') or '').strip()
    telefono = (data.get('telefono') or '').strip()
    mensaje = (data.get('mensaje') or '').strip()

    if not nombre or not email or not telefono or not mensaje:
        return JsonResponse(
            {'ok': False, 'error': 'Todos los campos son obligatorios.'},
            status=400,
        )

    ConsultaWeb.objects.create(
        nombre=nombre,
        email=email,
        telefono=telefono,
        mensaje=mensaje,
    )
    return JsonResponse({'ok': True, 'message': '¡Consulta enviada con éxito!'})


@login_required
@user_passes_test(_can_manage_clients)
def consultas_list(request):
    estado = request.GET.get('estado', 'all')
    q = request.GET.get('q', '').strip()

    consultas = ConsultaWeb.objects.all()
    total = consultas.count()
    nuevas = consultas.filter(estado=ConsultaWeb.Estados.NUEVA).count()

    if estado != 'all':
        consultas = consultas.filter(estado=estado)
    if q:
        consultas = consultas.filter(
            Q(nombre__icontains=q)
            | Q(email__icontains=q)
            | Q(telefono__icontains=q)
            | Q(mensaje__icontains=q)
        )

    context = {
        'consultas': consultas[:200],
        'total': total,
        'nuevas': nuevas,
        'estado': estado,
        'query': q,
        'estado_choices': ConsultaWeb.Estados.choices,
    }
    context.update(_role_context(request.user))
    return render(request, 'consultas_list.html', context)


@login_required
@user_passes_test(_can_manage_clients)
def consulta_detail(request, consulta_id):
    consulta = get_object_or_404(ConsultaWeb, pk=consulta_id)
    # Marcar como leída automáticamente si es nueva
    if consulta.estado == ConsultaWeb.Estados.NUEVA:
        consulta.estado = ConsultaWeb.Estados.LEIDA
        consulta.save(update_fields=['estado'])

    if request.method == 'POST' and 'notas_internas' in request.POST:
        consulta.notas_internas = request.POST.get('notas_internas', '')
        consulta.save(update_fields=['notas_internas'])
        return redirect('consulta_detail', consulta_id=consulta.pk)

    context = {
        'consulta': consulta,
        'estado_choices': ConsultaWeb.Estados.choices,
    }
    context.update(_role_context(request.user))
    return render(request, 'consulta_detail.html', context)


@login_required
@user_passes_test(_can_manage_clients)
def consulta_estado(request, consulta_id):
    consulta = get_object_or_404(ConsultaWeb, pk=consulta_id)
    nuevo_estado = request.POST.get('estado', '')
    if nuevo_estado in dict(ConsultaWeb.Estados.choices):
        consulta.estado = nuevo_estado
        consulta.save(update_fields=['estado', 'updated_at'])
    return redirect('consulta_detail', consulta_id=consulta.pk)


@login_required
@user_passes_test(_can_manage_clients)
def consulta_convertir(request, consulta_id):
    """Redirige al formulario de alta de cliente con los datos pre‑llenados."""
    consulta = get_object_or_404(ConsultaWeb, pk=consulta_id)
    # Store in session so the create view can read them
    request.session['consulta_prefill'] = {
        'consulta_id': consulta.pk,
        'name': consulta.nombre,
        'email': consulta.email,
        'telefono': consulta.telefono,
        'referencias': consulta.mensaje,
    }
    return redirect('clients_create')
