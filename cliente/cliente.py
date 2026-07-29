import requests

def fazer_request_tmdb(url, header, params):
    r = requests.get(url, params=params, headers=header)
    try:
        r.raise_for_status()
        print("Requisição bem-sucedida!")
    except requests.HTTPError as erro:
        print(f"Não foi possível obter uma requisição: {erro}")
        print(f"Código do erro: {r.status_code}")
    else:
        return r.json()

def fazer_request_tmdb_sem_params(url, header):
    r = requests.get(url, headers=header)
    try:
        r.raise_for_status()
        print("Requisição bem-sucedida!")
    except requests.HTTPError as erro:
        print(f"Não foi possível obter uma requisição: {erro}")
        print(f"Código do erro: {r.status_code}")
    else:
        return r.json()