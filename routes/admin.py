from flask import Blueprint, render_template, redirect, request, session, flash, send_file, url_for
from werkzeug.utils import secure_filename
import os, io, string, random
from models import Image
from routes.utils import admin_required, is_admin

admin_bp = Blueprint("admin", __name__)
ADMIN_PASS = os.environ['ADMIN_CODE']
ALLOWED_IMG_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG_EXTENSIONS

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASS:
            session['admin'] = True
            return redirect('/')
        else:
            return render_template('admin_login.html', message="Wrong password")
    return render_template('admin_login.html', is_admin=is_admin())

@admin_bp.route('/logout', methods=['POST'])
def logout():
    if is_admin():
        session['admin'] = False
    return redirect('/')

@admin_bp.route("/upload_image", methods=['POST'])
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
        Image.create(filename, file.read())
    return redirect("/images")

@admin_bp.route("/get_image/<int:image_id>")
def send_image(image_id):
    image = Image.query.get_or_404(image_id)
    return send_file(io.BytesIO(image.image), mimetype="image/jpeg")

@admin_bp.route('/edit/<int:post_id>/images')
def edit_post_images(post_id):
    page = request.args.get('page', 1, type=int)
    per_page = 6
    images_pagination = Image.query.order_by(Image.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    images = images_pagination.items

    image_list = [{"id": img.id, "src": url_for('admin.send_image', image_id=img.id)} for img in images]

    return {
        "images": image_list,
        "page": page,
        "total_pages": images_pagination.pages
    }