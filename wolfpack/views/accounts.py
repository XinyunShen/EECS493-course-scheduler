"""
wolfpack accounts view.

URLs include:
/accounts/login/
/accounts/logout/
/accounts/create/
/accounts/delete/
/accounts/edit/
/accounts/password/
"""
import sqlite3
import uuid
import hashlib
import pathlib
import flask
import wolfpack


@wolfpack.app.route('/accounts/login/', methods=['GET', 'POST'])
def login():
    """Handle POST."""
    # If logged in, redirect to /
    if flask.session.get('username'):
        return flask.redirect(flask.url_for('show_index'))

    # If POST check user and password
    if flask.request.method == "POST":

        username = flask.request.form["username"]
        password = flask.request.form["password"]

        # Connect to database
        connection = wolfpack.model.get_db()

        # Query database
        cur_user = connection.execute(
            "SELECT * FROM users WHERE username=?", [username]
        )
        try:
            fetched = cur_user.fetchall()
        except sqlite3.Error:
            print("Failed to query.")
            flask.abort(500)

        # If user exists
        if len(fetched) > 0:

            # Encode enetered password
            algorithm = 'sha512'
            salt = fetched[0]['password'].split('$')[1]
            hash_obj = hashlib.new(algorithm)
            password_salted = salt + password
            hash_obj.update(password_salted.encode('utf-8'))
            password_hash = hash_obj.hexdigest()
            password_db_string = "$".join([algorithm, salt, password_hash])

            if password_db_string == fetched[0]['password']:
                # If password matches redirect
                flask.session['username'] = username
                return flask.redirect(flask.url_for('show_index'))
            # If user does not exist error 403
            print("wrong psw")
            flask.abort(403)
        else:
            flask.abort(403)

    # Add database info to context
    context = {}
    return flask.render_template("accounts-login.html", **context)


@wolfpack.app.route('/accounts/logout/', methods=['GET','POST'])
def logout():
    """Handle POST."""
    # If not logged in 403
    if 'username' not in flask.session:
        flask.abort(403)

    flask.session['username'] = None
    return flask.redirect(flask.url_for('login'))


@wolfpack.app.route('/accounts/create/', methods=['GET', 'POST'])
def create():
    """Handle POST."""
    # If logged in, redirect to edit page
    if flask.session.get('username'):
        return flask.redirect(flask.url_for('edit'))

    # If POST check user and password
    if flask.request.method == "POST":

        inputfile = flask.request.files["file"]
        if inputfile.filename == '':
            flask.abort(400)

        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            suffix=pathlib.Path(inputfile.filename).suffix
        )
        # Save to disk
        path = wolfpack.app.config["UPLOAD_FOLDER"]/uuid_basename
        inputfile.save(path)

        fullname = flask.request.form["fullname"]
        username = flask.request.form["username"]
        email = flask.request.form["email"]
        password = flask.request.form["password"]

        if password == '':
            flask.abort(400)
            return flask.redirect(flask.request.url)
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new('sha512')
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join(['sha512', salt, password_hash])

        # Connect to database
        connection = wolfpack.model.get_db()

        # Query database
        try:
            connection.execute(
                "INSERT INTO users "
                "VALUES (?,?,?,?,?, CURRENT_TIMESTAMP)",
                [username, fullname, email, uuid_basename, password_db_string]
            )
        except sqlite3.Error as err:
            if "UNIQUE constraint failed" in str(err):
                flask.abort(409)
                return flask.redirect(flask.request.url)

        flask.session['username'] = username
        return flask.redirect(flask.url_for('show_index'))

    context = {}
    return flask.render_template("accounts-create.html", **context)


@wolfpack.app.route('/accounts/delete/', methods=['GET', 'POST'])
def delete():
    """Handle POST."""
    # Connect to database
    connection = wolfpack.model.get_db()
    # If POST
    if flask.request.method == "POST":
        # If not logged in 403
        if 'username' not in flask.session:
            flask.abort(403)
        username = flask.session.get('username')

        if flask.request.form["delete"]:
            print("DELETING ACCOUNT")
            # Fetch all post filenames
            try:
                cur_post = connection.execute(
                    "SELECT * FROM posts WHERE owner=?", [username]
                )
                fetched_post = cur_post.fetchall()
            except sqlite3.Error:
                print("error")
                flask.abort(500)
            print(fetched_post)
            # Delete all post images
            for post in fetched_post:
                img_url = pathlib.Path(wolfpack.app.config['UPLOAD_FOLDER'])
                img_url = img_url/post['filename']
                try:
                    img_url.unlink()
                except FileNotFoundError:
                    pass

            # Delete pfp
            try:
                pfp = connection.execute(
                    "SELECT filename AS user_img_url "
                    "FROM users WHERE username=?", [username]
                ).fetchone()
            except sqlite3.Error:
                print("error pfp")
                flask.abort(500)
            pfp_url = pathlib.Path(wolfpack.app.config['UPLOAD_FOLDER'])
            pfp_url = pfp_url/pfp['user_img_url']
            try:
                pfp_url.unlink()
            except FileNotFoundError:
                pass
            print(pfp)

            # Delete DB entry
            connection.execute(
                "DELETE FROM users WHERE username=?", [username]
            )
            flask.session['username'] = None
            return flask.redirect(flask.url_for('create'))

        # return None

    # If not logged in redirect to login
    username = flask.session.get('username')
    if not username:
        return flask.redirect(flask.url_for('login'))

    context = {"logname": username}
    return flask.render_template("accounts-delete.html", **context)


