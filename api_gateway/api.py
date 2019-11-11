
import urllib.request, json
import requests
import pandas as pd


def leer_tabla(tabla):

    headers = {
        'Content-type': 'application/json',
    }

    data = '{"tabla": ' + tabla + '}'

    response = requests.post('https://8luy98fw22.execute-api.us-east-1.amazonaws.com/default/consultar', headers=headers, data=data)

    print(response.content)


def buscar_usuario(tabla):

    headers = {
        'Content-type': 'application/json',
    }

    data = '{"tabla": "CodingTips"}'

    response = requests.post('https://8luy98fw22.execute-api.us-east-1.amazonaws.com/default/consultar?tabla={}'.format(tabla), headers=headers)
    print(response.content)
    json_data = json.loads(response.text)
    print(json_data)

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


if __name__ == '__main__':

    # leer_tabla(tabla='usuarios')

    buscar_usuario(tabla='usuarios')

    # write()

    # delete()