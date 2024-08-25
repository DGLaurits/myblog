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

add_project("This is another test",
            'projects/example.md',
            'Here is a test being described in the most descriptive way possible. No one can describe it better in any way.',
            'https://cdn.britannica.com/92/212692-050-D53981F5/labradoodle-dog-stick-running-grass.jpg')