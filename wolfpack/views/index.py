"""
wolfpack index (main) view.

URLs include:
/
"""
import sqlite3
import pathlib
import arrow
import flask
import wolfpack


@wolfpack.app.route('/', methods=['GET', 'POST'])
def show_index():
    # Handle GET
    # If not logged in redirect to login
    username = flask.session.get('username')
    if not username:
        return flask.redirect(flask.url_for('login'))

    # posts = index_posts(username)

    # Add database info to context
    context = {"logname": username}
    return flask.render_template("index.html", **context)
