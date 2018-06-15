from flask import Blueprint, render_template, flash, redirect, url_for
from flyflask.models import Env, Mdb, User
from flask_login import login_required, current_user
from flyflask.forms import MigrateForm
import os
import sys

env = Blueprint('env', __name__, url_prefix='/envs')

@env.route('/<int:env_id>')
def detail(env_id):
    env = Env.query.get_or_404(env_id)
    return render_template('env/detail.html', env=env)


@env.route('/<int:env_id>/mdbs/<int:mdb_id>', methods=['GET', 'POST'])
@login_required
def mdb(env_id, mdb_id):
    mdb = Mdb.query.get_or_404(mdb_id)
    versions = ['v1','v2','v3']
    form = MigrateForm()
    form.menu_id.choices = [(v.id, v.name) for v in Mdb.query.all()]
    form.rout_str = '/envs/' + str(mdb.env_id) + '/mdbs/' + str(mdb.id)

    if form.validate_on_submit():
        form.migrate()
        flash('脚本更新成功', 'success')
        # return redirect(url_for('front.index'))

    return render_template('env/mdb.html', mdb=mdb, versions=versions, form=form, rout_str=form.rout_str)

# @env.route('/migrate', methods=['GET', 'POST'])
# @login_required
# def migrate():
#     form = MigrateForm()  # obj=current_user
#     if form.validate_on_submit():
        # form.update_profile(current_user)
#         flash('个人信息更新成功', 'success')
#         return redirect(url_for('front.index'))
#     return render_template('env/mdb.html', form=form)

