from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

import django_excel as excel

from administracion.forms import FeedbackForm
from administracion.models import Escuela, Colegiatura
from becas.models import Beca
from captura.utils import get_study_info
from captura.models import Retroalimentacion
from perfiles_usuario.utils import is_capturista, is_member, ADMINISTRADOR_GROUP,\
    CAPTURISTA_GROUP, is_administrador
from familias.models import Integrante, Familia, Comentario, Alumno, Tutor, Oficio
from familias.utils import total_egresos_familia, total_ingresos_familia, total_neto_familia
from indicadores.models import Transaccion, Ingreso, Periodo

from .models import Estudio, Foto, Seccion, Subseccion, Pregunta, OpcionRespuesta, Respuesta


@login_required
@user_passes_test(is_administrador)
def download_studies(request):
    """ View for an administrator to make a database dump into an excell
        sheet. Each table will be emptied to a page inside the excell
        document.
    """
    return excel.make_response_from_tables(
        [
            Transaccion, Ingreso, Oficio, Periodo,
            Integrante, Familia, Comentario, Alumno, Tutor,
            Estudio, Seccion, Subseccion, Pregunta, OpcionRespuesta, Respuesta,
            Retroalimentacion, Beca, Escuela, Colegiatura

        ],
        'xls',
        file_name="JP2_ESTUDIOS_SOCIOECONOMICOS")


@login_required
@user_passes_test(lambda u: is_member(u, [ADMINISTRADOR_GROUP, CAPTURISTA_GROUP]))
def focus_mode(request, id_estudio):
    """ View to see the detail information about a family and their study.
    """
    context = {}

    estudio = get_object_or_404(Estudio.objects.filter(pk=id_estudio))

    if is_capturista(request.user):
        get_object_or_404(
            Estudio.objects.filter(pk=id_estudio),
            capturista=request.user.capturista)

    integrantes = Integrante.objects.filter(familia=estudio.familia, activo=True).select_related()
    fotos = Foto.objects.filter(estudio=id_estudio)
    context['estudio'] = estudio
    context['integrantes'] = integrantes
    context['fotos'] = fotos
    context['comentarios'] = Comentario.objects.filter(familia=estudio.familia)
    context['total_egresos_familia'] = total_egresos_familia(estudio.familia.id)
    context['total_ingresos_familia'] = total_ingresos_familia(estudio.familia.id)
    context['total_neto_familia'] = total_neto_familia(estudio.familia.id)

    transacciones = Transaccion.objects.filter(es_ingreso=True, familia=estudio.familia)
    context['ingresos'] = Ingreso.objects.filter(transaccion__in=transacciones)
    context['egresos'] = Transaccion.objects.filter(es_ingreso=False, familia=estudio.familia)
    context['cuestionario'] = get_study_info(estudio)
    context['status_options'] = Estudio.get_options_status()

    if estudio.status == Estudio.REVISION:
        feedback_form = FeedbackForm(initial={'estudio': estudio,
                                              'usuario': request.user})
        context['feedback_form'] = feedback_form

    if estudio.status == Estudio.RECHAZADO:
        context['retroalimentacion'] = Retroalimentacion.objects.filter(estudio=estudio)

    return render(
        request,
        'estudios_socioeconomicos/focus_mode.html',
        context)


@login_required
@user_passes_test(is_administrador)
def reject_study(request):
    """ View to reject a study.

    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('administracion:main_estudios', Estudio.RECHAZADO)


@login_required
@user_passes_test(is_administrador)
def accept_study(request, id_estudio):
    """ View to accept a study.
    """
    if request.method == "POST":
        estudio = Estudio.objects.get(pk=id_estudio)
        if estudio.status == Estudio.REVISION:
            estudio.status = Estudio.APROBADO
            estudio.save()
            return redirect('administracion:main_estudios', Estudio.APROBADO)
