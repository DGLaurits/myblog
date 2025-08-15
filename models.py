from datetime import date, datetime
from extensions import db

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    main_image = db.Column(db.String(255), nullable=False)
    public = db.Column(db.Integer, default=0)
    date = db.Column(db.String(20), default=datetime.today().strftime('%d-%m-%Y'))
    last_edited = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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

        self.last_edited = datetime.utcnow()  # force update every time

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def public_posts(cls, limit=10):
        return cls.query.filter_by(public=1).limit(limit).all()

    @classmethod
    def all_posts(cls, limit=10):
        return cls.query.limit(limit).all()


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