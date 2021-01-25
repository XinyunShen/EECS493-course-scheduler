"""REST API for idk."""
import json
import flask
import wolfpack
from wolfpack.api.exception import InvalidUsage,check_logged_in
import sqlite3

@wolfpack.app.route('/api/v1/schedule/<string:username>/', methods=["GET"])
def get_user_schedule(username):
    """get user schedule based on username."""
    # check whether logged_in user is friends with this user
    # still need to be implemented
    #  TO DO
    logged_user = check_logged_in()
    connection = wolfpack.model.get_db()

    existing = connection.execute(
        "SELECT * FROM following "
        "WHERE username1=? "
        "AND username2=? ",
        (logged_user, username)
    ).fetchall()

    # not friends
    # can read their own schedule
    if len(existing) == 0 and logged_user!=username:
        flask.abort(404)

    schedules = connection.execute(
        "SELECT * FROM schedule WHERE username = ?", [username]
    ).fetchall()
    context = {}
    for schedule in schedules:
        temp = {
            'username': schedule['username'],
            'courseid': schedule['courseid'],
            'timeid': schedule['timeid']
        }
        context[str(schedule['timeid'])] = temp
    return flask.jsonify(**context)

def username_schedule_this(connection, username, courseid, timeid):
    """Query for if Owner liked the post."""
    cur = connection.execute(
        "SELECT COUNT(*)"
        " FROM schedule"
        " WHERE username = ? AND courseid = ? AND timeid = ?;", (username, courseid, timeid)
    )
    return cur.fetchone()['COUNT(*)']

@wolfpack.app.route('/api/v1/schedule/user/<int:courseid>/<int:timeid>/', methods=["POST"])
def create_schedule(courseid, timeid):
    """create a schedule for user."""
    username = check_logged_in()
    if username is None:
        raise InvalidUsage('Forbidden', 403)
    # username = 'xinyun'
    # print(courseid," and ", timeid)
    connection = wolfpack.model.get_db()
    # print(username_schedule_this(connection, username, courseid, timeid))
    if username_schedule_this(connection, username, courseid, timeid) == 0:
        connection.execute(
            "INSERT INTO schedule(username, timeid, courseid) "
            "VALUES (?,?,?);", (username, timeid, courseid)
        )
        context = {
            "username": username,
            "courseid": courseid,
            "timeid": timeid,
        }
        return flask.jsonify(**context), 201
    context = {
        "username": username,
        "courseid": courseid,
        "timeid": timeid,
        "message": "Conflict",
        "status_code": 409,
    }
    return flask.jsonify(**context), 409


@wolfpack.app.route('/api/v1/schedule/user/<int:courseid>/<int:timeid>/', methods=["DELETE"])
def delete_schedule(courseid, timeid):
    """delete a schedule for user."""
    username = check_logged_in()
    if username is None:
        raise InvalidUsage('Forbidden', 403)

    connection = wolfpack.model.get_db()
    # try to delete
    if username_schedule_this(connection, username, courseid, timeid) == 1:
        connection.execute(
            "DELETE FROM schedule WHERE username=? "
            "AND timeid=? AND courseid=?", (username, timeid, courseid)
        )

    return '',204

@wolfpack.app.route('/api/v1/schedule/<int:courseid>/', methods=["GET"])
def get_coursetimes(courseid):
    """Get course time coresponding to its id."""
    username = check_logged_in()
    connection = wolfpack.model.get_db()

    courses = connection.execute(
        "SELECT * FROM coursetime WHERE courseid = ?", [courseid]
    ).fetchall()
    context = {}
    for course in courses:
        course_dict = {
            'courseid' : course['courseid'],
            'timeid': course['timeid'],
            'starttime':  course['starttime'],
            'endtime':  course['endtime'],
            'weekday':  course['weekday'],
        }
        context[str(course['timeid'])]=course_dict
    return flask.jsonify(**context)
        

@wolfpack.app.route('/api/v1/schedule/<int:courseid>/<int:timeid>/', methods=["GET"])
def get_coursetime(courseid, timeid):
    """Get course time coresponding to its id."""
    username = check_logged_in()
    connection = wolfpack.model.get_db()

    course = connection.execute(
        "SELECT coursetime.*, course.coursename, course.description "
        "FROM coursetime "
        "LEFT JOIN course "
        "ON coursetime.courseid = course.courseid "
        "WHERE coursetime.courseid = ? and coursetime.timeid = ?", 
        [courseid, timeid]
    ).fetchone()
    context = {
        'courseid' : course['courseid'],
        'timeid': course['timeid'],
        'starttime':  course['starttime'],
        'endtime':  course['endtime'],
        'weekday':  course['weekday'],
        'coursename': course['coursename'],
        'description': course['description']
    }
    return flask.jsonify(**context)


@wolfpack.app.route('/api/v1/schedule/<string:username>/complete', methods=["GET"])
def get_schedule(username):
    schedule = {
        'Monday':[],
        'Tuesday':[],
        'Wednesday':[],
        'Thursday':[],
        'Friday':[],
        'Saturday':[],
        'Sunday':[]
    }
    response = get_user_schedule(username)
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
    return flask.jsonify(**schedule)