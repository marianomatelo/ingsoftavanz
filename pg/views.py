from django.shortcuts import render, redirect
from pg.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, keyForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.timezone import datetime
from django.urls import reverse
from django.shortcuts import redirect
from . models import User
import pandas as pd
# from pg.tables import datasetTable
import random
import string
from api_gateway.api import buscar_usuario, buscar_usuario_mfa, checkStatus, leer_tabla, validar_usuario, guardar_db, buscar_db, buscar_db_id, log_acceso, log_creacion
from dao import Dao
import json


def index(request):
    '''
    Primera pagina visible al acceder a la url

    :param request: solicitud de mostrar pagina
    :return: pagina renderizada en navegador
    '''

    return render(request, 'pg/index.html', {'title': 'ISA'})


def Login(request):
    '''
    Pagina de logeo donde se solicita el usuario y contrasena

    :param request: solicitud de mostrar pagina
    :return: pagina renderizada en navegador
    '''

    if request.method == 'POST':

        validated, rol = validar_usuario(request.POST['username'])

        if validated:
            print('Usuario validado')

            usuario = request.POST['username']

            return redirect('mfa', nombre=usuario)

        else:
            print('Usuario invalido')

            messages.info(request, f'Error: Intente log in nuevamente')

    form = AuthenticationForm()

    return render(request, 'pg/login.html', {'form': form, 'title': 'Log In'})


def mfa(request, nombre):
    '''
    Pagina de validacion del MFA, genera un codigo MFA, lo envia por mail y lo valida.

    :param request: solicitud de mostrar pagina
    :param nombre: nombre de usuario ingresado
    :return: pagina renderizada en navegador
    '''

    if request.method == 'POST':\

        dao = Dao(host='34.233.129.172', port='18081', user='postgres', password='continente7', db='nano')

        df_mfa = dao.download_from_query(
            """SELECT * FROM usuarios WHERE usuario = '{}' AND mfa = '{}'""".format(nombre,
                                                                                    request.POST['clave_multifactor']))

        if len(df_mfa) > 0:
            print('MFA Validado')

            log_acceso(nombre, df_mfa['rol'].iloc[0])

            return redirect('menu', nombre=nombre, rol=df_mfa['rol'].iloc[0])

    form = keyForm()
    # htmly = get_template('pg/Email.html')
    # d = {'username': nombre, 'clave': clave_mfa}
    # subject, from_email, to = 'ISA Clave MFA', 'trqarg@gmail.com', email
    # html_content = htmly.render(d)
    # msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()

    return render(request, 'pg/mfa.html', {'form': form, 'title': 'MFA'})


def menu(request, nombre, rol):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status})


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             nuevo_usuario = User(rol=request.POST['rol'], name=request.POST['username'],
#                                  email=request.POST['email'], password=request.POST['password1'])
#             nuevo_usuario.save()
#
#             messages.success(request, f'Your account has been created! You are now able to log in')
#             return redirect('login')
#
#     else:
#         form = UserRegisterForm()
#
#     return render(request, 'pg/register.html', {'form': form, 'title': 'Reqister'})


def crearPlanEstudios(request, nombre):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    form = planEstudioForm()

    if validated:

        if request.method == 'POST':

            try:

                form = planEstudioForm(request.POST)

                if form.is_valid():

                    nombrePlan = form.cleaned_data['nombrePlan']
                    cargaHorariaTotal = form.cleaned_data['cargaHorariaTotal']
                    resolucionConeau = form.cleaned_data['resolucionConeau']
                    resolucionMinEdu = form.cleaned_data['resolucionMinEdu']
                    resolucionRectoral = form.cleaned_data['resolucionRectoral']

                    guardar_db('planestudios', 'nombreplan, cargahorariatotal, resolucionconeau, resolucionminedu, resolucionrectoral'
                                               ',fecha_creacion, usuario_creacion,fecha_modificacion, usuario_modificacion',
                                           [nombrePlan, cargaHorariaTotal, resolucionConeau, resolucionMinEdu, resolucionRectoral,
                                             str(pd.to_datetime('today')), nombre, str(pd.to_datetime('today')), nombre])

                    log_creacion(nombre, rol, 'Plan de estudios')

                    return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol, 'status': status})

            except Exception:
                pass

    return render(request, 'pg/crearplanestudios.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})


def mostrarPlanEstudios(request, nombre):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    df = buscar_db('planestudios')

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient='records')
    planes_json = json.loads(json_records)

    return render(request, 'pg/mostrarplanestudios.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'planes': planes_json})


def mostrarPlanEstudiosDetalle(request, nombre, idplan):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    df_planes = buscar_db_id('planestudios', 'idplan', idplan)

    # parsing the DataFrame in json format.
    json_records = df_planes.reset_index().to_json(orient='records')
    json_plan = json.loads(json_records)

    df = buscar_db_id('planestudios_materia', 'idplan', idplan)

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient='records')
    materias_json = json.loads(json_records)

    df = buscar_db_id('competencia', 'idplan', idplan)

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient='records')
    competencias_json = json.loads(json_records)

    return render(request, 'pg/mostrarplanestudiosdetalle.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'plan': json_plan, 'materias': materias_json,
                                            'competencias': competencias_json})


