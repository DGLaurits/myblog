from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import database_handler
import markdown

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    my_projects = database_handler.get_projects(10)
    return render_template("projects.html", my_projects=my_projects)

@app.route("/projects/<id>")
def project_page(id):
    
    content_markdown = database_handler.get_project_by_id(id)
    content_html = markdown.markdown(content_markdown)
    return render_template("project_page.html", content=content_html)

@app.route("/write", methods=["GET", "POST"])
def write_page():
    if request.method == "POST":
        print(request.form.to_dict())
    
    return render_template("writing.html")

if __name__ == "__main__":
    app.run(debug=True)