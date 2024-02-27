import sqlite3
from dataclasses import dataclass

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name + '.db')
        self.conn.execute("CREATE TABLE IF NOT EXISTS note(id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL)")

    def add(self, note):
        self.conn.execute("INSERT INTO note (title, content) VALUES (?, ?)", (note.title, note.content))
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute("SELECT id, title, content FROM note")
        objetos_note = []
        for linha in cursor:
            objetos_note.append(Note(id=linha[0], title=linha[1], content=linha[2]))
        return objetos_note
    
    def update(self, entry):
        self.conn.execute("UPDATE note SET title = ?, content = ? WHERE id = ?", (entry.title, entry.content, entry.id))
        self.conn.commit()

    def delete(self, note_id):
        self.conn.execute("DELETE FROM note WHERE id = ?", (note_id,))
        self.conn.commit()

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

    
        