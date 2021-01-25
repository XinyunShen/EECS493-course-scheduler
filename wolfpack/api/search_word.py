import json
import flask
import wolfpack
# import wolfpack.api.help_func as help_func
from wolfpack.api.exception import InvalidUsage, check_logged_in, check_postid
from wolfpack.api.help_func import split_words
from wolfpack.api.help_func import Intersection


@wolfpack.app.route('/api/v1/hits/', methods=["GET"])
def get_courses():
    """Return course id according to query."""
    query = flask.request.args.get('q', default='', type=str)
    words = split_words(query)
    course_list = []
    course_list = wolfpack.courseid_list
    print(words)
    for word in words:
        if word in wolfpack.course_words:
            print("course include this word:")
            print(wolfpack.course_words[word])
            course_list = Intersection(course_list, wolfpack.course_words[word])
        else:
            course_list = []
            break
    print(course_list)
    context = {
        "word": query,
        "course_list": course_list
    }
    return flask.jsonify(**context)

@wolfpack.app.route('/api/v1/courses/<int:courseid>/', methods=["GET"])
def get_course_info(courseid):
    """"Return course info accourding to courseid"""
    username = check_logged_in()

    # Connect to database
    connection = wolfpack.model.get_db()
    
    # Get course information
    course = connection.execute(
        "SELECT * FROM course WHERE courseid = ?", [courseid]
    ).fetchone()

    context = {
        "course_id": courseid,
        "credits": course["credits"],
        "course_name": course["coursename"],
        "description": course["description"],
        "prerequisite": course["prerequisite"]
    }

    return flask.jsonify(**context)