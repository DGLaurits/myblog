from flask import Blueprint, render_template, request, redirect
import markdown
from models import Post, Image
from routes.utils import admin_required, is_admin

blog_bp = Blueprint("blog", __name__)

@blog_bp.route('/')
def index():
    return render_template("home.html", is_admin=is_admin())

@blog_bp.route("/posts")
def posts():
    posts = Post.all_posts() if is_admin() else Post.public_posts()
    for post in posts:
        print(post.main_image)
    return render_template("posts.html", posts=posts, is_admin=is_admin())

@blog_bp.route("/posts/<int:post_id>")
def post_page(post_id):
    post = Post.query.get_or_404(post_id)
    content_html = markdown.markdown(post.content)
    return render_template("post_page.html", content=content_html)

@blog_bp.route("/edit/<post_id>", methods=["GET", "POST"])
@admin_required
def edit_post(post_id):
    if post_id == "new":
        post = Post.create("New post", "", "", "", 0)
        return redirect(f"/edit/{post.id}")
    
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.update(
            title=request.form.get('title'),
            content=request.form.get('content'),
            description=request.form.get('description'),
            main_image=request.form.get('image_path'),
            public=1 if request.form.get('public') == "on" else 0
        )
        return redirect(f"/edit/{post_id}")
    total_images = Image.query.count()
    print(f"Total images: {total_images}")
    return render_template("writing.html", post=post, total_images=total_images)

@blog_bp.route("/delete/<int:id>")
@admin_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    post.delete()
    return redirect('/posts')