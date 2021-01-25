"""
wolfpack user view.

URLs include:
/
"""
import sqlite3
import pathlib
import uuid
import flask
import wolfpack
import requests
from wolfpack.api.user_schedule import *
import json


@wolfpack.app.route('/u/<user_url_slug>/', methods=['GET', 'POST'])
def show_user_slug(user_url_slug):
    """Descriptive Docstring."""
    # Connect to database
    connection = wolfpack.model.get_db()

    if flask.request.method == 'POST':
        # If not logged in, abort
        if 'username' not in flask.session:
            flask.abort(403)
        username = flask.session.get('username')
        if "follow" in flask.request.form:
            # Query database
            connection.execute(
                "INSERT INTO following (username1, username2) "
                "VALUES (?,?)", (username, flask.request.form["username"])
            )
            # return flask.redirect(flask.request.url)11

        elif "unfollow" in flask.request.form:
            connection.execute(
                "DELETE FROM following "
                "WHERE username1=? AND username2=?",
                [username, flask.request.form["username"]]
            )
            return flask.redirect(flask.url_for('show_index'))

        elif "logout" in flask.request.form:
            return flask.redirect(flask.url_for('logout'))

    # GET
    # If not logged in redirect to login
    username = flask.session.get('username')
    if not username:
        return flask.redirect(flask.url_for('login'))

    # abort 404 if user_url_slug not in database
    cur = connection.execute(
        "SELECT COUNT(*) AS user_url_slug FROM users "
        "WHERE username = ?", [user_url_slug]
     ).fetchone()
    if not cur["user_url_slug"]:
        flask.abort(404)

    # Retrieve fullname
    cur = connection.execute(
        "SELECT fullname "
        "FROM users WHERE username=?", [user_url_slug]
    )
    user = cur.fetchone()

    # Retrieve if login user follows user_url_slug user
    cur = connection.execute(
        "SELECT username2 "
        "FROM following WHERE username1=?", [username]
    ).fetchall()
    user["logname_follows_username"] = user_url_slug in [usr["username2"]
                                                         for usr in cur]

    # Retrieve number following
    cur = connection.execute(
        "SELECT COUNT(username2) AS following "
        "FROM following WHERE username1=?", [user_url_slug]
    )
    user.update(cur.fetchone())

    # Retrieve followers
    cur = connection.execute(
        "SELECT COUNT(username1) AS followers "
        "FROM following WHERE username2=?", [user_url_slug]
    )
    user.update(cur.fetchone())
    
    # Get schedule data
    schedule = {
        'Monday':[],
        'Tuesday':[],
        'Wednesday':[],
        'Thursday':[],
        'Friday':[],
        'Saturday':[],
        'Sunday':[]
    }
    response = get_user_schedule(user_url_slug)
    if response.status_code == 200:
        for key, value in json.loads(response.data).items():
            course_info = get_coursetime(
                value.get('courseid'),
                value.get('timeid')
            )
            course_info = json.loads(course_info.data)
            print(course_info)
            course = {
                'coursename': str(course_info.get('courseid')) + " " + course_info.get('coursename'),
                'starttime': course_info.get('starttime'),
                'endtime': course_info.get('endtime'),
                'courseid': course_info.get('courseid'),
                'timeid': course_info.get('timeid'),
                'description': course_info.get('description')
            }        
            for day in course_info.get('weekday').split():
                schedule[day].append(course)
        for day, classes in schedule.items():
            schedule[day] = sorted(classes, key=lambda k: k['starttime']) 
        print(schedule)

    # Add database info to context
    print(username)
    context = {
        "logname": username, 
        "username": user_url_slug,
        "user": user,
        "schedule": schedule
    }
    return flask.render_template("user.html", **context)


def check_valid_user(user_url_slug):
    """Abort 404 if user not in database."""
    # abort 404 if user_url_slug not in database
    connection = wolfpack.model.get_db()
    cur = connection.execute(
        "SELECT COUNT(*) AS user_url_slug FROM users "
        "WHERE username = ?", [user_url_slug]
     ).fetchone()
    if not cur["user_url_slug"]:
        return False
    return True


