import regex


def validate_name(name):
    if not name:
        raise ValueError('Nome inválido.')
    pattern = r'^[\p{L}\'\-\s]+$'
    if not regex.match(pattern, name):
        raise ValueError(
            'Nome inválido. Não use números ou caracteres especiais.')
    name = regex.sub(r'\s+', ' ', name).strip()
    name_parts = name.split()
    prepositions = ['da', 'de', 'do', 'das', 'dos']
    formatted_name = ' '.join([part.capitalize() if part.lower(
    ) not in prepositions else part.lower() for part in name_parts])
    return formatted_name


def validate_cpf(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        raise ValueError('CPF inválido. Deve ter 11 dígitos numéricos.')
    if cpf in ['0' * 11, '1' * 11, '2' * 11, '3' * 11, '4' * 11, '5' * 11, '6' * 11, '7' * 11, '8' * 11, '9' * 11]:
        raise ValueError('CPF inválido. Sequência repetida.')
    sum_ = 0
    for i in range(9):
        sum_ += int(cpf[i]) * (10 - i)
    remainder = sum_ % 11
    digit1 = 0 if remainder < 2 else 11 - remainder
    if int(cpf[9]) != digit1:
        raise ValueError('CPF inválido. Dígito verificador 1 não confere.')
    sum_ = 0
    for i in range(10):
        sum_ += int(cpf[i]) * (11 - i)
    remainder = sum_ % 11
    digit2 = 0 if remainder < 2 else 11 - remainder
    if int(cpf[10]) != digit2:
        raise ValueError('CPF inválido. Dígito verificador 2 não confere.')
    return cpf


def validate_email(email):
    if '@' not in email:
        raise ValueError('Email inválido.')
    return email


def format_text(text):
    return ' '.join(word.capitalize() if word.lower() not in ['da', 'de', 'do', 'das', 'dos'] else word.lower() for word in regex.sub(r'\s+', ' ', text).strip().split())


def validate_address(street, number, complement, neighborhood, zip_code, city, state):
    street = format_text(street)
    neighborhood = format_text(neighborhood)
    city = format_text(city)
    if not all([street, number, neighborhood, zip_code, city, state]):
        raise ValueError(
            'Todos os campos de endereço, exceto complemento, são obrigatórios.')
    if not regex.match(r'^\d{5}-\d{3}$', zip_code):
        raise ValueError('CEP inválido. Deve seguir o formato 00000-000.')
    if not regex.match(r'^[A-Z]{2}$', state):
        raise ValueError(
            'UF inválido. Deve ser composto por duas letras maiúsculas.')
    return street, number, complement, neighborhood, zip_code, city, state
