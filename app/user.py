import logging
import random
import string
import smtplib
from email.mime.text import MIMEText
from os import environ
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash
)
from flask_login import (
    login_user,
    current_user,
    login_required,
    logout_user
)
from plugins import (
    db,
    cache,
    login_manager,
)
from app.models import User

user_bp = Blueprint('user_bp', __name__, template_folder='./templates/user')

# config about login user
# https://flask-login.readthedocs.io/en/latest/
# here is an example:
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
# Note: remenber config `SESSION_COOKIE_NAME` well.
login_manager.login_view='/login'

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(int(user_id))
    else:
        return None


def generate_code():
    return ''.join(random.sample(string.digits, 6))

def send_email(receiver, html_content=None):
    sender = environ.get('MAIL_USERNAME')
    msg = MIMEText(html_content, 'html') 
    msg['subject'] = '路课网验证码' 
    msg['from'] = sender
    msg['to'] = receiver  
    try:
        # Port of SMTP_SSL service is 465
	    s = smtplib.SMTP_SSL(environ.get('MAIL_SERVER'), 465)  
	    s.login(sender, environ.get('MAIL_PASSWORD'))  
	    s.sendmail(sender, receiver, msg.as_string().encode("utf-8"))
	    return 'Success'
    except smtplib.SMTPException:
	    return 'Failed'


@user_bp.route('/code', methods=['GET', 'POST'])
def sendcode():
    '''
    Send SMS code using to `phone`.
    '''
    if request.method == 'POST':
        email = request.form.get('email')
        if email is None:
            return jsonify(
                message='Error',
                code=206
            )
        code = generate_code()
        send_email(email, f'<p>你的验证码是:</p><h1>{code}</h1> 十分钟内有效')
        cache.set(email, code)
        return jsonify(
            message=f'Success',
            code=200
        )


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Register: when the user is not registerted.
    Sigin in: when the user is already registed.
    '''
    if request.method == 'POST':
        email = request.form.get('email')
        code = request.form.get('code')
        password = request.form.get('password')
        if code == cache.get(email):
            user = User.query.filter(User.email == email).first()
            if user is None:
                user = User(email=email, password=password)
                db.session.add(user)
                db.session.commit()
                db.session.refresh(user)
            login_user(user)
            return redirect('/user/{user.id}')
        else:
            return jsonify(
                code=406,
                message="验证码错误"
            )

    return render_template(
        'register.html',
        title='欢迎加入'
        )

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email == email).first()

        if not user:
            flash("未注册的邮箱, 请在此注册")
            return redirect('/register')
        
        if not user.check_password(password):
            flash("密码错误")
            return redirect('/login')
        login_user(user)
        return redirect(f'/user/{user.id}')
    else:
        return render_template(
            'login.html',
            title='欢迎回来'
        )

@user_bp.route('/user/<user_id>')
def profile(user_id):
    user = User.query.get(user_id)

    if not user:
        flash("查无此人")
        return redirect('/')

    current_user_id = current_user.id if hasattr(current_user, 'id') else None
    return render_template(
        'profile.html',
        title='My profile',
        user=user,
        current_user_id=current_user_id
    )

@user_bp.route("/me")
@login_required
def me():
    return redirect(f'/user/{current_user.id}')

@user_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    '''
    User will update their infos here.
    User may not update all items.
    Only none `None` item will be updated.
    '''
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        gender = request.form.get('gender')
        school = request.form.get('school')
        user = User.query.get(current_user.id)
        if nickname:
            user.nickname = nickname
        if school:
            user.school = school
        if gender:
            # the dafault value of gender is false, only update true
            user.gender=True
        db.session.commit()
        return redirect('/profile')
    else:
        return render_template(
            'edit_profile.html',
            title='Edit Your Profile',
            current_user=current_user
        )

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@user_bp.route('/user/manage')
def user_manage():
    if request.method == 'POST':
        pass
    else:
        users = User.query.all()
        
        return render_template(
            'user_manage.html',
            title =  '用户管理',
            users = users
        )

@user_bp.route('/user/manage/freeze/<user_id>')
def user_freeze(user_id):
    user = User.query.get(user_id)
    user.status = 'FREEZE'
    db.session.commit()
    return jsonify(
        msg = 'success'
    )


@user_bp.route('/user/manage/normal/<user_id>')
def user_normal(user_id):
    user = User.query.get(user_id)
    user.status = 'NORMAL'
    db.session.commit()
    return jsonify(
        msg = 'success'
    )