@wolfpack.app.route('/u/<user_url_slug>/followers/', methods=['GET', 'POST'])
def show_user_followers(user_url_slug):
    """Handle POST."""
    # Connect to database
    connection = wolfpack.model.get_db()

    if flask.request.method == 'POST':
        # If not logged in, abort
        if 'username' not in flask.session:
            flask.abort(403)
        username = flask.session.get('username')

        print(flask.request.form)
        if "follow" in flask.request.form:
            # Query database
            connection.execute(
                "INSERT INTO following (username1, username2) "
                "VALUES (?,?)", (username, flask.request.form["username"])
            )
            # return flask.redirect(flask.request.url)
        elif "unfollow" in flask.request.form:
            connection.execute(
                "DELETE FROM following "
                "WHERE username1=? AND username2=?",
                [username, flask.request.form["username"]]
            )
            # return flask.redirect(flask.request.url)

    # Handle GET
    # If not logged in redirect to login
    username = flask.session.get('username')
    if not username:
        return flask.redirect(flask.url_for('login'))

    # Abort if user not valid
    if not check_valid_user(user_url_slug):
        flask.abort(404)

    # Query for all users following user_url_slug
    try:
        fetched_users = connection.execute(
            "SELECT username1 "
            "FROM following "
            "WHERE username2=?", [user_url_slug]
        ).fetchall()
        print(fetched_users)
        follower_name = [usr["username1"] for usr in fetched_users]
    except sqlite3.Error as err:
        print(err)
        flask.abort(500)

    # Query for the follower's img and if login user follows them
    followers = []
    for user in follower_name:
        temp_user = {}
        try:
            # query pfp
            pfp = connection.execute(
                "SELECT filename AS user_img_url "
                "FROM users WHERE username=?", [user]
            ).fetchone()
            print(pfp)

            # query if login user follows them back
            try:
                fetch_following = connection.execute(
                    "SELECT username2 "
                    "FROM following WHERE username1=?", [username]
                ).fetchall()
                logname_follows_username = user in [usr["username2"]
                                                    for usr in fetch_following]
            except sqlite3.Error as err:
                print(err)
                flask.abort(500)

            temp_user["username"] = user
            up_path = pathlib.Path('/uploads/')
            temp_user["user_img_url"] = up_path/pfp["user_img_url"]
            temp_user["logname_follows_username"] = logname_follows_username
        except sqlite3.Error as err:
            print(err)
            flask.abort(500)
        followers.append(temp_user)

    # Add database info to context
    context = {"logname": username, "user_url_slug": user_url_slug,
               "followers": followers}
    return flask.render_template("followers.html", **context)


@wolfpack.app.route('/u/<user_url_slug>/following/', methods=['GET', 'POST'])
def show_user_following(user_url_slug):
    """Handle POST."""
    # Connect to database
    connection = wolfpack.model.get_db()

    if flask.request.method == 'POST':
        # If not logged in, abort
        if 'username' not in flask.session:
            flask.abort(403)
        username = flask.session.get('username')

        print(flask.request.form)

        if "follow" in flask.request.form:
            # Query database
            connection.execute(
                "INSERT INTO following (username1, username2) "
                "VALUES (?,?)", (username, flask.request.form["username"])
            )
            # return flask.redirect(flask.request.url)

        if "unfollow" in flask.request.form:
            connection.execute(
                "DELETE FROM following "
                "WHERE username1=? AND username2=?",
                [username, flask.request.form["username"]]
            )
            # return flask.redirect(flask.request.url)

    # If not logged in redirect to login
    username = flask.session.get('username')
    if not username:
        return flask.redirect(flask.url_for('login'))

    # Abort if user not valid
    if not check_valid_user(user_url_slug):
        flask.abort(404)

    # Query for all users that user_url_slug follows
    try:
        fetched_users = connection.execute(
            "SELECT username2 "
            "FROM following "
            "WHERE username1=?", [user_url_slug]
        ).fetchall()
        print(fetched_users)
        following_name = [usr["username2"] for usr in fetched_users]
    except sqlite3.Error as err:
        print(err)
        flask.abort(500)

    # Query for the follower's img and if login user follows them
    followings = []
    for user in following_name:
        temp_user = {}
        try:
            # query pfp
            pfp = connection.execute(
                "SELECT filename AS user_img_url "
                "FROM users WHERE username=?", [user]
            ).fetchone()
            print(pfp)

            # query if login user follows them back
            try:
                fetch_following = connection.execute(
                    "SELECT username2 "
                    "FROM following WHERE username1=?", [username]
                ).fetchall()
                logname_follows_username = user in [usr["username2"]
                                                    for usr in fetch_following]
            except sqlite3.Error as err:
                print(err)
                flask.abort(500)

            temp_user["username"] = user
            up_path = pathlib.Path('/uploads/')
            temp_user["user_img_url"] = up_path/pfp["user_img_url"]
            temp_user["logname_follows_username"] = logname_follows_username
        except sqlite3.Error as err:
            print(err)
            flask.abort(500)
        followings.append(temp_user)

    # Add database info to context
    context = {"logname": username, "user_url_slug": user_url_slug,
               "following": followings}
    return flask.render_template("following.html", **context)
