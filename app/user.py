from flask import (
    render_template
)

def signin():
    return render_template('signin.html')