@wolfpack.app.route('/accounts/edit/', methods=['GET', 'POST'])
def edit():
    """Handle POST."""
    # Connect to database
    connection = wolfpack.model.get_db()
    # If POST
    if flask.request.method == "POST":
        # If not logged in 403
        if 'username' not in flask.session:
            flask.abort(403)
        username = flask.session.get('username')

        if flask.request.form["update"]:

            # Update fullname and email
            fullname = flask.request.form["fullname"]
            email = flask.request.form["email"]
            try:
                connection.execute(
                    "UPDATE users "
                    "SET fullname = ?, email = ? "
                    "WHERE username = ?",
                    (fullname, email, username)
                )
            except sqlite3.Error as err:
                print(err)
                flask.abort(500)

            # Upload photo file if included
            inputfile = flask.request.files["file"]
            if inputfile.filename != "":
                uuid_basename = "{stem}{suffix}".format(
                    stem=uuid.uuid4().hex,
                    suffix=pathlib.Path(inputfile.filename).suffix
                )
                path = wolfpack.app.config["UPLOAD_FOLDER"]/uuid_basename
                inputfile.save(path)

                try:
                    # Delete old photo from filesystem
                    oldfile = connection.execute(
                        "SELECT filename AS user_img_url "
                        "FROM users WHERE username = ?", [username]
                    ).fetchone()
                    print(oldfile)
                    old_p = pathlib.Path(wolfpack.app.config['UPLOAD_FOLDER'])
                    old_p = old_p/oldfile['user_img_url']
                    old_p.unlink()

                    # Update photo file
                    connection.execute(
                        "UPDATE users "
                        "SET filename = ? "
                        "WHERE username = ?",
                        (uuid_basename, username)
                    )
                except sqlite3.Error as err:
                    print(err)
                    flask.abort(500)
                except FileNotFoundError as err:
                    print(err)
                    flask.abort(500)

            # Upon successful submission, re-render the current page
            # return flask.redirect(flask.request.url)
        # return None

    # GET
    # If not logged in redirect to login
    username = flask.session.get('username')
    if not username:
        return flask.redirect(flask.url_for('login'))

    # Query user info
    try:
        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            [username]
        ).fetchone()
    except sqlite3.Error as err:
        print(err)
        flask.abort(500)

    context = {"logname": username, "user": user}
    return flask.render_template("accounts-edit.html", **context)


@wolfpack.app.route('/accounts/password/', methods=['GET', 'POST'])
def show_password():
    """Handle POST."""
    # Connect to database
    connection = wolfpack.model.get_db()
    # If POST
    if flask.request.method == "POST":
        # If not logged in 403
        if 'username' not in flask.session:
            flask.abort(403)
        username = flask.session.get('username')

        if flask.request.form["update_password"]:
            old_pass = flask.request.form["password"]
            try:
                user = connection.execute(
                    "SELECT password FROM users WHERE username = ?",
                    [username]
                ).fetchone()
            except sqlite3.Error as err:
                print(err)
                flask.abort(500)
            # Encode old password
            algorithm = 'sha512'
            salt = user['password'].split('$')[1]
            hash_obj = hashlib.new(algorithm)
            password_salted = salt + old_pass
            hash_obj.update(password_salted.encode('utf-8'))
            password_hash = hash_obj.hexdigest()
            password_db_string = "$".join([algorithm, salt, password_hash])

            # Check user's password and abort(403) if fails
            if password_db_string != user["password"]:
                flask.flash("Wrong password")
                flask.abort(403)

            # Check if both new passwords match
            new_pass1 = flask.request.form["new_password1"]
            new_pass2 = flask.request.form["new_password2"]
            if new_pass1 != new_pass2:
                flask.abort(401)

            # Update hashed password entry in database
            if new_pass1 == '':
                flask.abort(400)
                return flask.redirect(flask.request.url)
            algorithm = 'sha512'
            salt = uuid.uuid4().hex
            hash_obj = hashlib.new(algorithm)
            password_salted = salt + new_pass1
            hash_obj.update(password_salted.encode('utf-8'))
            password_hash = hash_obj.hexdigest()
            password_db_string = "$".join([algorithm, salt, password_hash])
            try:
                connection.execute(
                    "UPDATE users "
                    "SET password = ? "
                    "WHERE username = ?", (password_db_string, username)
                )
            except sqlite3.Error as err:
                print(err)
                flask.abort(500)

            # Upon successful submission, redirect to /accounts/edit/
            return flask.redirect(flask.url_for('edit'))

        # return None

    # If not logged in redirect to login
    username = flask.session.get('username')
    if not username:
        return flask.redirect(flask.url_for('login'))

    context = {"logname": username}
    return flask.render_template("accounts-password.html", **context)
