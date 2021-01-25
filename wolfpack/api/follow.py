"""REST API for follow."""
import flask
import wolfpack
from wolfpack.api.exception import InvalidUsage, check_logged_in, check_postid

@wolfpack.app.route('/api/v1/p/get_following/', methods=["GET"])
def get_following():
    username = check_logged_in()

    # Connect to database
    connection = wolfpack.model.get_db()

    # Query database
    following_users = connection.execute(
        "SELECT username2 FROM following "
        "WHERE username1=? "
        "ORDER By created DESC", [username]
    ).fetchall()

    context = {
        "username" : username,
        "following" : following_users
    }

    return flask.jsonify(**context), 201

@wolfpack.app.route('/api/v1/p/set_following/', methods=["POST"])
def set_following():
    username = check_logged_in()

    # Connect to database
    connection = wolfpack.model.get_db()

    if "username" not in flask.request.json:
        raise InvalidUsage("Bad Request", 400)
    follow_user = flask.request.json["username"]

    # Create comment
    existing = connection.execute(
        "SELECT * FROM following "
        "WHERE username1=? "
        "AND username2=?",
        (username, follow_user)
    ).fetchall()

    if len(existing) > 0:
        flask.abort(404)
    
    connection.execute(
        "INSERT INTO following(username1, username2) "
        "VALUES(?,?)",
        (username, follow_user)
    )

    return flask.jsonify({"followed_user" : follow_user}), 201