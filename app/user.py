import logging
import json
from datetime import datetime
from urllib.request import urlopen

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
    login_manager
)
from app.models import User

user_bp = Blueprint('user_bp', __name__, template_folder='./templates/user')

# config about login user
# https://flask-login.readthedocs.io/en/latest/
# here is an example:
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
# Note: remenber config `SESSION_COOKIE_NAME` well.
login_manager.login_view='/signin'

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    else:
        return None

@user_bp.route('/smscode', methods=['GET', 'POST'])
def smscode():
    '''
    Send SMS code using to `phone`.
    '''
    if request.method == 'POST':
        phone = request.form['phone']
        if phone is not None:
            print(f'phone:{phone}')
            cache.set(phone, '1234')
            return jsonify(
                message=f'get phone number {phone}.',
                code=200
            )

def generate_avatar():
    '''
    see http://api.btstu.cn/doc/sjtx.php for more details.
    '''
    res = urlopen('http://api.btstu.cn/sjtx/api.php?lx=c1&format=json')
    return json.loads(res.read())['imgurl']

@user_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    '''
    Register: when the user is not registerted.
    Sigin in: when the user is already registed.
    '''
    if request.method == 'POST':
        phone = request.form.get('phone')
        smscode = request.form.get('smscode')
        if smscode == cache.get(phone):
            user = User.query.filter(User.phone == phone).first()
            if user is None:
                user = User(
                    phone = phone,
                    nickname=f'用戶{phone}',
                    avatar_url=generate_avatar(),
                    reputation=0.0,
                    created_time=datetime.now()
                )
                db.session.add(user)
                db.session.commit()
            print(user, user.id)
            login_user(user)
            return redirect('/profile')
        else:
            return render_template(
                'signin.html',
                title='Sign In'
                )

    return render_template(
        'signin.html',
        title='Sign In'
        )

@user_bp.route('/profile')
@login_required
def profile():
    return render_template(
        'profile.html',
        title='My profile',
        current_user=current_user,
    )

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