def crearMateria(request, nombre):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    form = materiaForm()

    if request.method == 'POST':

        try:

            form = materiaForm(request.POST)

            if form.is_valid():

                nombreMateria = form.cleaned_data['materia']
                descripcion = form.cleaned_data['descriptor']

                guardar_db('materias', 'nombre, descripcion'
                                       ',fecha_creacion, usuario_creacion'
                                       ',fecha_modificacion, usuario_modificacion',
                                       [nombreMateria, descripcion, str(pd.to_datetime('today')),
                                        nombre, str(pd.to_datetime('today')), nombre])

                log_creacion(nombre, rol, 'Materias')

                return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                        'status': status})
        except Exception:
            pass

    return render(request, 'pg/crearmateria.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})


def agregarMateria(request, nombre, idplan):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    form = materiaForm()

    if request.method == 'POST':

        try:

            form = materiaForm(request.POST)

            if form.is_valid():

                nombreMateria = form.cleaned_data['materia']
                descripcion = form.cleaned_data['descriptor']

                guardar_db('materias', 'nombre, descripcion'
                                       ',fecha_creacion, usuario_creacion'
                                       ',fecha_modificacion, usuario_modificacion',
                                       [nombreMateria, descripcion, str(pd.to_datetime('today')),
                                        nombre, str(pd.to_datetime('today')), nombre])

                log_creacion(nombre, rol, 'Materias')

                return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                        'status': status})
        except Exception:
            pass

    return render(request, 'pg/crearmateria.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})


def mostrarMaterias(request, nombre):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    df = buscar_db('materias')

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient='records')
    materias_json = json.loads(json_records)

    return render(request, 'pg/mostrarmaterias.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'materias': materias_json})


def mostrarMateriaDetalle(request, nombre, idmateria):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    df = buscar_db_id('materias', 'idmateria', idmateria)

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient='records')
    materias_json = json.loads(json_records)

    # Busco Contenidos Curriculares relacionados a la Materia
    df = buscar_db_id('contenidocurricular', 'idmateria', idmateria)

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient='records')
    contenidos_json = json.loads(json_records)

    return render(request, 'pg/mostrarmateriadetalle.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'materias': materias_json, 'idmateria': idmateria, 'contenidos': contenidos_json})



def crearContenidoCurricular(request, nombre, idmateria):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    df = buscar_db_id('materias', 'idmateria', idmateria)

    nombre_materia = df['nombre'].iloc[0]

    form = curricularForm()
    if request.method == 'POST':
        try:
            form = curricularForm(request.POST)
            if form.is_valid():

                nombreContenido = form.cleaned_data['contenido']
                descripcion = form.cleaned_data['descriptor']

                guardar_db('contenidocurricular', 'descripcion, idmateria, nombre, '
                                                  'fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion',
                           [nombreContenido, idmateria, descripcion, descripcion, str(pd.to_datetime('today')),
                                        nombre, str(pd.to_datetime('today')), nombre])

                log_creacion(nombre, rol, 'Contenido Curricular')

                return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                        'status': status})
        except Exception:
            pass

    return render(request, 'pg/crearcontenidocurricular.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form, 'nombre_materia': nombre_materia})


def mostrarContenidoCurricular(request, nombre, idcontenidocurricular, idmateria, descriptor):

    validated, rol = validar_usuario(nombre)

    df = buscar_db_id('contenidocurricular', 'idmateria', idmateria)

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient='records')
    contenido_json = json.loads(json_records)

    df = buscar_db_id('unidades', 'idcontenidocurricular', idcontenidocurricular)

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient='records')
    unidades_json = json.loads(json_records)


    df = buscar_db_id('actaformacion', 'idcontenidocurricular', idcontenidocurricular)

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient='records')
    actas_json = json.loads(json_records)

    return render(request, 'pg/mostrarcontenidocurricular.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                            'response_cont_curricular': contenido_json,
                            'idcontenidocurricular': idcontenidocurricular, 'idmateria': idmateria, 'descriptor': descriptor,
                            'response_unidades': unidades_json, 'response_act_formacion': actas_json
                                                                  })

