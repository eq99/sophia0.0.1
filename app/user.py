from datetime import datetime
import logging

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
    login_user
)

from plugins import (
    db,
    cache,
    login_manager
)
from app.models import User

user_bp = Blueprint('user_bp', __name__)

login_manager.login_view='/signin'

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(int(user_id))
    else:
        return None

@user_bp.route('/smscode', methods=['GET', 'POST'])
def smscode():
    if request.method == 'POST':
        phone = request.form['phone']
        if phone is not None:
            print(f'phone:{phone}')
            cache.set(phone, '1234')
            return jsonify(
                message=f'get phone number {phone}.',
                code=200
            )

@user_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        phone = request.form.get('phone')
        smscode = request.form.get('smscode')
        if smscode == cache.get(phone):
            user = User.query.filter(User.phone == phone).first()
            if user is None:
                user = User(
                    phone = phone,
                    nickname=f'用戶{phone}',
                    created_time=datetime.now()
                )
                db.session.add(user)
                db.session.commit()
            print(user, user.id)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('signin.html')

    return render_template('signin.html')

