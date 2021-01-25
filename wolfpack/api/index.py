"""REST API for idk."""
import flask
import wolfpack
from wolfpack.api.exception import InvalidUsage, check_logged_in, check_postid


@wolfpack.app.route('/api/v1/', methods=["GET"])
def get_resource():
    """Return API resource URLs.

    Does not require a login

    Example:
    {
      "posts": "/api/v1/p/",
      "hits": "/api/v1/hits/",
      "url": "/api/v1/"
    }
    """
    username = check_logged_in()

    context = {
        "username": username,
        "posts": "/api/v1/p/",
        "hits": "/api/v1/hits/",
        "url": flask.request.path
    }
    return flask.jsonify(**context)
