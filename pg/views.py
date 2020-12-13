from django.shortcuts import render
from pg.forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import keyForm, agregarMateriaForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.shortcuts import redirect
import pandas as pd
from random import randrange
from api_gateway.api import checkStatus, validar_usuario, guardar_db, \
                        buscar_db, buscar_db_id, log_acceso, log_creacion, chequeo_existencia, get_data, validar_mfa, \
                        guardar_mfa, validar_usuario_password
from api_gateway.crypto import encrypt_message
import json


def index(request):
    '''
    Primera pagina, punto de acceso de la aplicacion

    :param request: solicitud de mostrar pagina de index
    :return: pagina Index renderizada en navegador
    '''

    return render(request, 'pg/index.html', {'title': 'ISA'})


def Login(request):
    '''
    Pagina de login donde se solicita el usuario y contrasena

    :param request: solicitud de mostrar pagina de login
    :return: pagina renderizada en navegador
    '''

    # Si el usuario envio el formulario
    if request.method == 'POST':

        # Obtengo los parametros ingresados por el usuario
        usuario = request.POST['username']
        password = request.POST['password']

        # Encripto la password ingresada por el usuario
        encrypted_password = encrypt_message(password)

        # Comparo la password ingresada con la almacenada
        validated, rol = validar_usuario_password(request.POST['username'], encrypted_password)

        if validated:
            # Passwords coinciden
            print('Usuario validado')

            return redirect('mfa', nombre=usuario)

        else:
            # Password no coincide
            print('Usuario invalido')

            messages.info(request, f'Error: Intente log in nuevamente')

    # Formulario de login para que el usuario complete
    form = AuthenticationForm()

    return render(request, 'pg/login.html', {'form': form, 'title': 'Log In'})


def mfa(request, nombre):
    '''
    Pagina de validacion del MFA, genera un codigo MFA, lo envia por mail y lo valida.

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :return: pagina renderizada en navegador
    '''

    if request.method == 'POST':

        validated, rol = validar_mfa(nombre, request.POST['clave_multifactor'])

        if validated:
            print('MFA Validado')

            log_acceso(nombre, rol)

            return redirect('menu', nombre=nombre, rol=rol)

    # Formulario de MFA para que el usuario complete
    form = keyForm()

    # Genero un nuevo MFA para el usuario
    generated_mfa = randrange(0, 999999, 6)

    # Almaceno en la base el nuevo codigo de MFA
    to_email = guardar_mfa(nombre, generated_mfa)

    # Preparo para enviarle el nuevo codigo MFA por email
    try:
        htmly = get_template('pg/Email.html')
        d = {'username': nombre, 'clave': generated_mfa}
        subject, from_email, to = 'Clave MFA', 'trqarg@gmail.com', to_email
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")

        # Enviando mensaje por email
        msg.send()

    except Exception as e:
        print('Error enviando codigo MFA por email ', e)

    return render(request, 'pg/mfa.html', {'form': form, 'title': 'MFA'})


def menu(request, nombre, rol):
    '''
    Pagina de menu principal donde el usuario tiene los principales accesos
    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :return: pagina renderizada en navegador
    '''

    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
    validated, rol = validar_usuario(nombre)

    return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status})


def crearPlanEstudios(request, nombre):
    '''
    Pagina de menu principal donde el usuario tiene los principales accesos
    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :return: pagina renderizada en navegador
    '''
    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
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
    '''
    Pagina que lista los planes de estudio y sus detalles
    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :return: pagina renderizada en navegador
    '''

    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
    validated, rol = validar_usuario(nombre)

    # Busco en la DB todos los Planes de Estudio
    df = buscar_db('planestudios')

    # Parseo el DataFrame al formato JSON
    json_records = df.reset_index().to_json(orient='records')
    planes_json = json.loads(json_records)

    return render(request, 'pg/mostrarplanestudios.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'planes': planes_json})


def mostrarPlanEstudiosDetalle(request, nombre, idplan):
    '''
    Pagina de plan de estudios donde se visualizan sus detalles

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :param idplan: id de plan seleccionado por el usuario
    :return: pagina renderizada en navegador
    '''

    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
    validated, rol = validar_usuario(nombre)

    # Busco en la tabla de Planes de Estudio el Plan con el idplan
    df_planes = buscar_db_id('planestudios', 'idplan', idplan)

    # Parseo el DataFrame al formato JSON
    json_records = df_planes.reset_index().to_json(orient='records')
    json_plan = json.loads(json_records)

    # Busco en la tabla de Materias las materias correspondientes al idplan
    df = buscar_db_id('planestudios_materia', 'idplan', idplan)

    # Parseo el DataFrame al formato JSON
    json_records = df.reset_index().to_json(orient='records')
    materias_json = json.loads(json_records)

    # Busco en la tabla de Competencias las competencias correspondientes al idplan
    df = buscar_db_id('competencia', 'idplan', idplan)

    # Parseo el DataFrame al formato JSON
    json_records = df.reset_index().to_json(orient='records')
    competencias_json = json.loads(json_records)

    return render(request, 'pg/mostrarplanestudiosdetalle.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'plan': json_plan, 'materias': materias_json,
                                            'competencias': competencias_json})


