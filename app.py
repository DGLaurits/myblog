from flask import Flask, flash, render_template, request, redirect, url_for, session
from functools import wraps
from werkzeug.utils import secure_filename
import db
import markdown
import os

IMAGE_FOLDER = 'static/images/uploads'
ALLOWED_IMG_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ADMIN_PASS = os.environ['ADMIN_CODE']
SECRET_KEY = os.environ['SECRET_CODE']

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = SECRET_KEY

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if is_admin():
            return f(*args, **kwargs)
        else:
            return "NOT LOGGED IN"
    return wrap

def is_admin():
    return 'admin' in session and session['admin']

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    my_projects = db.get_projects(10)
    return render_template("projects.html", my_projects=my_projects)

@app.route("/projects/<id>")
def project_page(id):
    
    content_markdown = db.get_project_by_id(id)
    content_html = markdown.markdown(content_markdown)
    return render_template("project_page.html", content=content_html)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASS:
            session['admin'] = True
            return redirect('/')
        else:
            return render_template('admin_login.html', message = "INCORRECT PASSWORD")
    return render_template('admin_login.html', is_admin=is_admin())

@app.route('/logout')
def logout():
    if is_admin():
        session['admin'] = False
    return redirect('/')

@app.route("/write", methods=["GET", "POST"])
@admin_required
def write_page():
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        content = request.form.get('content')
        image_path = request.form.get('image_path')
        db.add_project(title, content, description, image_path)
        return redirect("/projects")
    
    return render_template("writing.html")

@app.route("/images", methods=['GET', 'POST'])
@admin_required
def images():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            print("part")
            flash('No file part')
            return redirect('/images')
        file = request.files['file']
        if file.filename == '':
            print("select")
            flash("No selected file")
            return redirect("/images")
        if file and allowed_file(file.filename):
            print("half success")
            filename = secure_filename(file.filename)
            file.save(f"{IMAGE_FOLDER}/{filename}")
        flash("success")
        return redirect("/images")
    
    image_files = os.listdir(IMAGE_FOLDER)
    image_paths = [f"{IMAGE_FOLDER}/{file}" for file in image_files]
    return render_template("images.html", images=image_paths)

if __name__ == "__main__":
    app.run(debug=True)