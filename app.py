from flask import Flask, flash, render_template, request, redirect, session, send_file
from functools import wraps
from werkzeug.utils import secure_filename
import string, random, os, markdown, io
import db_handler
from models import db, Post, Image

IMAGE_FOLDER = 'static/images/uploads'
ALLOWED_IMG_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ADMIN_PASS = os.environ['ADMIN_CODE']
SECRET_KEY = os.environ['SECRET_CODE']

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = SECRET_KEY

# Configure the database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

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

@app.route("/posts")
def posts():
    if is_admin():
        my_posts = db_handler.load_all_posts(10)
    else:
        my_posts = db_handler.load_public_posts(10)
    for post in my_posts:
        print(post.title, post.date, post.public)
    return render_template("posts.html", my_posts=my_posts, is_admin=is_admin())

@app.route("/posts/<int:id>")
def post_page(id):
    post = db_handler.load_post_by_id(id)
    if not post:
        return "Post not found", 404
    content_html = markdown.markdown(post.content)
    return render_template("post_page.html", content=content_html)

@app.route("/edit/<id>", methods=["GET", "POST"])
@admin_required
def write_page(id):
    if id == "new":
        new_id = db_handler.add_post("New post", "", "", "", 0)
        return redirect(f"/edit/{new_id}")
    
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        content = request.form.get('content')
        image_path = request.form.get('image_path')
        public = 1 if request.form.get('public') == "on" else 0
        db_handler.update_post(id, title, content, description, image_path, public)
        return redirect(f"/edit/{id}")
    
    post = db_handler.load_post_by_id(id)
    if not post:
        return "Post not found", 404
    return render_template("writing.html", post=post)

@app.route("/delete/<int:id>")
@admin_required
def delete(id):
    db_handler.delete_post(id)
    return redirect('/posts')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASS:
            session['admin'] = True
            return redirect('/')
        else:
            return render_template('admin_login.html', message="Wrong password")
    return render_template('admin_login.html', is_admin=is_admin())

@app.route('/logout')
def logout():
    if is_admin():
        session['admin'] = False
    return redirect('/')

@app.route("/upload_image", methods=['POST'])
@admin_required
def post_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/images')
    file = request.files['file']
    if file.filename == '':
        flash("No selected file")
        return redirect("/images")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        fileextension = filename.rsplit('.', 1)[1]
        filename = id_generator() + '.' + fileextension
        db_handler.add_image(filename, file.read())
    return redirect("/images")

@app.route("/get_image/<int:id>")
def send_image(id):
    image = db_handler.load_image(id)
    if not image:
        return "No image with this id"
    return send_file(io.BytesIO(image.image), mimetype="image/jpeg")

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == "__main__":
    app.run(debug=True)