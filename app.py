"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Shows home page"""
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/', methods=['POST'])
def add_user():
    """Adds new user to DB... or cancel add"""

    if request.form['add'] == 'add':
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form["image_url"]
        image_url = str(image_url) if image_url else "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
        
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

    return redirect('/')

@app.route('/add-user')
def add_user_form():
    """Generates new user form"""
    return render_template("new-user-form.html")

@app.route('/user-options/<int:user_id>')
def user_details(user_id):
    """View your options and posts for a selected user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id).all() 

    return render_template('user-details.html', user=user, posts=posts)

@app.route('/user-options/<int:user_id>', methods=["POST"])
def handle_option(user_id):
    """Handle edit/delete option selected on user options"""
    user = User.query.get_or_404(user_id)
    
    if request.form['submit'] == 'edit':
        return render_template('edit.html', user=user)
    elif request.form['submit'] == 'delete':
        db.session.delete(user)
        db.session.commit()
        return redirect('/')
        
@app.route('/user-details/<int:user_id>', methods=["POST"])
def handle_update(user_id):
    """Handle if operator updates user details or cancels"""
    user = User.query.get_or_404(user_id)

    if request.form['update'] == 'save':
        user.first_name = request.form["first_name"] if request.form["first_name"] else user.first_name
        user.last_name = request.form["last_name"] if request.form["last_name"] else user.last_name
        user.image_url = str(request.form["image_url"]) if request.form["image_url"] else "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
        
        db.session.add(user)
        db.session.commit()
    return redirect(f"/user-options/{user_id}") 
    
@app.route('/new-post-form/<int:user_id>')
def show_new_post_form(user_id):
    """Show add new post form"""
    user = User.query.get_or_404(user_id)
 
    return render_template('new-post-form.html', user=user)

@app.route('/new-post-form/<int:user_id>', methods=["POST"])
def add_post(user_id):
    """Handle if post added for user or cancelled"""
    
    if request.form['new'] == 'add':
        now = datetime.now()
        time = now.strftime("%m/%d/%Y, %H:%M:%S")

        title = request.form['title']
        content = request.form['content']
            
        new_post = Post(title=title, content=content, created_at=time, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

    return redirect(f"/user-options/{user_id}")

@app.route('/post-details/<id>')
def show_post_details(id):
    """Show a selected post's details"""
    post = Post.query.filter(Post.id == id).first()
    return render_template('post-details.html', post=post)

@app.route('/edit-post/<int:id>', methods=['POST'])
def handle_edit_choice(id):
    """Cancels, shows edit post form, or deletes post"""
    post = Post.query.filter(Post.id == id).first()
    page=post.info.id

    if request.form['updatePost'] == 'cancel':
        return redirect(f"/user-options/{page}")
    elif request.form['updatePost'] == 'edit':
        return render_template('/edit-post-form.html', post=post)
    elif request.form['updatePost'] == 'delete':
        db.session.delete(post)
        db.session.commit()
        return redirect(f"/user-options/{page}")

@app.route('/edit-post/<int:id>', methods=['POST'])
def edit_post(id):
    """Edit a selected post"""
    post = Post.query.filter(Post.id == id).first()

    if request.form['editPost'] == 'edit':
        post.title = request.form['title'] if request.form["title"] else post.title
        post.content = request.form['content']if request.form["content"] else post.content
            
        db.session.add(post)
        db.session.commit()

    return redirect(f"/user-options/{post.info.id}")   

    


