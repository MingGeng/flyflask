from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, SelectField, ValidationError
from wtforms.validators import Length, Email, EqualTo, Required, Regexp, DataRequired
from flask_wtf.file import FileField, FileRequired
from flyflask.models import db, User, Env, Mdb
from flask import url_for
import os, sys

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(3, 24), Regexp(
        '^[A-Za-z0-9]*$', 0, 'Username must have only letters,  numbers!')])
    email = StringField('Email:', validators=[Required(), Email(
        message='Please input currect email address!')])
    password = PasswordField('Password:', validators=[Required(), Length(
        6, 24, message='Password Length need to between 6 to 24!')])
    repeat_password = PasswordField('Repeat Password:', validators=[
                                    Required(), EqualTo('password')])
    submit = SubmitField('Submit')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exist!')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exist!')


class LoginForm(FlaskForm):
    # email = StringField('Email', validators=[Required(), Email(message='Please input currect email address!')])
    username = StringField('Username', validators=[Required(), Length(3, 24)])
    password = PasswordField('Password', validators=[
                             Required(), Length(6, 24)])
    remember_me = BooleanField('Remember')
    submit = SubmitField('Submit')
    # def validate_email(self, field):
    #     if field.data and not User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email unregistered!')

    def validate_username(self, field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('User unregistered!')

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('Wrong password!')



class MigrateForm(FlaskForm):
    rout_str = ""
    version = SelectField('Version', validators=[Required()], choices=[('0', '全部'), ('1', '待审核'), ('2', '认证成功'), ('3', '认证失败')])
    mdb_id = StringField('mdb_id')
    # mdb = Mdb.query.get_or_404(mdb_id)
    # validators = [Required(), Length(3, 24), Regexp('^[A-Za-z0-9]*$', 0, 'Username must have only letters,  numbers!')]
    # email = StringField('Email:', validators=[Required(), Email(message='Please input currect email address!')])
    # password = PasswordField('Password:', validators=[Required(), Length(6, 24, message='Password Length need to between 6 to 24!')])
    # repeat_password = PasswordField('Repeat Password:', validators=[Required(), EqualTo('password')])
    menu_id = SelectField(label = "所属菜单",validators = [DataRequired("请选择菜单!")], 
    coerce = int, choices = "",render_kw = {"class":"form-control"})

    # def __init__(self, *args, **kwargs):
    #     self.choices = [(v.id, v.name) for v in Env.query.all()]
    #     super().__init__(*args, **kwargs)

    submit = SubmitField('Migrate')




    def migrate(self):
        version = self.version.data
        os.system('echo flyway.user='+self.mdb_id.data+' >> tmp.conf')
        os.system('echo flyway.password=Abcd1234 >> tmp.conf')
        # os.system('./flyway -configFile=/app/flyway-4.2.0/tmp.conf ' + 'migrate')

    #     user.username = self.username.data
    #     user.email = self.email.data
    #     user.password = self.password.data
    #     db.session.add(user)
    #     db.session.commit()
        return version

    # def validate_username(self, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('Username already exist!')

    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email already exist!')


class UserProfileForm(FlaskForm):
    real_name = StringField('姓名', [Required()])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码(不填写保持不变)')
    phone = StringField('手机号')
    work_years = IntegerField('工作年限')
    resume = FileField('上传简历', validators=[FileRequired()])
    submit = SubmitField('提交')

    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('请输入有效的手机号')

    # def upload_resume(self):
    #     f = self.resume.data
    #     filename = self.real_name.data + '.pdf'
    #     f.save(os.path.join(
    #         os.path.abspath(os.path.dirname(__file__)),
    #         'static',
    #         'resumes',
    #         filename
    #     ))
    #     return filename

    # def update_profile(self, user):
    #     user.real_name = self.real_name.data
    #     user.email = self.email.data
    #     if self.password.data:
    #         user.password = self.password.data
    #     user.phone = self.phone.data
    #     user.work_years = self.work_years.data
        # filename = self.upload_resume()
        # user.resume_url = url_for('static', filename=os.path.join('resumes', filename))
        # db.session.add(user)
        # db.session.commit()