def mostrarUnidad(request, nombre, idunidad):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    response_unidades = {'Items': [{'idUnidad': '1', 'Descriptor': 'Repaso', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarunidad.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                     'idunidad': idunidad,
                                                     'response_unidades': response_unidades['Items']
                                                                  })


def mostrarActFormacionPractica(request, nombre, idactformacionpractica):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    response_cont_curricular = {'Items': [{'idContenidoCurricular': '1', 'Descriptor': 'Objetivo', 'idMateria': 1}], 'Count': 1, 'ScannedCount': 1}
    response_unidades = {'Items': [{'idUnidad': '1', 'Descriptor': 'Repaso', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}
    response_act_formacion = {'Items': [{'idActFormacionPractica': '1', 'Descriptor': 'TP 1', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostraractformacionpractica.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                            'response_act_formacion': response_act_formacion['Items'],
                            'idactformacionpractica': idactformacionpractica,
                                                                  })


def crearCompetencia(request, nombre, idplan):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    form = competenciaForm()
    if request.method == 'POST':
        try:
            form = competenciaForm(request.POST)
            if form.is_valid():

                nombreCompetencia = form.cleaned_data['competencia']
                descripcion = form.cleaned_data['descriptor']

                guardar_db('competencia', 'descripcion, nombre, idplan, '
                                          'fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion',
                           [nombreCompetencia, descripcion, idplan, str(pd.to_datetime('today')),
                                        nombre, str(pd.to_datetime('today')), nombre])

                log_creacion(nombre, rol, 'Competencia')

                return mostrarPlanEstudiosDetalle(request, nombre, idplan)

        except Exception:
            pass

    return render(request, 'pg/crearcompetencia.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})


def mostrarCompetencias(request, nombre):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    df = buscar_db('competencia')

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient='records')
    competencias_json = json.loads(json_records)

    return render(request, 'pg/mostrarcompetencias.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'competencias': competencias_json})


def mostrarCompetenciaDetalle(request, nombre, idcompetencia):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    df = buscar_db_id('competencia', 'idcompetencia', idcompetencia)

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient='records')
    competencias_json = json.loads(json_records)

    df = buscar_db_id('capacidades', 'idcompetencia', idcompetencia)

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient='records')
    capacidades_json = json.loads(json_records)

    return render(request, 'pg/mostrarcompetenciadetalle.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status,
                                            'competencias': competencias_json,
                                            'capacidades': capacidades_json})


def crearCapacidad(request, nombre, idcompetencia):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    form = capacidadForm()
    if request.method == 'POST':
        try:
            form = capacidadForm(request.POST)
            if form.is_valid():

                nombreCapacidad = form.cleaned_data['capacidad']
                descripcion = form.cleaned_data['descriptor']

                guardar_db('capacidades', 'nombre, descripcion, idcompetencia, '
                                          'fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion',
                           [nombreCapacidad, descripcion, idcompetencia, str(pd.to_datetime('today')),
                            nombre, str(pd.to_datetime('today')), nombre])

                log_creacion(nombre, rol, 'Capacidad')

                return mostrarCompetenciaDetalle(request, nombre, idcompetencia)

        except Exception:
            pass

    return render(request, 'pg/crearcapacidad.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})


def crearUnidad(request, nombre, idcontenidocurricular):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    form = unidadForm()
    if request.method == 'POST':
        try:
            form = unidadForm(request.POST)
            if form.is_valid():

                nombreunidad = form.cleaned_data['unidad']
                descripcion = form.cleaned_data['descriptor']

                guardar_db('unidades', 'nombre, descriptor, idcontenidocurricular, '
                                       'fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion',
                           [nombreunidad, descripcion, idcontenidocurricular,
                            str(pd.to_datetime('today')), nombre, str(pd.to_datetime('today')), nombre])

                log_creacion(nombre, rol, 'Unidad')

                return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                        'status': status})
        except Exception:
            pass

    return render(request, 'pg/crearunidad.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})


def crearActa(request, nombre, idcontenidocurricular):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    form = actaForm()
    if request.method == 'POST':
        try:
            form = actaForm(request.POST)
            if form.is_valid():

                nombreacta = form.cleaned_data['acta']
                descripcion = form.cleaned_data['descriptor']

                guardar_db('actaformacion', 'nombre, descriptor, idcontenidocurricular,'
                                            ' fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion',
                                           [nombreacta, descripcion, idcontenidocurricular,
                                            str(pd.to_datetime('today')),nombre, str(pd.to_datetime('today')), nombre])

                log_creacion(nombre, rol, 'Acta')

                return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                        'status': status})
        except Exception:
            pass

    return render(request, 'pg/crearacta.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})