import re
from datetime import datetime
from extensions import db

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    main_image = db.Column(db.String(255), nullable=False)
    public = db.Column(db.Integer, default=0, nullable=False)
    date = db.Column(db.String(20), default=datetime.today().strftime('%d-%m-%Y'), nullable=False)
    last_edited = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    tags = db.relationship('Tag', secondary=post_tags, back_populates='posts')

    @classmethod
    def create(cls, title, content, description, main_image, public=0):
        post = cls(
            title=title,
            content=content,
            description=description,
            main_image=main_image,
            public=public,
            date=datetime.today().strftime('%d-%m-%Y')
        )
        db.session.add(post)
        db.session.commit()
        return post

    def update(self, title=None, content=None, description=None, main_image=None, public=None):
        if title is not None: self.title = title
        if content is not None: self.content = content
        if description is not None: self.description = description
        if main_image is not None: self.main_image = main_image
        if public is not None: self.public = public

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def set_tags(self, tags):
        self.tags = tags
        db.session.commit()

    @classmethod
    def public_posts(cls, limit=10):
        return cls.query.filter_by(public=1).limit(limit).all()

    @classmethod
    def all_posts(cls, limit=10):
        return cls.query.limit(limit).all()

    @property
    def hero_image_url(self):
        """URL for list/card thumbnails. Supports /get_image/<id>, numeric id, or external URL."""
        value = (self.main_image or '').strip()
        if not value:
            return None
        if value.startswith('/get_image/') or value.startswith('http://') or value.startswith('https://'):
            return value
        if value.isdigit():
            return f'/get_image/{value}'
        return value


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), unique=True, nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)

    @classmethod
    def create(cls, file_name, image_bytes):
        img = cls(file_name=file_name, image=image_bytes)
        db.session.add(img)
        db.session.commit()
        return img

    @property
    def url_path(self):
        return f'/get_image/{self.id}'


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(60), unique=True, nullable=False)
    posts = db.relationship('Post', secondary=post_tags, back_populates='tags')

    @staticmethod
    def normalized_name(name: str) -> str:
        return re.sub(r'\s+', ' ', name.strip())

    @staticmethod
    def slugify(name: str) -> str:
        normalized = Tag.normalized_name(name).lower()
        slug = re.sub(r'[^a-z0-9]+', '-', normalized).strip('-')
        return slug or 'tag'

    @classmethod
    def _next_available_slug(cls, base_slug: str) -> str:
        slug = base_slug
        index = 2
        while cls.query.filter_by(slug=slug).first() is not None:
            slug = f'{base_slug}-{index}'
            index += 1
        return slug

    @classmethod
    def get_or_create(cls, name: str):
        normalized = cls.normalized_name(name)
        existing = cls.query.filter(db.func.lower(cls.name) == normalized.lower()).first()
        if existing:
            return existing

        base_slug = cls.slugify(normalized)
        slug = cls._next_available_slug(base_slug)
        tag = cls(name=normalized, slug=slug)
        db.session.add(tag)
        db.session.commit()
        return tag