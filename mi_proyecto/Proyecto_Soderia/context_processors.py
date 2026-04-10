from .models import ConsultaWeb


def consultas_count(request):
    """Inject count of new web inquiries for the sidebar badge."""
    if not request.user.is_authenticated:
        return {}
    from .views import _is_admin, _has_any_role
    if _is_admin(request.user) or _has_any_role(request.user, ['Encargado de Atencion al Cliente']):
        return {
            'consultas_nuevas_count': ConsultaWeb.objects.filter(
                estado=ConsultaWeb.Estados.NUEVA,
            ).count()
        }
    return {}
