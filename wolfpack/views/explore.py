"""
wolfpack explore view.

URLs include:
/
"""
import sqlite3
import flask
import wolfpack


@wolfpack.app.route('/explore/', methods=['GET', 'POST'])
def show_explore():
    """Handle Post."""
    username = flask.session.get("username")
    # Connect to database
    connection = wolfpack.model.get_db()

    if flask.request.method == 'POST':

        # If not logged in, abort
        if 'username' not in flask.session:
            flask.abort(403)
        username = flask.session.get('username')

        if "follow" in flask.request.form:
            # Query database
            print(flask.request.form["username"])
            connection.execute(
                "INSERT INTO following (username1, username2) "
                "VALUES (?,?)", (username, flask.request.form["username"])
            )
            # return flask.redirect(flask.url_for('show_explore'))

    # GET
    # Query for all users logged in user is not following
    try:
        fetch_allusr = connection.execute(
            "SELECT username FROM users "
            "WHERE NOT username=?", [username]
        ).fetchall()
        # print(fetch_allusr)
        allusr = [usr["username"] for usr in fetch_allusr]
        print(allusr)
        fetched_users = connection.execute(
            "SELECT username2 "
            "FROM following "
            "WHERE username1=?", [username]
        ).fetchall()
        print(fetched_users)
        not_followers = []
        for usr in allusr:
            if usr not in [flwr["username2"] for flwr in fetched_users]:
                not_followers.append(usr)
        print(not_followers)
    except sqlite3.Error as err:
        print(err)
        flask.abort(500)

    users = []
    for user in not_followers:
        temp_user = {}
        try:
            pfp = connection.execute(
                "SELECT filename AS user_img_url "
                "FROM users WHERE username = ?", [user]
            ).fetchone()
            print(pfp)
            temp_user["username"] = user
            temp_user["user_img_url"] = pfp["user_img_url"]
        except sqlite3.Error as err:
            print(err)
            flask.abort(500)
        users.append(temp_user)

    # Add database info to context
    context = {"logname": username, "not_following": users}
    return flask.render_template("explore.html", **context)