from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('release', __name__)

def get_release(id, check_owner=True):
    release = get_db().execute(
        'SELECT * FROM release WHERE id = ?', (id,)
    ).fetchone()

    if release is None:
        abort(404, "This release does not exist!")


    return release

@bp.route('/')
def index():
    return render_template('release/index.html')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        label = request.form['label']
        link_1 = request.form['link_1']
        link_2 = request.form['link_2']
        link_3 = request.form['link_3']
        error = None

        if not title:
            error = 'A title is required!'

        if not artist:
            error = 'An artist name is required!'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO release (title, artist, label, link_1, link_2, link_3, owner_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (title, artist, label, link_1, link_2, link_3, g.user['id'],)
            )
            db.commit()
            return redirect(url_for('release.index'))
    
    else:
        return render_template('release/create.html')

@bp.route('/r/<int:id>')
def display(id):
    release = get_release(id)

    return render_template('release/display.html', release=release)


@bp.route('/r/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    release = get_release(id)

    if release['owner_id'] != g.user['id']:
        abort(403)

    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        label = request.form['label']
        link_1 = request.form['link_1']
        link_2 = request.form['link_2']
        link_3 = request.form['link_3']
        error = None

        if not title:
            error = 'A title is required!'

        if not artist:
            error = 'An artist name is required!'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE release SET' 
                ' title = ?,'
                ' artist = ?,'
                ' label = ?,'
                ' link_1 = ?,'
                ' link_2 = ?,'
                ' link_3 = ?'
                ' WHERE id = ?',
                (title, artist, label, link_1, link_2, link_3, release['id'],)
            )
            db.commit()
            return redirect(url_for('release.display', id=release['id'])) 
    else:
        return render_template('release/update.html', release=release)