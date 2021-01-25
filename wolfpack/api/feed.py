"""REST API for idk."""
import flask
import wolfpack


@wolfpack.app.route('/api/v1/feed', methods=["GET"])
def get_feed():
    return flask.render_template("feed.html")