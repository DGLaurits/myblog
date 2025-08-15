# db_handler.py
from datetime import date
from models import db, Post, Image

def add_post(title, content, description, main_image_path, public):
    current_date = date.today().strftime('%d-%m-%Y')
    post = Post(
        title=title,
        content=content,
        description=description,
        main_image=main_image_path,
        public=public,
        date=current_date
    )
    db.session.add(post)
    db.session.commit()
    return post.id

def update_post(id, title, content, description, main_image_path, public):
    post = Post.query.get(id)
    if post:
        post.title = title
        post.content = content
        post.description = description
        post.main_image = main_image_path
        post.public = public
        post.date = date.today().strftime('%d-%m-%Y')
        db.session.commit()

def update_content(id, content):
    post = Post.query.get(id)
    if post:
        post.content = content
        post.date = date.today().strftime('%d-%m-%Y')
        db.session.commit()

def update_content_by_title(title, content):
    post = Post.query.filter_by(title=title).first()
    if post:
        update_content(post.id, content)

def delete_post(id):
    post = Post.query.get(id)
    if post:
        db.session.delete(post)
        db.session.commit()

def load_public_posts(amount=10):
    return Post.query.filter_by(public=1).limit(amount).all()

def load_all_posts(amount=10):
    return Post.query.limit(amount).all()

def load_post_by_id(id):
    return Post.query.get(id)

# Images
def add_image(file_name, image_data):
    img = Image(file_name=file_name, image=image_data)
    db.session.add(img)
    db.session.commit()

def load_image(id):
    return Image.query.get(id)