from flask import request, redirect, url_for, render_template, session, flash
from . import app
from .models import Entry
from .forms import LoginForm
from .base_functions import get_post, add_post, delete
from .decorator import login_required


@app.route('/')
def homepage():
    posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", posts=posts)

@app.route('/draft-posts')
def draft_posts():
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
    return render_template("drafts.html", drafts=drafts)

@app.route('/edit-post/', methods=["GET", "POST"])
@login_required
def new_post():
    get_post()
    if request.method == "POST":
        add_post()
        return redirect((url_for("homepage")))
    return render_template('entry_form.html', form=get_post())


@app.route('/edit-post/<int:id>', methods=["GET", "POST"])
@login_required
def exist_post(id=id):
    get_post(id)
    if request.method == "POST":
        add_post(id)
        return redirect((url_for("homepage")))
    return render_template('update_form.html', form=get_post(), post=Entry.query.filter_by(id=id).first())

@app.route('/delete-post/<int:id>', methods=["POST"])
@login_required
def delete_post(id=id):
    delete(id)
    return redirect((url_for("homepage")))
   # return render_template('delete.html', post=Entry.query.filter_by(id=id).first())


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('homepage'))
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('homepage'))


if __name__ == "__main__":
    app.run(debug=True)
