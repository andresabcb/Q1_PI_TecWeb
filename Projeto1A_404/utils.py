import os
import json

def extract_route(request):
    # request é uma string
    lista_split = request.split()
    i = len(request)-1
    route = lista_split[1][1:i]
    return route

def read_file(path):
    # path é um caminho
    filename, file_extension = os.path.splitext('/path/to/somefile.ext')
    extensions_list = [".txt",".html",".css",".js"]
    if file_extension in extensions_list:
        # ler file e devolver uma string
        # abrindo e lendo o arquivo
        file = open(path, "rt")
        fileread = file.read()
        return fileread
    else:
        file = open(path, "rb")
        fileread = file.read()
        return fileread

def load_data(path):
    file_path = str('data/'+path)
    with open(file_path,"rt") as file:
        return json.load(file)

def load_template(name_file):
    path = str("templates/"+name_file)
    with open(path,"rt") as file:
        file_string = str(file.read())
        return file_string

def find_last_id(notes):
    last_id = 0
    for note in notes:
        if note['id'] > last_id:
            last_id = note['id']
    return last_id

def add_to_json(params, path):
    load = load_data(path)
    last_id = find_last_id(load)
    params['id'] = last_id + 1
    load.append(params)
    file_path = str('data/'+path)
    with open(file_path,"wt") as file:
        return json.dump(load, file)

def build_response(body='', code=200, reason='OK', headers=''):
    if headers == "":
        skip = ""
    else:
        skip = "\n"
    if isinstance(body,str):
        body = body.encode()
    return ("HTTP/1.1 "+f"{code} "+reason+skip+headers+"\n\n").encode()+body

# def build_response_404(body='', code=404, reason='OK', headers=''):
#     if headers == "":
#         skip = ""
#     else:
#         skip = "\n"
#     if isinstance(body,str):
#         body = body.encode()
#     return ("HTTP/1.1 "+f"{code} "+reason+skip+headers+"\n\n").encode()+body

# delete function
def remove_from_json(target_id, path):
    load = load_data(path)

    new_notes = []
    for note in load:
        if note['id'] != target_id:
            new_notes.append(note)

    file_path = str('data/'+path)
    with open(file_path,"wt") as file:
        return json.dump(new_notes, file)

# edit function
def edit_from_json(target_id, new_note, path):
    load = load_data(path)

    new_notes = []
    for note in load:
        if note['id'] == target_id:
            new_notes.append(new_note)
        else:
            new_notes.append(note)

    file_path = str('data/'+path)
    with open(file_path,"wt") as file:
        return json.dump(new_notes, file)
