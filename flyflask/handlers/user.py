from flask import Blueprint, render_template, flash, redirect, url_for
from flyflask.models import User
from flask_login import login_required, current_user
from flyflask.forms import UserProfileForm


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/<username>')
def user_index(username):
	user = User.query.filter_by(username=username).first()
	return render_template('user.html', user=user)
	# TODO: add 404.html for none result

# profile
@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserProfileForm(obj=current_user)
    if form.validate_on_submit():
        # form.update_profile(current_user)
        flash('个人信息更新成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('user/profile.html', form=form)
