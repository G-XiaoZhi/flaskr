# coding:utf-8
from flask import Blueprint, render_template, session, flash, url_for
from flask import request
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from flaskr.app.bootstrap import get_db, cnf

bp = Blueprint(__name__, __name__)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['username'] != cnf['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != cnf['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('flaskr.app.views.entry_list'))
    # elif request.method == 'GET':

    return render_template('login.html', error=error)


@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('flaskr.app.views.entry_list'))


@bp.route("/entry/list")
def entry_list():
    db = get_db()
    cur = db.execute('select id, title, content from entries order by id desc')
    entries = cur.fetchall()
    return render_template('entry_list.html', entries=entries)


@bp.route('/entry/add', methods=['POST', "GET"])
def entry_add():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'GET':
        return render_template("entry_add.html")
    db = get_db()
    db.execute('insert into entries (title, content) values (?, ?)',
               [request.form['title'], request.form['content']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('flaskr.app.views.entry_list'))


@bp.route('/entry/detail', methods=['GET'])
def entry_detail():
    db = get_db()
    entry_id = request.args.get('id')
    if not entry_id:
        abort(404)

    cur = db.execute('select title, content from entries where id=?', [entry_id])
    entry = cur.fetchone()
    return render_template('entry_detail.html', entry=entry)
