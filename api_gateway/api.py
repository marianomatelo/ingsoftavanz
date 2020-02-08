
import urllib.request, json
import requests
import pandas as pd
import base64


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

    url = 'https://stackoverflow.com/'
    response_code = 200

    r = requests.get(url)

    if r.status_code != response_code:
        return 'DOWN'
    else:
        return 'UP'


if __name__ == '__main__':

    leer_tabla(tabla='PlanEstudios')

    # usuario = buscar_usuario(tabla='usuarios', input_usuario='Mariano', input_password='Continente7')
    #
    # if len(usuario) > 0:
    #     print('Usuario validado')
    #     nombre = usuario[0]
    #     email = usuario[1]
    #     rol = usuario[2]
    #     key = usuario[3]
    #
    # else:
    #     print('Usuario invalido')

    # write()

    # delete()

    # checkStatus()