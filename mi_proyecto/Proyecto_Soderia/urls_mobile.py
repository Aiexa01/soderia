from django.urls import path
from . import views_mobile

urlpatterns = [
    path('', views_mobile.mobile_home, name='mobile_home'),
    path('login/', views_mobile.mobile_login, name='mobile_login'),
    path('logout/', views_mobile.mobile_logout, name='mobile_logout'),
    path('entregas/', views_mobile.mobile_entregas, name='mobile_entregas'),
    path('entregas/<int:order_id>/', views_mobile.mobile_entrega_operar, name='mobile_entrega_operar'),
    path('entregas/<int:order_id>/rapida/', views_mobile.mobile_entrega_rapida, name='mobile_entrega_rapida'),
    path('stock/', views_mobile.mobile_stock, name='mobile_stock'),
    path('camioneta/', views_mobile.mobile_camioneta, name='mobile_camioneta'),
    
    # EAC URLs
    path('consultas/', views_mobile.mobile_consultas_list, name='mobile_consultas_list'),
    path('consultas/<int:consulta_id>/', views_mobile.mobile_consulta_detail, name='mobile_consulta_detail'),
    path('pedidos/', views_mobile.mobile_pedidos_list, name='mobile_pedidos_list'),
    path('pedidos/nuevo/', views_mobile.mobile_pedido_crear, name='mobile_pedido_crear'),
]
