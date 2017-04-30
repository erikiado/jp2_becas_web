import csv
import json
from collections import OrderedDict

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse

from rest_framework.response import Response
import django_excel as excel

from administracion.models import Escuela, Colegiatura
from becas.models import Beca
from captura.utils import get_study_info
from captura.models import Retroalimentacion
from perfiles_usuario.utils import is_capturista, is_member, ADMINISTRADOR_GROUP, CAPTURISTA_GROUP
from perfiles_usuario.utils import is_administrador
from familias.models import Integrante, Familia, Comentario, Integrante, Alumno, Tutor
from familias.utils import total_egresos_familia, total_ingresos_familia, total_neto_familia
from indicadores.models import Transaccion, Ingreso, Oficio, Periodo

from .models import Estudio, Foto, Seccion, Subseccion, Pregunta, OpcionRespuesta, Respuesta
from .serializers import EstudioSerializer


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
            Integrante, Familia, Comentario, Integrante, Alumno, Tutor,
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

    integrantes = Integrante.objects.filter(familia=estudio.familia).select_related()
    fotos = Foto.objects.filter(estudio=id_estudio)
    context['estudio'] = estudio
    context['integrantes'] = integrantes
    context['fotos'] = fotos

    context['total_egresos_familia'] = total_egresos_familia(estudio.familia.id)
    context['total_ingresos_familia'] = total_ingresos_familia(estudio.familia.id)
    context['total_neto_familia'] = total_neto_familia(estudio.familia.id)

    transacciones = Transaccion.objects.filter(es_ingreso=True, familia=estudio.familia)
    context['ingresos'] = Ingreso.objects.filter(transaccion__in=transacciones)
    context['egresos'] = Transaccion.objects.filter(es_ingreso=False, familia=estudio.familia)
    context['cuestionario'] = get_study_info(estudio)
    context['status_options'] = Estudio.get_options_status()
    return render(
        request,
        'estudios_socioeconomicos/focus_mode.html',
        context)
