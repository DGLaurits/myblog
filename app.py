from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import db
import markdown
import os

IMAGE_FOLDER = 'static/images/uploads'
ALLOWED_IMG_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "HELLOHELO"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG_EXTENSIONS

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

@app.route("/write", methods=["GET", "POST"])
def write_page():
    if request.method == "POST":
        title = request.form.getlist()['title']
        description = request.form.getlist()['description']
        content = request.form.getlist()['content']
        image_path = request.form.getlist()['image_path']
        db.add_project(title, content, description, "static/images/projects/mandelbrot-visualizer.png", image_path)
        return redirect("/projects")
    
    return render_template("writing.html")

@app.route("/images", methods=['GET', 'POST'])
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