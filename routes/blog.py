from flask import Blueprint, render_template, request, redirect
import markdown
from models import Post
from routes.utils import admin_required, is_admin

blog_bp = Blueprint("blog", __name__)

@blog_bp.route('/')
def index():
    return render_template("home.html", is_admin=is_admin())

@blog_bp.route("/posts")
def posts():
    posts = Post.all_posts() if is_admin() else Post.public_posts()
    return render_template("posts.html", my_posts=posts, is_admin=is_admin())

@blog_bp.route("/posts/<int:id>")
def post_page(id):
    post = Post.query.get_or_404(id)
    content_html = markdown.markdown(post.content)
    return render_template("post_page.html", content=content_html)

@blog_bp.route("/edit/<id>", methods=["GET", "POST"])
@admin_required
def edit_post(id):
    if id == "new":
        post = Post.create("New post", "", "", "", 0)
        return redirect(f"/edit/{post.id}")
    
    post = Post.query.get_or_404(id)
    if request.method == "POST":
        post.update(
            title=request.form.get('title'),
            content=request.form.get('content'),
            description=request.form.get('description'),
            main_image=request.form.get('image_path'),
            public=1 if request.form.get('public') == "on" else 0
        )
        return redirect(f"/edit/{id}")

    return render_template("writing.html", post=post)

@blog_bp.route("/delete/<int:id>")
@admin_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    post.delete()
    return redirect('/posts')