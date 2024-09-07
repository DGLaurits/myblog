
import sqlite3
from datetime import date

connect = sqlite3.connect('database.db', check_same_thread=False)
connect.row_factory = sqlite3.Row
cursor = connect.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL, description TEXT NOT NULL, main_image TEXT NOT NULL, date TEXT DEFAULT "21-08-2024");')
cursor.execute('CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, file_name TEXT NOT NULL UNIQUE, image BLOB NOT NULL);')
cursor.close()

def add_project(title: str, content: str, description: str, main_image_path: str):
    cursor = connect.cursor()
    current_date = date.today().strftime('%d-%m-%Y')

    cursor.execute('INSERT INTO projects (title, content, description, main_image, date) VALUES (?, ?, ?, ?, ?)', (title, content, description, main_image_path, current_date))
    connect.commit()
    cursor.close()

def update_content(id: str, content: str):
    cursor = connect.cursor()
    current_date = date.today().strftime('%d-%m-%Y')
    cursor.execute("UPDATE projects SET content = ?, date = ? WHERE id = ?", (content, current_date, id))
    connect.commit()
    cursor.close()

def update_content_by_title(title: str, content: str):
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM projects WHERE title = ?", (title,))
    id = cursor.fetchone()
    update_content(id[0], content)
    cursor.close()

def delete_project(id: int):
    cursor = connect.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ?", (id,))
    connect.commit()
    cursor.close()

def load_projects(amount: int):
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM projects LIMIT ?", (str(amount), ))
    result = cursor.fetchall()
    cursor.close()
    return result

def load_project_by_id(id: int):
    cursor = connect.cursor()
    cursor.execute("SELECT content FROM projects WHERE id = ?", (str(id), ))
    result = cursor.fetchone()[0]
    cursor.close()
    return result


# Storing and loading images

def add_image(file_name: str, image: str):
    cursor = connect.cursor()
    cursor.execute("INSERT INTO images (file_name, image) VALUES (?, ?)", (file_name, image))
    connect.commit()
    cursor.close()

def load_image(id: int):
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM images WHERE id = ?", (str(id), ))
    result = cursor.fetchone()
    cursor.close()
    return result
