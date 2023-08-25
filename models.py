"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String,
                           nullable=True,
                           default='Unknown')
    
    last_name = db.Column(db.String,
                           nullable=True,
                           default='Unknown')
    
    image_url = db.Column(db.String,
                          nullable=True)
    
    def whole_name(self):
        "Display first and last name"
        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):
    """Posts"""
    
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
               primary_key=True,
               autoincrement=True)
        
    title = db.Column(db.String(50),
                      nullable=False)
    
    content = db.Column(db.String,
                        nullable=False)
    
    created_at = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    info = db.relationship('User', backref='posts')

class Tag(db.Model):
    """Tags"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True)
    
    name = db.Column(db.String,
                   unique=True,
                   nullable=False)
    
    posts = db.relationship('Post', secondary="post_tags", backref="tags")

class PostTag(db.Model):
    """Relationship table"""

    __tablename__ = 'post_tags'

    post_id = id = db.Column(db.Integer,
                   db.ForeignKey("posts.id"),
                   primary_key=True
                   )
    
    tag_id = id = db.Column(db.Integer,
                  db.ForeignKey("tags.id"),
                  primary_key=True
                  )
    