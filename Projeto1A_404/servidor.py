# socket é usado para lidar chamadas de rede em baixo nível
import socket
from pathlib import Path
from utils import extract_route, read_file, build_response, load_template
from views import index, delete_note, edit_note

CUR_DIR = Path(__file__).parent
# definem o endereço do servidor
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

# f strings - forma mais simples de fazer o format
print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

while True:
  # accept trava a execução do programa até que receba uma requisição
  client_connection, client_address = server_socket.accept()

  # indicamos que queremos ler no máximo 1024 bytes
  # resultado é um valor do tipo bytes
  # convertemos ele para uma string utilizando o decode()
  request = client_connection.recv(1024).decode()
  print(request)

  route = extract_route(request)
  filepath = CUR_DIR / route
  if filepath.is_file():
    response = build_response(read_file(filepath))
  elif route == '':
    response = index(request)
  elif route == 'deletar':
    response = delete_note(request)
  elif route.startswith('edit'):
    response = edit_note(request, int(route.split('/')[1]))
  else:
    response = build_response(load_template('404.html'))
  client_connection.sendall(response)


  # sem essas duas quebras de linha, o Hello World seria considerado parte do cabeçalho (header)
  # response = 'HTTP/1.1 200 OK\n\nHello World'
  # client_connection.sendall(RESPONSE_TEMPLATE.encode())

  client_connection.close()
server_socket.close()
