from utils import load_data, load_template, add_to_json, build_response, remove_from_json, edit_from_json
import urllib
import json

def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    print(request)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        print(corpo)
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            print(chave_valor)
            split_chave_valor = chave_valor.split('=')
            split_novo1 = urllib.parse.unquote_plus(split_chave_valor[0])
            split_novo2 = urllib.parse.unquote_plus(split_chave_valor[1])
            params[split_novo1] = split_novo2
        add_to_json(params, "notes.json")
        return build_response(code=303, reason='See Other', headers='Location: /')

        '''elif request.startswith('DELETE'):
            remove_from_json()'''

    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados['titulo'], details=dados['detalhes'], id=dados['id'])
        for dados in load_data('notes.json')
    ]
    notes = '\n'.join(notes_li)

    return build_response(load_template('index.html').format(notes=notes))

def delete_note(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        print(corpo)
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            print(chave_valor)
            split_chave_valor = chave_valor.split('=')
            split_novo1 = urllib.parse.unquote_plus(split_chave_valor[0])
            split_novo2 = urllib.parse.unquote_plus(split_chave_valor[1])
            params[split_novo1] = split_novo2

        remove_from_json(int(params['id']), "notes.json")

    return build_response(code=303, reason='See Other', headers='Location: /')

def edit_note(request, target_id):
    if request.startswith("POST"):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            split_chave_valor = chave_valor.split('=')
            split_novo1 = urllib.parse.unquote_plus(split_chave_valor[0])
            split_novo2 = urllib.parse.unquote_plus(split_chave_valor[1])
            params[split_novo1] = split_novo2

        params['id'] = target_id
        edit_from_json(target_id, params, 'notes.json')
        return build_response(code=303, reason='See Other', headers='Location: /')

    if request.startswith("GET"):
        notes = load_data('notes.json')
        target = None
        for note in notes:
            if note['id'] == target_id:
                target = note
                break

        return build_response(load_template('edit.html').format(title=target['titulo'], details=target['detalhes'], id=target['id']))
