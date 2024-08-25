import sqlite3
from datetime import date

def add_project(title: str, content_path: str, description: str, main_image_path: str):
    current_date = date.today().strftime('%d-%m-%Y')
    with open(content_path, 'r', encoding='utf-8') as read_file:
        content = read_file.read()

    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO projects (title, content, description, main_image, date) VALUES (?, ?, ?, ?, ?)', (title, content, description, main_image_path, current_date))
    connect.commit()

def update_content(id: str, content_path: str):
    current_date = date.today().strftime('%d-%m-%Y')
    with open(content_path, 'r', encoding='utf-8') as read_file:
        content = read_file.read()

    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE projects SET content = ?, date = ? WHERE id = ?", (content, current_date, id))
    connect.commit()

def update_content_by_title(title: str, content_path: str):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM projects WHERE title = ?", (title,))
    id = cursor.fetchone()
    cursor.close()
    connect.close()
    update_content(id[0], content_path)