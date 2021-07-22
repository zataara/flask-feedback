from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import UserForm


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

        db.session.add(new_user)
        db.session.commit()
        # try:
        #     db.session.commit()
        # except IntegrityError:
        #     form.user.errors.append('Username taken')
        #     return render_template('register.html', form=form)
        session['user_id'] = new_user.id 
        flash(f'Welcome ${new_user.username}! Successfully Created Your Account!', 'success')
        return redirect('secret.html')
    else:
        return render_template('register.html', form=form)