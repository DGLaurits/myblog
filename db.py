
import sqlite3
from datetime import date

connect = sqlite3.connect('database.db')
connect.row_factory = sqlite3.Row
cursor = connect.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL, description TEXT NOT NULL, main_image TEXT NOT NULL, date TEXT DEFAULT "21-08-2024");')


def add_project(title: str, content: str, description: str, main_image_path: str):
    current_date = date.today().strftime('%d-%m-%Y')

    cursor.execute('INSERT INTO projects (title, content, description, main_image, date) VALUES (?, ?, ?, ?, ?)', (title, content, description, main_image_path, current_date))
    connect.commit()

def update_content(id: str, content: str):
    current_date = date.today().strftime('%d-%m-%Y')
    cursor.execute("UPDATE projects SET content = ?, date = ? WHERE id = ?", (content, current_date, id))
    connect.commit()

def update_content_by_title(title: str, content: str):
    cursor.execute("SELECT id FROM projects WHERE title = ?", (title,))
    id = cursor.fetchone()
    update_content(id[0], content)

def delete_project(id: int):
    cursor.execute("DELETE FROM projects WHERE id = ?", (id,))
    connect.commit()

def get_projects(amount: int):
    cursor.execute("SELECT * FROM projects LIMIT ?", str(amount))
    return cursor.fetchall()

def get_project_by_id(id: int):
    cursor.execute("SELECT content FROM projects WHERE id = ?", str(id))
    return cursor.fetchone()[0]