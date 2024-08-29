import requests


def get_address(cep):
    cep = cep.replace('-', '')

    if len(cep) != 8 or not cep.isdigit():
        return None

    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        response = requests.get(url)
        response.raise_for_status()

        address = response.json()

        if 'erro' in address:
            return None

        return address

    except requests.RequestException:
        return None
