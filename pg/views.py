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
from api_gateway.api import buscar_usuario, buscar_usuario_mfa, checkStatus, leer_tabla


def index(request):

    return render(request, 'pg/index.html', {'title': 'ISA 2019 APP'})


def Login(request):

    ### HARDCODEO ###
    usuario ='director'


    if request.method == 'POST':

        # usuario = buscar_usuario(tabla='usuarios', input_usuario=request.POST['username'], input_password=request.POST['password'])

        if len(usuario) > 0:
            print('Usuario validado')
            nombre = usuario[0]
            return redirect('mfa', nombre=nombre)
    #
    #     else:
    #         print('Usuario invalido')
    #         messages.info(request, f'Error: Intente log in nuevamente')
    #
    form = AuthenticationForm()

    return render(request, 'pg/login.html', {'form': form, 'title': 'Log In'})


def mfa(request, nombre):


    # usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)
    #
    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     clave_mfa = usuario[3]

    if request.method == 'POST':

        # if request.POST['clave_multifactor'] == clave_mfa:

        print('MFA Validado')

        return redirect('menu', nombre=nombre)

    form = keyForm()
    # htmly = get_template('pg/Email.html')
    # d = {'username': nombre, 'clave': clave_mfa}
    # subject, from_email, to = 'ISA Clave MFA', 'trqarg@gmail.com', email
    # html_content = htmly.render(d)
    # msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()

    return render(request, 'pg/mfa.html', {'form': form, 'title': 'MFA'})


def menu(request, nombre):

    # usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)
    #
    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     rol = usuario[2]
    #     status = checkStatus()
    #
    # else:
    #     print('Usuario invalido')

    rol = 'Director'

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

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    # usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)

    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     rol = usuario[2]
    #     status = checkStatus()
    #
    # else:
    #     print('Usuario invalido')

    form = planEstudioForm()
    if request.method == 'POST':
        try:
            form = planEstudioForm(request.POST)
            if form.is_valid():

                print ('Creando Plan de estudios')

                nombrePlan = form.cleaned_data['nombrePlan']
                cargaHorariaTotal = form.cleaned_data['cargaHorariaTotal']
                resolucionConeau = form.cleaned_data['resolucionConeau']
                resolucionMinEdu = form.cleaned_data['resolucionMinEdu']
                resolucionRectoral = form.cleaned_data['resolucionRectoral']

                print (nombrePlan, cargaHorariaTotal,resolucionConeau,resolucionMinEdu, resolucionRectoral)

                print ('Plan de estudios creado')

                return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                        'status': status})
        except Exception:
            pass

    return render(request, 'pg/crearplanestudios.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form})


def mostrarPlanEstudios(request, nombre):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    # usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)
    #
    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     rol = usuario[2]
    #     status = checkStatus()
    #
    # else:
    #     print('Usuario invalido')
    #
    # response = leer_tabla('PlanEstudios')

    response = {'Items': [{'resolucionConeau': 'A1A', 'cargaHorariaTotal': '160', 'resolucionMinEdu': '111', 'nombrePlan': 'Ing Agrimensura', 'resolucionRectoral': '222', 'idPlan': '3'}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarplanestudios.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'planes': response['Items']})


def mostrarPlanEstudiosDetalle(request, nombre, idplan):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    # usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)
    #
    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     rol = usuario[2]
    #     status = checkStatus()
    #
    # else:
    #     print('Usuario invalido')
    #
    # response = leer_tabla('PlanEstudios')

    response = {'Items': [{'resolucionConeau': 'A1A', 'cargaHorariaTotal': '160', 'resolucionMinEdu': '111', 'nombrePlan': 'Ing Agrimensura', 'resolucionRectoral': '222', 'idPlan': '3'}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarplanestudiosdetalle.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'planes': response['Items']})


def crearMateria(request, nombre):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    # usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)

    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     rol = usuario[2]
    #     status = checkStatus()
    #
    # else:
    #     print('Usuario invalido')

    form = materiaForm()
    if request.method == 'POST':
        try:
            form = materiaForm(request.POST)
            if form.is_valid():

                print ('Creando Materia')

                descriptor = form.cleaned_data['materia']

                print (descriptor)

                print ('Materia Creada')

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

    # usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)
    #
    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     rol = usuario[2]
    #     status = checkStatus()
    #
    # else:
    #     print('Usuario invalido')
    #
    # response = leer_tabla('PlanEstudios')

    response = {'Items': [{'idMateria': '1', 'Descriptor': 'Fisica 1'}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarmaterias.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'planes': response['Items']})


def mostrarMateriaDetalle(request, nombre, idmateria):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    # usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)
    #
    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     rol = usuario[2]
    #     status = checkStatus()
    #
    # else:
    #     print('Usuario invalido')
    #
    # response = leer_tabla('ContenidoCurricular')

    response = {'Items': [{'idContenidoCurricular': '1', 'Descriptor': 'Objetivo', 'idMateria': 1}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarmateriadetalle.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'planes': response['Items'], 'idmateria': idmateria})



def crearContenidoCurricular(request, nombre, idmateria):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    # usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)

    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     rol = usuario[2]
    #     status = checkStatus()
    #
    # else:
    #     print('Usuario invalido')

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

    # usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)
    #
    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     rol = usuario[2]
    #     status = checkStatus()
    #
    # else:
    #     print('Usuario invalido')
    #
    # response = leer_tabla('ContenidoCurricular')

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

    # usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)
    #
    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     rol = usuario[2]
    #     status = checkStatus()
    #
    # else:
    #     print('Usuario invalido')
    #
    # response = leer_tabla('ContenidoCurricular')

    response_unidades = {'Items': [{'idUnidad': '1', 'Descriptor': 'Repaso', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarunidad.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                     'idunidad': idunidad,
                                                     'response_unidades': response_unidades['Items']
                                                                  })


def mostrarActFormacionPractica(request, nombre, idactformacionpractica):

    nombre = 'tester'
    rol = 'Director'
    status = 'UP'

    # usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)
    #
    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     rol = usuario[2]
    #     status = checkStatus()
    #
    # else:
    #     print('Usuario invalido')
    #
    # response = leer_tabla('ContenidoCurricular')

    response_cont_curricular = {'Items': [{'idContenidoCurricular': '1', 'Descriptor': 'Objetivo', 'idMateria': 1}], 'Count': 1, 'ScannedCount': 1}
    response_unidades = {'Items': [{'idUnidad': '1', 'Descriptor': 'Repaso', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}
    response_act_formacion = {'Items': [{'idActFormacionPractica': '1', 'Descriptor': 'TP 1', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostraractformacionpractica.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                            'response_act_formacion': response_act_formacion['Items'],
                            'idactformacionpractica': idactformacionpractica,
                                                                  })