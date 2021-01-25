"""wolfpack package initializer."""
import pathlib
import re
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Read settings from config module (wolfpack/config.py)
app.config.from_object('wolfpack.config')

# Overlay settings read from a Python file whose path is set in the environment
# variable wolfpack_SETTINGS. Setting this environment variable is optional.
# Docs: http://flask.pocoo.org/docs/latest/config/
#
# EXAMPLE:
# $ export wolfpack_SETTINGS=secret_key_config.py
app.config.from_envvar('wolfpack_SETTINGS', silent=True)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import wolfpack.api  # noqa: E402 pylint: disable=wrong-import-position
import wolfpack.views  # noqa: E402  pylint: disable=wrong-import-position
import wolfpack.model  # noqa: E402  pylint: disable=wrong-import-position

# File of wolfpack
WOLFPACK_ROOT = pathlib.Path(__file__).parent
STOPWORDS = WOLFPACK_ROOT/"stopwords.txt"
COURSE_INFO = WOLFPACK_ROOT/"course_information.txt"


# read all the stopwords
stopwords = []
with open(STOPWORDS, "r") as input_file:
    for line in input_file:
        line = line.split("\n")[0]
        stopwords.append(line)


# create a dict in which key is the word and value is a list of course id which its description invloves this word.
course_words = {}
courseid_list = []
with open(COURSE_INFO, "r") as input_file:
    for line in input_file:
        line = line.split("//")
        course_id = line[0]
        courseid_list.append(course_id)
        course_name = line[1]
        course_info = line[2]
        course_name = course_name.split(' ')
        course_info = course_info.split(' ')
        total_words = course_name + course_info
        for word in total_words:
            word = re.sub(r'[^a-zA-Z0-9]+', '', word).lower()
            if word in stopwords or word == '':
                continue
            if word in course_words:
                if course_id not in course_words[word]:
                    course_words[word].append(course_id)
            else:
                course_words[word] = [course_id]