from django.shortcuts import render, redirect
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
from api_gateway.api import buscar_usuario, buscar_usuario_mfa


def index(request):

    # if request.user.is_authenticated:
    #     usuario = User.objects.filter(name=request.user)[0]
    #
    #     if usuario.rol == '1':
    #         rol = 'admin'

    # return render(request, 'pg/index.html', {'title': 'Bienvenido', 'rol': rol})

    return render(request, 'pg/index.html', {'title': 'Bienvenido'})


def mfa(request, nombre):

    usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)

    if len(usuario) > 0:
        print('Usuario validado')
        nombre = usuario[0]
        email = usuario[1]
        clave_mfa = usuario[3]

    if request.method == 'POST':

        if request.POST['clave_multifactor'] == clave_mfa:

            print('MFA Validado')

            return redirect('menu', nombre=nombre)

    form = keyForm()
    htmly = get_template('pg/Email.html')
    d = {'username': nombre, 'clave': clave_mfa}
    subject, from_email, to = 'ISA Clave MFA', 'trqarg@gmail.com', email
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return render(request, 'pg/mfa.html', {'form': form, 'title': 'MFA'})


def menu(request, nombre):

    usuario = buscar_usuario_mfa(tabla='usuarios', input_usuario=nombre)

    if len(usuario) > 0:
        print('Usuario validado')
        nombre = usuario[0]
        rol = usuario[2]

    else:
        print('Usuario invalido')

    return render(request, 'pg/menu.html', {'title': 'Bienvenido', 'nombre': nombre, 'rol': rol})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            nuevo_usuario = User(rol=request.POST['rol'], name=request.POST['username'],
                                 email=request.POST['email'], password=request.POST['password1'])
            nuevo_usuario.save()

            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'pg/register.html', {'form': form, 'title': 'Reqister'})


def Login(request):
    if request.method == 'POST':

        usuario = buscar_usuario(tabla='usuarios', input_usuario=request.POST['username'], input_password=request.POST['password'])

        if len(usuario) > 0:
            print('Usuario validado')
            nombre = usuario[0]
            return redirect('mfa', nombre=nombre)

        else:
            print('Usuario invalido')
            messages.info(request, f'Error: Intente log in nuevamente')

        # user = authenticate(request, username=username, password=password)
        #
        # if user is not None:
        #     form = login(request, user)
        #     return redirect('mfa')
        # else:
        #     messages.info(request, f'Error: Intente log in nuevamente')

    form = AuthenticationForm()
    return render(request, 'pg/login.html', {'form': form, 'title': 'Log In'})


# def dataset(request):
#
#     if request.user.is_authenticated:
#
#         dataset_table = datasetTable(Dataset_Meta.objects.all())
#
#         if request.method == 'POST':
#
#             name = None
#             description = None
#             problem = None
#             frequency = None
#             file = None
#
#             name = request.POST.get('name')
#
#             description = request.POST.get('description')
#
#             if int(request.POST.get('problem')) == 1:
#                 problem = 'regression'
#             elif int(request.POST.get('problem')) == 2:
#                 problem = 'classification'
#
#             if int(request.POST.get('frequency')) == 1:
#                 frequency = 'month'
#             elif int(request.POST.get('frequency')) == 2:
#                 frequency = 'week'
#             elif int(request.POST.get('frequency')) == 3:
#                 frequency = 'day'
#             elif int(request.POST.get('frequency')) == 4:
#                 frequency = 'hour'
#             elif int(request.POST.get('frequency')) == 5:
#                 frequency = 'minute'
#
#             files = request.FILES.getlist('file')
#
#             for f in files:
#                 df = pd.read_csv(f)
#
#             dataset = Dataset_Meta()
#             dataset.name = name
#             dataset.description = description
#             dataset.problem = problem
#             dataset.frequency = frequency
#             dataset.user = request.user
#             dataset.last_mod = datetime.today()
#
#             dataset.save()
#
#             ### Upload dataset to his table ###
#             dm = DataManager()
#             dm.dao.upload_from_dataframe(df, 'pg_dataset_{}'.format(dataset.pk), if_exists='replace')
#
#             return redirect(reverse('index'))
#
#         return render(request, 'pg/datasets.html', {'form': UploadsForm(), 'dataset_table': dataset_table})
#
#
# def playground(request):
#
#     if request.user.is_authenticated:
#
#         if request.method == 'POST':
#
#             model = None
#             clean = None
#             scaling = None
#             training = None
#             params = None
#
#             if int(request.POST.get('model')) == 1:
#                 model = 'XGBoost'
#             elif int(request.POST.get('model')) == 2:
#                 model = 'LSTM'
#             else:
#                 pass
#
#             if int(request.POST.get('cleaning_method')) == 1:
#                 clean = 'no'
#             elif int(request.POST.get('cleaning_method')) == 2:
#                 clean = 'cleansmooth'
#             elif int(request.POST.get('cleaning_method')) == 3:
#                 clean = 'clean'
#             elif int(request.POST.get('cleaning_method')) == 4:
#                 clean = 'smooth'
#             else:
#                 pass
#
#             if int(request.POST.get('scaling_method')) == 1:
#                 scaling = 'no'
#             elif int(request.POST.get('scaling_method')) == 2:
#                 scaling = 'minmax'
#             elif int(request.POST.get('scaling_method')) == 3:
#                 scaling = 'std'
#             else:
#                 pass
#
#             if int(request.POST.get('training_method')) == 1:
#                 training = 'bayopt'
#             elif int(request.POST.get('training_method')) == 2:
#                 training = 'grids'
#             elif int(request.POST.get('training_method')) == 3:
#                 training = 'finetune'
#
#                 params = str(request.POST.get('max_depth')) + ';' + str(request.POST.get('subsample'))
#             else:
#                 pass
#
#             dataset = Dataset_Meta.objects.get(id=request.POST.get('dataset'))
#
#             run_description = request.POST.get('run_description')
#
#
#             # ### SEND TO DAEMON ###
#             task = Daemon(dataset_id=dataset.id, name=dataset.name, dataset_description=dataset.description,
#                             run_description=run_description, problem=dataset.problem,
#                             frequency=dataset.frequency, user=str(request.user.username), status='waiting',
#                             model=model, clean=clean, scaling=scaling, training=training, params=params)
#             task.save()
#
#             daemon.run_daemon()
#
#             return redirect(reverse('index'))
#
#         return render(request, 'pg/playground.html', {'form': MessageForm()})
#
#
# def analyzer(request):
#
#     if request.user.is_authenticated:
#
#         model = None
#         run_name = None
#
#         if request.method == 'POST':
#
#             run = Daemon.objects.get(id=request.POST.get('run'))
#
#             run_name = run.name
#             dataset_name = run.name
#             model = run.model
#             clean = run.clean
#             scaling = run.scaling
#             training = run.training
#             params = run.params
#
#             return render(request, 'pg/analyzer_filtered.html', {'form': AnalyzerForm(), 'run_name': run_name,
#                                                                  'dataset_name': dataset_name, 'model': model,
#                                                                  'clean': clean, 'scaling': scaling, 'training': training,
#                                                                  'params': params})
#
#     return render(request, 'pg/analyzer.html', {'form': AnalyzerForm()})