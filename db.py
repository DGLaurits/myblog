import sqlite3
from datetime import date

def add_project(title: str, content: str, description: str, main_image_path: str):
    current_date = date.today().strftime('%d-%m-%Y')

    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO projects (title, content, description, main_image, date) VALUES (?, ?, ?, ?, ?)', (title, content, description, main_image_path, current_date))
    connect.commit()

def update_content(id: str, content: str):
    current_date = date.today().strftime('%d-%m-%Y')
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE projects SET content = ?, date = ? WHERE id = ?", (content, current_date, id))
    connect.commit()

def update_content_by_title(title: str, content: str):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM projects WHERE title = ?", (title,))
    id = cursor.fetchone()
    cursor.close()
    connect.close()
    update_content(id[0], content)

def delete_project(id: int):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ?", (id,))
    connect.commit()

def get_projects(amount: int):
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute("SELECT * FROM projects LIMIT 10")
    return cursor.fetchall()

def get_project_by_id(id: int):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT content FROM projects WHERE id = ?", id)
    return cursor.fetchone()[0]