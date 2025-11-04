from .models import SolicitudUnion

def solicitudes_pendientes_context(request):
    """
    Devuelve la cantidad de solicitudes pendientes para el CUIG del usuario logueado.
    """
    if request.user.is_authenticated and hasattr(request.user, "id_rol"):
        if request.user.id_rol and request.user.id_rol.nombre_rol == "Administrador" and request.user.CUIG:
            cantidad = SolicitudUnion.objects.filter(
                establecimiento=request.user.CUIG,
                estado="Pendiente"
            ).count()
            return {"solicitudes_pendientes": cantidad}
    return {"solicitudes_pendientes": 0}
