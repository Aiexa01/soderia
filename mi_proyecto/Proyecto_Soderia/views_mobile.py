from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import timedelta

from .models import Pedido, Camioneta, StockCamioneta, StockMovimiento, PedidoEstado, ConsultaWeb, Client, Producto
from .views import _get_user_camioneta, _can_manage_orders

def is_eac(user):
    return user.is_authenticated and user.groups.filter(name='Encargado de Atencion al Cliente').exists()

def is_repartidor(user):
    return user.is_authenticated and user.groups.filter(name__in=['Repartidor', 'Repartidor / Instalador']).exists()

def is_mobile_user(user):
    return is_repartidor(user) or is_eac(user)

def mobile_login(request):
    if request.user.is_authenticated:
        return redirect('mobile_home')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('mobile_home')
        else:
            return render(request, 'mobile/login.html', {'error': 'Usuario o contraseña incorrectos'})
            
    return render(request, 'mobile/login.html')

def mobile_logout(request):
    logout(request)
    return redirect('mobile_login')

@login_required(login_url='mobile_login')
@user_passes_test(is_mobile_user, login_url='mobile_login')
def mobile_home(request):
    if is_eac(request.user):
        hoy = timezone.now().date()
        nuevas = ConsultaWeb.objects.filter(estado=ConsultaWeb.Estados.NUEVA).count()
        pedidos_hoy = Pedido.objects.filter(created_at__date=hoy).count()
        return render(request, 'mobile/home_eac.html', {
            'nuevas': nuevas,
            'pedidos_hoy': pedidos_hoy,
        })
        
    camioneta = _get_user_camioneta(request.user)
    context = {
        'camioneta': camioneta,
        'pendientes': 0,
        'completadas': 0,
        'devueltas': 0
    }
    
    if camioneta:
        hoy = timezone.now().date()
        context['pendientes'] = Pedido.objects.filter(
            camioneta=camioneta,
            estado__in=[Pedido.Estados.ASIGNADO, Pedido.Estados.EN_REPARTO]
        ).count()
        context['completadas'] = Pedido.objects.filter(
            camioneta=camioneta,
            estado__in=[Pedido.Estados.ENTREGADO, Pedido.Estados.PAGADO],
            updated_at__date=hoy
        ).count()
        context['devueltas'] = Pedido.objects.filter(
            camioneta=camioneta,
            estado=Pedido.Estados.DEVUELTO,
            updated_at__date=hoy
        ).count()

    return render(request, 'mobile/home.html', context)

@login_required(login_url='mobile_login')
@user_passes_test(is_repartidor, login_url='mobile_login')
def mobile_entregas(request):
    camioneta = _get_user_camioneta(request.user)
    pedidos_pendientes = []
    
    if camioneta:
        pedidos_pendientes = Pedido.objects.filter(
            camioneta=camioneta,
            estado__in=[Pedido.Estados.ASIGNADO, Pedido.Estados.EN_REPARTO]
        ).select_related('cliente', 'cliente__barrio').order_by('cliente__barrio__nombre', 'created_at')
        
    return render(request, 'mobile/entregas.html', {
        'pedidos': pedidos_pendientes,
        'camioneta': camioneta
    })

@login_required(login_url='mobile_login')
@user_passes_test(is_repartidor, login_url='mobile_login')
def mobile_entrega_operar(request, order_id):
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
                errores.append(f'Cantidad inválida para {detalle.producto.nombre}.')
                continue
            if entregado == 0 and devuelto == 0:
                continue
            if entregado + devuelto > detalle.cantidad:
                errores.append(f'La suma supera lo pedido en {detalle.producto.nombre}.')
                continue
                
            operaciones.append((detalle, entregado, devuelto))
            total_devuelto += devuelto

        if not operaciones:
            errores.append('Ingresá al menos una cantidad entregada o devuelta.')

        camioneta = pedido.camioneta
        if camioneta:
            for detalle, entregado, _ in operaciones:
                if entregado <= 0:
                    continue
                stock = StockCamioneta.objects.filter(camioneta=camioneta, producto=detalle.producto).first()
                if not stock or stock.cantidad_actual < entregado:
                    errores.append(f'Stock insuficiente en {detalle.producto.nombre}.')

        if errores:
            return render(request, 'mobile/entrega_operar.html', {'pedido': pedido, 'detalles': detalles, 'errores': errores})

        estado = Pedido.Estados.ENTREGADO if total_devuelto == 0 else Pedido.Estados.DEVUELTO
        
        # Payment handling
        cobrado_efectivo = request.POST.get('cobrado_efectivo')
        if cobrado_efectivo and cobrado_efectivo.strip():
            try:
                monto = float(cobrado_efectivo)
                if monto > 0:
                    pedido.pago_monto = monto
                    pedido.forma_pago = Pedido.FormasPago.EFECTIVO
                    pedido.pago_fecha = timezone.now()
                    estado = Pedido.Estados.PAGADO
            except ValueError:
                pass

        pedido.estado = estado
        pedido.save(update_fields=['estado', 'updated_at', 'pago_monto', 'forma_pago', 'pago_fecha'])
        PedidoEstado.objects.create(pedido=pedido, estado=estado, usuario=request.user, motivo=motivo)

        if camioneta:
            for detalle, entregado, devuelto in operaciones:
                stock, _ = StockCamioneta.objects.get_or_create(camioneta=camioneta, producto=detalle.producto)
                if entregado:
                    stock.cantidad_actual -= entregado
                    StockMovimiento.objects.create(
                        camioneta=camioneta, producto=detalle.producto, pedido=pedido,
                        tipo=StockMovimiento.Tipos.ENTREGA, cantidad=entregado, usuario=request.user
                    )
                if devuelto:
                    stock.cantidad_actual += devuelto
                    StockMovimiento.objects.create(
                        camioneta=camioneta, producto=detalle.producto, pedido=pedido,
                        tipo=StockMovimiento.Tipos.DEVOLUCION, cantidad=devuelto, usuario=request.user
                    )
                stock.save(update_fields=['cantidad_actual'])
                
        return redirect('mobile_entregas')

    return render(request, 'mobile/entrega_operar.html', {'pedido': pedido, 'detalles': detalles})


