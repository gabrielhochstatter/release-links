from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db


bp = Blueprint('user', __name__)

def get_user(username):
    user = get_db().execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        abort(404, "This user does not exist")

    return user

@bp.route('/u/<username>')
def profile(username):
    user = get_user(username)

    releases = get_db().execute(
        'SELECT * FROM release WHERE owner_id = ?'
        ' ORDER BY created DESC', (user['id'],)
    ).fetchall()

    return render_template('user/profile.html', user=user, releases=releases)

