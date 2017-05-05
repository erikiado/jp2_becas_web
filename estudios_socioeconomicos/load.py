import pickle

from estudios_socioeconomicos.models import Seccion, Subseccion, Pregunta, OpcionRespuesta


def parse(name):
    """ utility script to parse the study.
    """
    preguntas = {}
    while True:
        seccion = input('Ingrese el nombre de la seccion: ')
        if seccion == 'n':
            break
        if seccion not in preguntas:
            preguntas[seccion] = {}
        while True:
            subseccion = input('Ingrese el nombre de la subseccion dentro de %s: ' % seccion)
            if subseccion == 'n':
                break
            curr = 1
            if subseccion not in preguntas[seccion]:
                preguntas[seccion][subseccion] = []
            while True:
                p = input('Ingrese el nombre de la pregunta: ')
                if p == 'n':
                    break
                opt = input('Respuestas: ')
                opt = opt.split(',')
                rel_integrante = input('related? (y/n): ')
                preguntas[seccion][subseccion].append({
                    'texto': p,
                    'numero': curr,
                    'opciones': list(map(lambda x: x.strip(), opt)) if len(opt) > 1 else [],
                    'relacionado_a_integrante': rel_integrante == 'y'
                    })
                curr += 1
    print(preguntas)
    pickle.dump(preguntas, open(name, 'wb'))


def load_data(name='estudios_socioeconomicos/preguntas.pkl'):
    """ Load the questions and sections for the study.

    To execute: import this function after running
    python manage.py shell
    and just call it.
    """
    preguntas = pickle.load(open(name, 'rb'))
    nums = {
        'Generales del Solicitante': 1,
        'Datos y Relación Familiar de Todos los Integrantes de la Vivienda': 2,
        'Situación Económica': 3,
        'Vivienda y Entorno Social': 4,
        'Investigación Laboral': 5,
        'Personalidad': 6,
        'Otros Aspectos': 7
    }
    # delete everything first
    Pregunta.objects.all().delete()
    Seccion.objects.all().delete()
    Subseccion.objects.all().delete()
    OpcionRespuesta.objects.all().delete()

    for sec in preguntas.keys():
        seccion = Seccion.objects.get_or_create(nombre=sec, numero=nums[sec])[0]
        for i, sub in enumerate(preguntas[sec].keys()):
            subseccion = Subseccion.objects.get_or_create(
                                seccion=seccion,
                                nombre=sub,
                                numero=i)[0]
            for p in preguntas[sec][sub]:
                pregunta = Pregunta.objects.get_or_create(
                                subseccion=subseccion,
                                texto=p['texto'],
                                descripcion=p['descripcion'],
                                orden=p['numero'],
                                )[0]
                for opt in p['opciones']:
                    OpcionRespuesta.objects.get_or_create(
                                    pregunta=pregunta,
                                    texto=opt)
