from pathlib import Path
from database import Database
from database import Note
import json

def extract_route(request):
    lines = request.split('\n')
    first_line = lines[0]
    parts = first_line.split()
    route = parts[1][1:]
    return route



def read_file(file_path: Path) -> bytes:
    with open(file_path, 'rb') as file:
        content = file.read()
    return content


def load_data():
    db = Database('banco')

    notes = db.get_all()
    
    return notes

def load_template(filename):
    filepath = "templates/"+filename
    with open(filepath, 'r') as file:
        content = file.read()
    return content

def add_annotation_to_notes(titulo, detalhes):
  """
  Adiciona uma anotação ao arquivo notes.json.

  Args:
    titulo: O título da anotação.   
    detalhes: A descrição da anotação.

  Returns:
    None.
  """
  db = Database('banco')

  db.add(Note(title=titulo, content=detalhes))
  
#   with open("data/notes.json", "r") as f:
#     notes = json.load(f)

#   with open("data/notes.json", "w") as f:
#     json.dump(notes, f, indent=2)

def build_response(body='', code=200, reason='OK', headers=''):
    if body:
        response = "HTTP/1.1 {} {}\n\n{}".format(code, reason, body)
    elif headers:
        response = "HTTP/1.1 {} {}\n{}\n\n".format(code, reason, headers)
    else:
        response = "HTTP/1.1 {} {}\n\n".format(code, reason)
    return response.encode()

