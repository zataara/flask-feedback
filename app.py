from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm, DeleteForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

### Main routes
@app.route('/')
def root():
    '''Homepage directory'''
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():

    form=UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken')
            return render_template('register.html', form=form)
        flash(f'Welcome ${new_user.username}! Successfully Created Your Account! Please Login.', 'success')
        return redirect('/login')
    else:
        return render_template('register.html', form=form)

@app.route('/users/<username>')
def show_user(username):

    if 'username' not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.get(username)
    form = FeedbackForm()


    return render_template('user.html', user=user, form=form)



@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login_user():

    form=LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user: 
            flash(f'Welcome back {user.username}!', 'primary')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']
    return render_template('login.html', form=form)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    '''Delete user account'''
    if 'username' not in session or username != session['username']:
        flash('Please login first!', 'danger')
        raise Unauthorized()
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    '''Show the feedback form and process adding feedback'''

    if 'username' not in session or username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f'/users/{new_feedback.username}')

    return render_template('/feedback/add.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    '''Update an existing feedback'''
    feedback = Feedback.query.get(feedback_id)

    if 'username' not in session or feedback.username != session['username']:
            raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f'/users/{feedback.username}')
    return render_template('/feedback/edit.html', form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    
    feedback = Feedback.query.get(feedback_id)
    
    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f'/users/{feedback.username}')




