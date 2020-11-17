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
from api_gateway.api import buscar_usuario, buscar_usuario_mfa, checkStatus, leer_tabla, validar_usuario, guardar_db, buscar_db
from dao import Dao
import json


def index(request):

    return render(request, 'pg/index.html', {'title': 'ISA'})


def Login(request):

    if request.method == 'POST':

        dao = Dao(host='34.233.129.172', port='18081', user='postgres', password='continente7', db='nano')

        df_usuarios = dao.download_from_query(
            """SELECT * FROM usuarios WHERE usuario = '{}' AND password = '{}'""".format(request.POST['username'],
                                                                                         request.POST['password']))

        if len(df_usuarios) > 0:
            print('Usuario validado')
            usuario = request.POST['username']
            return redirect('mfa', nombre=usuario)

        else:
            print('Usuario invalido')
            messages.info(request, f'Error: Intente log in nuevamente')

    form = AuthenticationForm()

    return render(request, 'pg/login.html', {'form': form, 'title': 'Log In'})


def mfa(request, nombre):

    if request.method == 'POST':\

        dao = Dao(host='34.233.129.172', port='18081', user='postgres', password='continente7', db='nano')

        df_mfa = dao.download_from_query(
            """SELECT * FROM usuarios WHERE usuario = '{}' AND mfa = '{}'""".format(nombre,
                                                                                    request.POST['clave_multifactor']))

        if len(df_mfa) > 0:
            print('MFA Validado')

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

                    guardar_db('planestudios', [nombrePlan, cargaHorariaTotal, resolucionConeau, resolucionMinEdu, resolucionRectoral])

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
    data = json.loads(json_records)

    return render(request, 'pg/mostrarplanestudios.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'planes': data})


def mostrarPlanEstudiosDetalle(request, nombre, idplan):

    # status = checkStatus()
    status = 'UP'

    validated, rol = validar_usuario(nombre)

    response = {'Items': [{'resolucionConeau': 'A1A', 'cargaHorariaTotal': '160', 'resolucionMinEdu': '111',
                           'nombrePlan': 'Ing Agrimensura', 'resolucionRectoral': '222', 'idPlan': '3'}], 'Count': 1, 'ScannedCount': 1}

    response_materias = {'Items': [{'idMateria': '1', 'Descriptor': 'Fisica 1'}], 'Count': 1, 'ScannedCount': 1}

    response_competencias = {'Items': [{'idCompetencia': '32', 'Descriptor': 'Sistemas informaticos'}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarplanestudiosdetalle.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'planes': response['Items'], 'materias': response_materias['Items'],
                                            'competencias': response_competencias['Items']})


def crearMateria(request, nombre):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    form = materiaForm()
    if request.method == 'POST':
        try:
            form = materiaForm(request.POST)
            if form.is_valid():

                descriptor = form.cleaned_data['materia']

                return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                        'status': status})
        except Exception:
            pass

    return render(request, 'pg/crearmateria.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})


def mostrarMaterias(request, nombre):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    response = {'Items': [{'idMateria': '1', 'Descriptor': 'Fisica 1'}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarmaterias.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'planes': response['Items']})


def mostrarMateriaDetalle(request, nombre, idmateria):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    response = {'Items': [{'idContenidoCurricular': '1', 'Descriptor': 'Objetivo', 'idMateria': 1}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarmateriadetalle.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'planes': response['Items'], 'idmateria': idmateria})


def crearContenidoCurricular(request, nombre, idmateria):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    form = curricularForm()
    if request.method == 'POST':
        try:
            form = curricularForm(request.POST)
            if form.is_valid():

                print ('Creando Curricula')

                descriptor = form.cleaned_data['descriptor']

                print (descriptor)

                print ('Curricula Creada')

                return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                        'status': status})
        except Exception:
            pass

    return render(request, 'pg/crearcontenidocurricular.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form, 'idmateria': idmateria})


def mostrarContenidoCurricular(request, nombre, idcontenidocurricular, idmateria, descriptor):

    nombre = 'tester'
    rol = 'Director'

    response_cont_curricular = {'Items': [{'idContenidoCurricular': '1', 'Descriptor': 'Objetivo', 'idMateria': 1}], 'Count': 1, 'ScannedCount': 1}
    response_unidades = {'Items': [{'idUnidad': '1', 'Descriptor': 'Repaso', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}
    response_act_formacion = {'Items': [{'idActFormacionPractica': '1', 'Descriptor': 'TP 1', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarcontenidocurricular.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                            'response_cont_curricular': response_cont_curricular['Items'],
                            'idcontenidocurricular': idcontenidocurricular, 'idmateria': idmateria, 'descriptor': descriptor,
                            'response_unidades': response_unidades['Items'], 'response_act_formacion': response_act_formacion['Items']
                                                                  })

def mostrarUnidad(request, nombre, idunidad):

    nombre = 'tester'
    rol = 'Director'

    response_unidades = {'Items': [{'idUnidad': '1', 'Descriptor': 'Repaso', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarunidad.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                     'idunidad': idunidad,
                                                     'response_unidades': response_unidades['Items']
                                                                  })


def mostrarActFormacionPractica(request, nombre, idactformacionpractica):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    response_cont_curricular = {'Items': [{'idContenidoCurricular': '1', 'Descriptor': 'Objetivo', 'idMateria': 1}], 'Count': 1, 'ScannedCount': 1}
    response_unidades = {'Items': [{'idUnidad': '1', 'Descriptor': 'Repaso', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}
    response_act_formacion = {'Items': [{'idActFormacionPractica': '1', 'Descriptor': 'TP 1', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostraractformacionpractica.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                            'response_act_formacion': response_act_formacion['Items'],
                            'idactformacionpractica': idactformacionpractica,
                                                                  })


def crearCompetencia(request, nombre, idplan):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    form = competenciaForm()
    if request.method == 'POST':
        try:
            form = competenciaForm(request.POST)
            if form.is_valid():

                # guardar con idplan

                return mostrarPlanEstudiosDetalle(request, nombre, idplan)

        except Exception:
            pass

    return render(request, 'pg/crearcompetencia.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})


def mostrarCompetencias(request, nombre):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    response_competencias = {'Items': [{'idCompetencia': '32', 'Descriptor': 'Sistemas informaticos'}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarcompetencias.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'planes': response_competencias['Items']})


def mostrarCompetenciaDetalle(request, nombre, idcompetencia):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    response_competencia = {'Items': [{'idCompetencia': '32', 'Descriptor': 'Sistemas informaticos'}], 'Count': 1, 'ScannedCount': 1}

    response_capacidades = {'Items': [{'idCapacidad': '7', 'Descriptor': 'Programar'}, {'idCapacidad': '5', 'Descriptor': 'Diagramar'}]}

    return render(request, 'pg/mostrarcompetenciadetalle.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status,
                                            'competencias': response_competencia['Items'],
                                            'capacidades': response_capacidades['Items']})


def crearCapacidad(request, nombre, idcompetencia):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    form = capacidadForm()
    if request.method == 'POST':
        try:
            form = capacidadForm(request.POST)
            if form.is_valid():

                # guardar con idcompetencia

                return mostrarCompetenciaDetalle(request, nombre, idcompetencia)

        except Exception:
            pass

    return render(request, 'pg/crearcapacidad.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})


def crearUnidad(request, nombre, idcontenidocurricular):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    form = unidadForm()
    if request.method == 'POST':
        try:
            form = unidadForm(request.POST)
            if form.is_valid():

                descriptor = form.cleaned_data['unidad']

                return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                        'status': status})
        except Exception:
            pass

    return render(request, 'pg/crearunidad.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})


def crearActa(request, nombre, idcontenidocurricular):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    form = actaForm()
    if request.method == 'POST':
        try:
            form = actaForm(request.POST)
            if form.is_valid():

                descriptor = form.cleaned_data['unidad']

                return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                        'status': status})
        except Exception:
            pass

    return render(request, 'pg/crearacta.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})