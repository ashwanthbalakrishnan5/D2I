import requests

from pprint import pprint


def convertSVG(path):
    path = path
    url = 'https://api.convertio.co/convert'
    data = '{"apikey": "8b7c46507f50ee876380cf498a6d3d03","input":"upload","outputformat":"svg"}'
    res = requests.post(url,data = data)
    result = res.json()
    id = result['data']['id']
    print(id)
    urlToUpload = f'https://api.convertio.co/convert/{id}/{path}'
    print(urlToUpload)
    res2 = requests.put(urlToUpload)
    result2 = res2.json()
    pprint(result)
    pprint(result2)
