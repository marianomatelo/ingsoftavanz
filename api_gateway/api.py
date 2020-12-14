
import urllib.request, json
import requests
import pandas as pd
import base64
from dao import Dao
import os
from api_gateway.crypto import decrypt_message


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


def validar_usuario_password(nombre, encrypted_password):

    dao = connect()

    q = """SELECT usuario, email, rol, id, "password", mfa FROM public.usuarios WHERE usuario = '{}'""".format(nombre)

    df = dao.download_from_query(q)

    if len(df) == 1 and decrypt_message(bytes(df['password'].iloc[0], 'utf-8')) == decrypt_message(encrypted_password):

        return True, df['rol'].iloc[0]

    else:
        print('Error Usuario Invalido')

    return False, 'Guest'


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


def validar_mfa(nombre, mfa):

    dao = connect()

    df = dao.download_from_query(
        """SELECT * FROM usuarios WHERE usuario = '{}' AND mfa = '{}'""".format(nombre, mfa))

    if len(df) == 1 and df['mfa'].iloc[0] == mfa:

        return True, df['rol'].iloc[0]

    else:
        print('Error Usuario Invalido')

    return False, 'Guest'


def guardar_mfa(nombre, mfa):

    dao = connect()

    q = """UPDATE usuarios SET mfa = '{}' WHERE usuario = '{}'""".format(mfa, nombre)

    dao.run_query(q)

    df = dao.download_from_query(
        """SELECT email FROM usuarios WHERE usuario = '{}'""".
            format(nombre))

    return df['email'].iloc[0]


def guardar_db(tabla, fields, datos):

    dao = connect()

    campos = ''

    for i in datos:

        campos = str(campos) + "'" + str(i) + "',"

    query = """ INSERT INTO {} ({}) VALUES ({})""".format(tabla, fields, str(datos)[1:-1])

    dao.run_query(query)


def buscar_db(tabla):

    dao = connect()

    q = """SELECT * FROM {} ORDER BY 1""".format(tabla)

    return dao.download_from_query(q)


def buscar_db_id(tabla, id_col, id):

    dao = connect()

    q = """SELECT * FROM {} WHERE {} = '{}'""".format(tabla, id_col, id)

    return dao.download_from_query(q)


def chequeo_existencia(tabla, idplan, nombreMateria):

    dao = connect()

    query = """ SELECT idplan, nombre FROM public.{} WHERE idplan = '{}' AND nombre = '{}'""".format(tabla, idplan, nombreMateria)

    df = dao.download_from_query(query)

    if len(df) > 0:
        return True

    else:
        return False


def get_data(tabla, nombreMateria):

    dao = connect()

    query = """ SELECT idmateria, descripcion FROM public.{} WHERE nombre = '{}'""".format(tabla, nombreMateria)

    df = dao.download_from_query(query)

    return df['idmateria'].iloc[0], df['descripcion'].iloc[0]


def connect():

    if os.name == 'nt':

        dao = Dao(host='34.233.129.172', port='18081', user='postgres', password='continente7', db='nano')

    else:

        dao = Dao(host='localhost', port='18081', user='postgres', password='continente7', db='nano')

    return dao


def write():

    headers = {
        'Content-type': 'application/json',
    }

    data = '{ "author": "Nick", "tip": "Learn by doing", "category": "General" }'

    response = requests.post('https://8luy98fw22.execute-api.us-east-1.amazonaws.com/default/tips', headers=headers, data=data)


def delete():

    headers = {
        'Content-type': 'application/json',
    }

    data = '{ "author": "Nick", "date": 1572462564420}'

    response = requests.post('https://8luy98fw22.execute-api.us-east-1.amazonaws.com/default/delete', headers=headers, data=data)


def log_acceso(nombre, rol):

    dao = connect()

    q = """INSERT INTO logs (usuario, rol, fecha, accion) VALUES ('{}', '{}', '{}', '{}')""".format(nombre, rol, pd.to_datetime('today'), 'acceso autenticado')

    dao.run_query(q)


def log_creacion(nombre, rol, tabla):

    dao = connect()

    q = """INSERT INTO logs (usuario, rol, fecha, accion, recurso) VALUES ('{}', '{}', '{}', '{}', '{}')""".format(nombre, rol, pd.to_datetime('today'), 'creo un nuevo registro', tabla)

    dao.run_query(q)


def checkStatus():

    status = True if os.system("ping -c 1 " + '34.233.129.172') is 0 else False

    if status:
        return 'DOWN'

    else:
        return 'UP'
