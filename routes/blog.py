from flask import Blueprint, jsonify, render_template, request, redirect, flash

from models import Post, Tag
from routes.utils import admin_required, is_admin
from services.posts import get_post_for_view
from services.render import render_markdown

blog_bp = Blueprint("blog", __name__)


@blog_bp.route('/')
def index():
    latest_posts = Post.public_posts(limit=3)
    return render_template("home.html", latest_posts=latest_posts, is_admin=is_admin())


@blog_bp.route("/posts")
def posts():
    post_list = Post.all_posts() if is_admin() else Post.public_posts()
    return render_template("posts.html", posts=post_list, is_admin=is_admin())


@blog_bp.route("/posts/<int:post_id>")
def post_page(post_id):
    post = get_post_for_view(post_id)
    content_html = render_markdown(post.content)
    return render_template("post_page.html", post=post, content=content_html)


@blog_bp.route("/preview", methods=["POST"])
@admin_required
def preview():
    text = request.get_data(as_text=True)
    return jsonify({"html": render_markdown(text)})


@blog_bp.route("/edit/<post_id>", methods=["GET", "POST"])
@admin_required
def edit_post(post_id):
    if post_id == "new":
        post = Post.create("New post", "", "", "", 0)
        return redirect(f"/edit/{post.id}")

    post = Post.query.get_or_404(post_id)
    all_tags = Tag.query.order_by(Tag.name.asc()).all()
    if request.method == "POST":
        selected_ids = request.form.getlist('tag_ids')
        selected_tags = []
        if selected_ids:
            selected_tags = Tag.query.filter(Tag.id.in_(selected_ids)).all()

        new_tag_name = request.form.get('new_tag_name', '').strip()
        if new_tag_name:
            selected_tags.append(Tag.get_or_create(new_tag_name))

        # Deduplicate while preserving order.
        deduped_tags = []
        seen_ids = set()
        for tag in selected_tags:
            if tag.id not in seen_ids:
                deduped_tags.append(tag)
                seen_ids.add(tag.id)

        if len(deduped_tags) > 6:
            flash("A post can have at most 6 tags.")
            return render_template("writing.html", post=post, all_tags=all_tags)

        post.update(
            title=request.form.get('title'),
            content=request.form.get('content'),
            description=request.form.get('description'),
            main_image=request.form.get('image_path'),
            public=1 if request.form.get('public') == "on" else 0
        )
        post.set_tags(deduped_tags)
        return redirect(f"/edit/{post_id}")

    return render_template("writing.html", post=post, all_tags=all_tags)


@blog_bp.route("/delete/<int:id>")
@admin_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    post.delete()
    return redirect('/posts')