def crearMateria(request, nombre):
    '''
    Pagina para crear una nueva Materia

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :return: materia creada
    '''

    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
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
    '''
    Pagina para agregar una materia a un Plan de Estudios

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :param idplan: id de plan seleccionado por el usuario
    :return: materia creada
    '''
    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
    validated, rol = validar_usuario(nombre)

    if request.method == 'POST':

        try:

            form = agregarMateriaForm(request.POST)

            if form.is_valid():

                nombreMateria = form.cleaned_data['materia']

                exists = chequeo_existencia('planestudios_materia', idplan, nombreMateria)

                if exists:
                    print('La relacion materia-plan ya existe')

                else:
                    idmateria, descripcion = get_data('materias', nombreMateria)

                    guardar_db('planestudios_materia', 'idplan, idmateria, nombre, descripcion'
                                           ',fecha_creacion, usuario_creacion'
                                           ',fecha_modificacion, usuario_modificacion',
                                           [idplan, idmateria,nombreMateria, descripcion, str(pd.to_datetime('today')),
                                            nombre, str(pd.to_datetime('today')), nombre])

                    log_creacion(nombre, rol, 'Materias')

                return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                        'status': status})
        except Exception:
            pass

    return render(request, 'pg/agregarmateria.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': agregarMateriaForm()})


def mostrarMaterias(request, nombre):
    '''
    Pagina para mostrar todas las Materias

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :return: pagina listando todas las materias
    '''

    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
    validated, rol = validar_usuario(nombre)

    df = buscar_db('materias')

    # Parseo el DataFrame al formato JSON
    json_records = df.reset_index().to_json(orient='records')
    materias_json = json.loads(json_records)

    return render(request, 'pg/mostrarmaterias.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'materias': materias_json})


def mostrarMateriaDetalle(request, nombre, idmateria):
    '''
    Pagina para mostrar el detalle de la materia seleccionada por el usuario

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :param idmateria: id de la materia seleccionada por el usuario
    :return: pagina mostrando detalles de la materia
    '''
    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
    validated, rol = validar_usuario(nombre)

    # Busco detalles de la Materia segun idmateria
    df = buscar_db_id('materias', 'idmateria', idmateria)

    # Parseo el DataFrame al formato JSON
    json_records = df.reset_index().to_json(orient='records')
    materias_json = json.loads(json_records)

    # Busco Contenidos Curriculares relacionados a la Materia
    df = buscar_db_id('contenidocurricular', 'idmateria', idmateria)

    # Parseo el DataFrame al formato JSON
    json_records = df.reset_index().to_json(orient='records')
    contenidos_json = json.loads(json_records)

    return render(request, 'pg/mostrarmateriadetalle.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'materias': materias_json, 'idmateria': idmateria, 'contenidos': contenidos_json})



def crearContenidoCurricular(request, nombre, idmateria):
    '''
    Pagina para crear un nuevo Contenido Curricular

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :param idmateria: id de la materia seleccionada por el usuario
    :return: pagina mostrando detalles de la materia
    '''

    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
    validated, rol = validar_usuario(nombre)

    # Busco detalles de la Materia segun idmateria
    df = buscar_db_id('materias', 'idmateria', idmateria)

    # Almaceno el nombre de la materia seleccionada
    nombre_materia = df['nombre'].iloc[0]

    # Creo formulacion de creacion de Contenido Curricular
    form = curricularForm()

    # Si el usuario envio el formulario
    if request.method == 'POST':

        try:
            form = curricularForm(request.POST)

            # Valido el formulario
            if form.is_valid():

                # Obtengo los parametros ingresados por el usuario en el formulario
                nombreContenido = form.cleaned_data['contenido']
                descripcion = form.cleaned_data['descriptor']

                # Almaceno el nuevo Contenido Curricular en la DB
                guardar_db('contenidocurricular', 'descripcion, idmateria, nombre, '
                                                  'fecha_creacion, usuario_creacion, fecha_modificacion, usuario_modificacion',
                           [nombreContenido, idmateria, descripcion, descripcion, str(pd.to_datetime('today')),
                                        nombre, str(pd.to_datetime('today')), nombre])

                # Registro la creacion en el Log
                log_creacion(nombre, rol, 'Contenido Curricular')

                return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                        'status': status})
        except Exception:
            pass

    return render(request, 'pg/crearcontenidocurricular.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'form': form, 'nombre_materia': nombre_materia})


def mostrarContenidoCurricular(request, nombre, idcontenidocurricular, idmateria, descriptor):
    '''
    Pagina para mostrar el Contenido Curricular

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :param idmateria: id de la materia seleccionada por el usuario
    :return: pagina mostrando detalles de la materia
    '''
    # Valido la sesion del usuario
    validated, rol = validar_usuario(nombre)

    df = buscar_db_id('contenidocurricular', 'idmateria', idmateria)

    # Parseo el DataFrame al formato JSON
    json_records = df.reset_index().to_json(orient='records')
    contenido_json = json.loads(json_records)

    df = buscar_db_id('unidades', 'idcontenidocurricular', idcontenidocurricular)

    # Parseo el DataFrame al formato JSON
    json_records = df.reset_index().to_json(orient='records')
    unidades_json = json.loads(json_records)

    # Busco en la tabla de actaformacion segun el idcontenidocurricular
    df = buscar_db_id('actaformacion', 'idcontenidocurricular', idcontenidocurricular)

    # Parseo el DataFrame al formato JSON
    json_records = df.reset_index().to_json(orient='records')
    actas_json = json.loads(json_records)

    return render(request, 'pg/mostrarcontenidocurricular.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                            'response_cont_curricular': contenido_json,
                            'idcontenidocurricular': idcontenidocurricular, 'idmateria': idmateria, 'descriptor': descriptor,
                            'response_unidades': unidades_json, 'response_act_formacion': actas_json
                                                                  })

