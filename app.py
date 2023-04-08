"""Blogly application."""
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY']="blogly-secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

debug=DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    '''Redirect to list of users'''
    recent_posts = Post.query.order_by(Post.created_at).limit(5).all()
    return render_template('homepage.html', posts = recent_posts)

@app.route('/users')
def users_page():
    '''Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form'''
    all_users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users.html', all_users=all_users)

@app.route('/users/new')
def newUser():
    '''Show an add form for users'''
    return render_template('add-user.html')

@app.route('/users/new', methods=['POST'])
def do_newUser():
    '''Process the add form, adding a new user and going back to /users'''
    f_name = request.form.get('first')
    l_name = request.form.get('last')
    img_url = request.form.get('image')
    if img_url:
       img_url = img_url
    else:
        img_url = None
    
    newUser = User(first_name=f_name, last_name=l_name, image_url=img_url)
    db.session.add(newUser)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def userDetails(user_id):
    '''Show information about the given user. Have a button to get to their edit page, and to delete the user'''
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@app.route('/users/<int:user_id>/edit')
def editUser(user_id):
    '''Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user.'''
    user = User.query.get_or_404(user_id)
    return render_template('edit-profile.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def do_editUser(user_id):
    '''Process the edit form, returning the user to the /users page.'''
    fname = request.form['first']
    lname = request.form['last']
    img = request.form['image']
    
    user = User.query.get_or_404(user_id)
    user.first_name = fname
    user.last_name = lname
    user.image_url = img
    
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def do_deleteUser(user_id):
    '''Delete the user.'''
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/posts/new')
def newPost(user_id):
    '''Show form to add a post for that user'''

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('add-post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def do_newPost(user_id):
    '''Handle add form; add post and redirect to the user detail page'''
    t = request.form.get('title')
    c = request.form.get('content')

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=t, content=c, user_id=user_id, tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    '''Show a post. Show buttons to edit and delete the post'''
    post = Post.query.get_or_404(post_id)
    return render_template('post-details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def editPost(post_id):
    '''Show form to edit a post, and to cancel (back to user page).'''

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit-post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def do_editPost(post_id):
    '''Handle editing of a post. Redirect back to the post view.'''
    post = Post.query.get_or_404(post_id)
    
    post.title = request.form.get('title')
    post.content = request.form.get('content')
    
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def do_deletePost(post_id):
    '''Delete the post.'''

    # Get user_id of the post
    user_id = list(db.session.query(Post.user_id).filter(Post.id==post_id).first())[0]

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/tags')
def show_tags():
    '''Lists all tags, with links to the tag detail page.'''
    
    all_tags = Tag.query.all()
    return render_template('tags.html', all_tags=all_tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    '''Show detail about a tag. Have links to edit form and to delete.'''
    tag = Tag.query.get(tag_id)
    return render_template('tag-details.html', tag=tag)

@app.route('/tags/new')
def newTag():
    '''Shows a form to add a new tag.'''
    return render_template('add-tag.html')

@app.route('/tags/new', methods=['POST'])
def do_newTag():
    '''Process add form, adds tag, and redirect to tag list.'''
    t = request.form.get('name')
    
    new_tag = Tag(name=t)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def editTag(tag_id):
    '''Show edit form for a tag.'''
    tag = Tag.query.get(tag_id)
    return render_template('edit-tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def do_editTag(tag_id):
    '''Process edit form, edit tag, and redirects to the tags list.'''

    t = request.form.get('name')
    
    tag = Tag.query.get_or_404(tag_id)
    tag.name = t

    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def do_deleteTag(tag_id):
    '''Delete a tag.'''

    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")

@app.errorhandler(404)
def page_err_404(error):
    return render_template('404-page.html', err=error),404
