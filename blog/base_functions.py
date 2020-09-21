from . import db
from .models import Entry
from .forms import EntryForm
from flask import flash

def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
       if session.get('logged_in'):
           return view_func(*args, **kwargs)
       return redirect(url_for('login', next=request.path))
   return check_permissions

def get_post(id=None):
    if id:
        post = Entry.query.filter_by(id=id).first()
        form = EntryForm(data={
            'title': post.title,
            'body': post.body,
            'is_published': post.is_published})
    else:
        form = EntryForm()
    return form

def add_post(id=None):
    if id:
        post = Entry.query.filter_by(id=id).first()
        form = EntryForm(data={
            'title': post.title,
            'body': post.body,
            'is_published': post.is_published})
        post.title = form.title.data
        post.body = form.body.data
        post.is_published = form.is_published.data
        if form.is_published.data:
            flash(f'Post "{form.title.data.upper()}" updated!')
        else:
            flash('Required box not checked. Post not added.')
    else:
        form = EntryForm()
        new_post = Entry(title=form.title.data, body=form.body.data, is_published=form.is_published.data)
        db.session.add(new_post)
        if form.is_published.data:
            flash(f'New post "{form.title.data.upper()}" added!')
        else:
            flash('Required box not checked. Post not added.')
    db.session.commit()

def delete(id):
    ids = []
    posts = Entry.query.all()
    for post in posts:
        ids.append(post.id)
    if id in ids:
        post_to_delete = Entry.query.filter_by(id=id).first()
        db.session.delete(post_to_delete)
        db.session.commit()
        flash(f'Post "{post_to_delete.title}" deleted!')
    else:
        flash('No post!')
