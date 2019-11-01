
import urllib.request, json
import requests
import pandas as pd


def read_all():

    with urllib.request.urlopen("https://8luy98fw22.execute-api.us-east-1.amazonaws.com/default/tips") as url:
        data = json.loads(url.read().decode())
        data = pd.DataFrame(data)

        for i in range(len(data)):
            date = data['Items'][i]['date']
            author = data['Items'][i]['author']

            print(date, author)


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
    read_all()

    # write()

    # delete()