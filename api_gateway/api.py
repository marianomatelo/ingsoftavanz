
import urllib.request, json
import requests
import pandas as pd
import base64
from dao import Dao
import os


def leer_tabla(tabla):

    headers = {
        'Content-type': 'application/json',
    }

    data = '{"tabla": ' + tabla + '}'

    response = requests.post('https://8luy98fw22.execute-api.us-east-1.amazonaws.com/default/consultar', headers=headers, data=data)

    response = json.loads(response.text)

    return response

    # for key, value in response.items():
    #     if key == 'Items':
    #         usuario = pd.DataFrame(value)
    #
    #         return usuario['nombre'].iloc[0], usuario['cargaHorariaTotal'].iloc[0], usuario['resolucionMinEdu'].iloc[0],\
    #                usuario['cargaHorariaTotal'].iloc[0], usuario['resolucionRectoral'].iloc[0]


def buscar_usuario(tabla, input_usuario, input_password):

    headers = {
        'Content-type': 'application/json',
    }

    data = '{"tabla": ' + tabla + '}'

    response = requests.post('https://8luy98fw22.execute-api.us-east-1.amazonaws.com/default/consultar', headers=headers, data=data)

    usuarios = json.loads(response.text)

    for key, value in usuarios.items():

        if key == 'Items':

            usuario = pd.DataFrame(value)

            a = base64.b64encode(bytes(u'isa2019', "utf-8"))
            b = base64.b64decode(a).decode("utf-8", "ignore")

            if input_usuario == usuario['nombre'].iloc[0] and b == input_password:

                return [usuario['nombre'].iloc[0], usuario['email'].iloc[0],
                        usuario['rol'].iloc[0], usuario['key'].iloc[0]]

            else:

                return []


def buscar_usuario_mfa(tabla, input_usuario):

    headers = {
        'Content-type': 'application/json',
    }

    data = '{"tabla": ' + tabla + '}'

    response = requests.post('https://8luy98fw22.execute-api.us-east-1.amazonaws.com/default/consultar', headers=headers, data=data)

    usuarios = json.loads(response.text)

    for key, value in usuarios.items():

        if key == 'Items':

            usuario = pd.DataFrame(value)

            if input_usuario == usuario['nombre'].iloc[0]:

                return [usuario['nombre'].iloc[0], usuario['email'].iloc[0], usuario['rol'].iloc[0], usuario['key'].iloc[0]]

            else:

                return []


def validar_usuario(nombre):

    dao = connect()

    q = """SELECT usuario, email, rol, id, "password", mfa FROM public.usuarios WHERE usuario = '{}'""".format(nombre)

    df = dao.download_from_query(q)

    if len(df) == 1:
        print('User Validated')

        return True, df['rol'].iloc[0]

    else:
        print('Invalid user')

    return False, 'Guest'


def guardar_db(tabla, fields, datos):

    dao = connect()

    campos = ''

    for i in datos:

        campos = str(campos) + "'" + str(i) + "',"

    query = """ INSERT INTO {} ({}) VALUES ({})""".format(tabla, fields, str(datos)[1:-1])

    dao.run_query(query)


def buscar_db(tabla):

    dao = connect()

    q = """SELECT * FROM {} """.format(tabla)

    return dao.download_from_query(q)


def buscar_db_id(tabla, id_col, id):

    dao = connect()

    q = """SELECT * FROM {} WHERE {} = '{}'""".format(tabla, id_col, id)

    return dao.download_from_query(q)


def connect():

    dao = Dao(host='34.233.129.172', port='18081', user='postgres', password='continente7', db='nano')

    return dao


def write():

    headers = {
        'Content-type': 'application/json',
    }

    data = '{ "author": "Nick", "tip": "Learn by doing", "category": "General" }'

    response = requests.post('https://8luy98fw22.execute-api.us-east-1.amazonaws.com/default/tips', headers=headers, data=data)

    print(response.content)


def delete():

    headers = {
        'Content-type': 'application/json',
    }

    data = '{ "author": "Nick", "date": 1572462564420}'

    response = requests.post('https://8luy98fw22.execute-api.us-east-1.amazonaws.com/default/delete', headers=headers, data=data)


def checkStatus():

    status = True if os.system("ping -c 1 " + '34.233.129.172') is 0 else False

    if status:
        return 'UP'

    else:
        return 'DOWN'
