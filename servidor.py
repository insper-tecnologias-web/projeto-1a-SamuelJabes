import socket
from pathlib import Path
from utils import extract_route, read_file, build_response, load_template, load_data
from views import index
from database import Database

db = Database('banco')

CUR_DIR = Path(__file__).parent
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    print('*'*100)
    print(request)

    route = extract_route(request)

    filepath = CUR_DIR / route
    if filepath.is_file():
        response = build_response() + read_file(filepath)
    elif route == '':
        response = index(request)
    elif route.startswith("deletar"):
        id = int(route.split("/")[1])
        db.delete(id)
        response = build_response(code=303, reason='See Other', headers='Location: /')
    elif route.startswith("prova"):
        note_template = load_template('components/note.html')
        notes_li = [
            note_template.format(title=note.title, details=note.content, id=note.id)
            for note in load_data()
        ]
        notes = '\n'.join(notes_li)
        qtd_notes = len(notes_li)
        response = build_response(body=load_template('page.html').format(qtd_notes=qtd_notes))
    else:
        response = build_response(body=load_template('404.html'))

    client_connection.sendall(response)

    client_connection.close()

server_socket.close()