def mostrarUnidad(request, nombre, idunidad):
    '''
    Pagina para mostrar la Unidad

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :param idmateria: id de la materia seleccionada por el usuario
    :return: pagina mostrando detalles de la materia
    '''

    # Valido la sesion del usuario
    validated, rol = validar_usuario(nombre)

    response_unidades = {'Items': [{'idUnidad': '1', 'Descriptor': 'Repaso', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostrarunidad.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                                     'idunidad': idunidad,
                                                     'response_unidades': response_unidades['Items']
                                                                  })


def mostrarActFormacionPractica(request, nombre, idactformacionpractica):
    '''
    Pagina para mostrar Acta de Formacion Practica

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :param idactformacionpractica: id del acta de formacion practica seleccionada por el usuario
    :return: pagina mostrando detalles de la materia
    '''

    # Valido la sesion del usuario
    validated, rol = validar_usuario(nombre)

    response_act_formacion = {'Items': [{'idActFormacionPractica': '1', 'Descriptor': 'TP 1', 'idContenidoCurricular': 1}], 'Count': 1, 'ScannedCount': 1}

    return render(request, 'pg/mostraractformacionpractica.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                            'response_act_formacion': response_act_formacion['Items'],
                            'idactformacionpractica': idactformacionpractica,
                                                                  })


def crearCompetencia(request, nombre, idplan):
    '''
    Pagina para crear una nueva Competencia

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :param idplan: idplan del Plan de Estudios seleccionado
    :return: pagina mostrando detalles de la materia
    '''

    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
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
    '''
    Pagina para mostrar todas las Competencias

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :return: pagina mostrando detalles de la materia
    '''

    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
    validated, rol = validar_usuario(nombre)

    # Busco todas las Competencias
    df = buscar_db('competencia')

    # Parseo el DataFrame al formato JSON
    json_records = df.reset_index().to_json(orient='records')
    competencias_json = json.loads(json_records)

    return render(request, 'pg/mostrarcompetencias.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status, 'competencias': competencias_json})


def mostrarCompetenciaDetalle(request, nombre, idcompetencia):
    '''
    Pagina para mostrar el detalle de la Competencia seleccionada

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :param idcompetencia: idcompetencia de la Competencia elegida
    :return: pagina mostrando detalles de la materia
    '''

    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
    validated, rol = validar_usuario(nombre)

    df = buscar_db_id('competencia', 'idcompetencia', idcompetencia)

    # Parseo el DataFrame al formato JSON
    json_records = df.reset_index().to_json(orient='records')
    competencias_json = json.loads(json_records)

    df = buscar_db_id('capacidades', 'idcompetencia', idcompetencia)

    # Parseo el DataFrame al formato JSON
    json_records = df.reset_index().to_json(orient='records')
    capacidades_json = json.loads(json_records)

    return render(request, 'pg/mostrarcompetenciadetalle.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol,
                                            'status': status,
                                            'competencias': competencias_json,
                                            'capacidades': capacidades_json})


def crearCapacidad(request, nombre, idcompetencia):
    '''
    Pagina para crear una nueva Capacidad

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :param idcompetencia: idcompetencia de la Competencia elegida
    :return: pagina mostrando detalles de la materia
    '''

    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
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
    '''
    Pagina para crear una nueva Unidad

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :param idcontenidocurricular: idcontenidocurricular de la Unidad elegida
    :return: pagina mostrando detalles de la materia
    '''

    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
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
    '''
    Pagina para crear una nueva Acta

    :param request: solicitud de mostrar pagina
    :param nombre: nombre del usuario recibido por el contexto
    :param idcontenidocurricular: idcontenidocurricular de la Unidad elegida
    :return: pagina mostrando detalles de la materia
    '''

    # Valido el estado de los servicios
    status = checkStatus()

    # Valido la sesion del usuario
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