@login_required(login_url='mobile_login')
@user_passes_test(is_repartidor, login_url='mobile_login')
def mobile_entrega_rapida(request, order_id):
    """Mark an order as fully delivered and paid in cash."""
    pedido = get_object_or_404(Pedido, pk=order_id)
    if request.method == 'POST':
        camioneta = pedido.camioneta
        detalles = pedido.detalles.select_related('producto').all()
        
        errores = []
        if camioneta:
            for detalle in detalles:
                stock = StockCamioneta.objects.filter(camioneta=camioneta, producto=detalle.producto).first()
                if not stock or stock.cantidad_actual < detalle.cantidad:
                    errores.append(f'Stock insuficiente en {detalle.producto.nombre}.')
                    
        if errores:
            # We can't do fast complete without stock
            return redirect('mobile_entrega_operar', order_id=pedido.id)

        # Apply stock discounts
        if camioneta:
            for detalle in detalles:
                stock = StockCamioneta.objects.get(camioneta=camioneta, producto=detalle.producto)
                stock.cantidad_actual -= detalle.cantidad
                stock.save(update_fields=['cantidad_actual'])
                StockMovimiento.objects.create(
                    camioneta=camioneta, producto=detalle.producto, pedido=pedido,
                    tipo=StockMovimiento.Tipos.ENTREGA, cantidad=detalle.cantidad, usuario=request.user
                )

        # Mark as paid in cash fully
        pedido.estado = Pedido.Estados.PAGADO
        pedido.pago_monto = pedido.total
        pedido.forma_pago = Pedido.FormasPago.EFECTIVO
        pedido.pago_fecha = timezone.now()
        pedido.save(update_fields=['estado', 'updated_at', 'pago_monto', 'forma_pago', 'pago_fecha'])
        
        PedidoEstado.objects.create(pedido=pedido, estado=Pedido.Estados.ENTREGADO, usuario=request.user, motivo='Entrega Rápida')
        PedidoEstado.objects.create(pedido=pedido, estado=Pedido.Estados.PAGADO, usuario=request.user, motivo='Cobro Rápido Efectivo')
        
    return redirect('mobile_entregas')


@login_required(login_url='mobile_login')
@user_passes_test(is_repartidor, login_url='mobile_login')
def mobile_stock(request):
    camioneta = _get_user_camioneta(request.user)
    stock = []
    if camioneta:
        stock = camioneta.stock.select_related('producto').all()
    return render(request, 'mobile/stock.html', {'stock': stock, 'camioneta': camioneta})


@login_required(login_url='mobile_login')
@user_passes_test(is_repartidor, login_url='mobile_login')
def mobile_camioneta(request):
    camioneta = _get_user_camioneta(request.user)
    return render(request, 'mobile/camioneta.html', {'camioneta': camioneta})

# ----------------- EAC VIEWS -----------------

@login_required(login_url='mobile_login')
@user_passes_test(is_eac, login_url='mobile_login')
def mobile_consultas_list(request):
    consultas = ConsultaWeb.objects.all().order_by('-created_at')
    # Filter only recent or pending ones for speed
    consultas = consultas.filter(estado__in=[ConsultaWeb.Estados.NUEVA, ConsultaWeb.Estados.LEIDA, ConsultaWeb.Estados.CONTACTADA])
    return render(request, 'mobile/consultas.html', {'consultas': consultas})

@login_required(login_url='mobile_login')
@user_passes_test(is_eac, login_url='mobile_login')
def mobile_consulta_detail(request, consulta_id):
    consulta = get_object_or_404(ConsultaWeb, pk=consulta_id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in [choice[0] for choice in ConsultaWeb.Estados.choices]:
            consulta.estado = nuevo_estado
            consulta.save()
            return redirect('mobile_consultas_list')
    
    # Mark as read if new
    if consulta.estado == ConsultaWeb.Estados.NUEVA:
        consulta.estado = ConsultaWeb.Estados.LEIDA
        consulta.save()
        
    return render(request, 'mobile/consulta_detalle.html', {'consulta': consulta})

@login_required(login_url='mobile_login')
@user_passes_test(is_eac, login_url='mobile_login')
def mobile_pedidos_list(request):
    pedidos = Pedido.objects.select_related('cliente').all()[:30] # Last 30 orders
    return render(request, 'mobile/pedidos.html', {'pedidos': pedidos})

@login_required(login_url='mobile_login')
@user_passes_test(is_eac, login_url='mobile_login')
def mobile_pedido_crear(request):
    clientes = Client.objects.filter(activo=True).order_by('name')
    productos = Producto.objects.filter(active=True).order_by('nombre')
    
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        producto_id = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad', 1))
        
        if cliente_id and producto_id and cantidad > 0:
            cliente = get_object_or_404(Client, pk=cliente_id)
            producto = get_object_or_404(Producto, pk=producto_id)
            
            pedido = Pedido.objects.create(
                cliente=cliente,
                estado=Pedido.Estados.CREADO,
                total=producto.precio * cantidad,
                creado_por=request.user
            )
            # Add detail
            pedido.detalles.create(
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )
            return redirect('mobile_pedidos_list')
            
    return render(request, 'mobile/pedido_crear.html', {
        'clientes': clientes,
        'productos': productos
    })
