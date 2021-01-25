"""
API Exceptions.

https://flask.palletsprojects.com/en/0.12.x/patterns/apierrors/
"""
import flask
import wolfpack


class InvalidUsage(Exception):
    """Example:raise InvalidUsage('e', status_code=410)."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Init."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """To dict."""
        rv_dict = dict(self.payload or ())
        rv_dict['message'] = self.message
        rv_dict['status_code'] = self.status_code
        return rv_dict


@wolfpack.app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Handle."""
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def check_logged_in():
    """Check."""
    # Check that user is logged in
    if 'username' not in flask.session:
        raise InvalidUsage("Forbidden", status_code=403)
    username = flask.session.get('username')
    return username


def check_postid(postid):
    """Check."""
    # Connect to database
    connect = wolfpack.model.get_db()

    # Check if post id is out of range
    cur = connect.execute(
        "SELECT COUNT(*) AS postid FROM posts "
        "WHERE postid = ?", [postid]
     ).fetchone()
    if not cur["postid"]:
        raise InvalidUsage("Not Found", status_code=404)
    return connect
