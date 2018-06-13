from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flyflask.models import Env, User
from flyflask.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required

front = Blueprint('front', __name__)

@front.route('/')
def index():
    return render_template('index.html')


@front.route('/environments')
def environments():
    page = request.args.get('page', default=1, type=int)
    pagination = Env.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('/env/index.html', pagination=pagination)



@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():#and user is not None
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logout!', 'success')
    return redirect(url_for('.index'))

@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('Register Success, please login!', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)





