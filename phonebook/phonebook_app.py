"""
Phonebook app with basic CRUD, using Flask and Jinja2 templating.
"""

from flask import Flask, render_template, request, redirect
import mysql.connector
import config

PHONEBOOK = Flask("Phonebook")
PHONEBOOK.debug = True

CONX = mysql.connector.connect(
    user=config.db_args['user'],
    password=config.db_args['password'],
    host=config.db_args['host'],
    database=config.db_args['database']
)

CUR = CONX.cursor()

class person(object):
    """
    Defines attributes of a distinct ID in the phonebook
    """
    

@PHONEBOOK.route("/")
def home():
    """
    Phonebook homepage. Displays list of entries phonebook.
    """
    phonebook_entries = ("SELECT id, profile_img, first_name, last_name, github_link FROM user_names ORDER BY last_name ASC")
    CUR.execute(phonebook_entries)
    return render_template("index.html", entries=CUR.fetchall(), title="All Entries")

@PHONEBOOK.route("/add_person", methods=["GET"])
def add_person():
    """
    Form to allow adding a new person to the phonebook
    """
    return render_template("add_person.html")

@PHONEBOOK.route("/create_person", methods=["POST"])
def create_person():
    """
    Creates the person entered into the add_person form
    """
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github_link = request.form.get('github_link')
    # profile_img = request.form.get('profile_img')
    phone_1 = request.form.get('user_number_1')
    phone_1_type = 'Home'
    phone_2 = request.form.get('user_number_2')
    phone_2_type = 'Work'
    phone_3 = request.form.get('user_number_3')
    phone_3_type = 'Mobile'
    create_user = ("insert into user_names (first_name, last_name, github_link) values ('%s', '%s', '%s')" % (first_name, last_name, github_link))
    CUR.execute(create_user)
    CONX.commit()
    created_user_id = CUR.lastrowid
    # Put this in a loop
    add_home_number = ("insert into user_numbers (user_id, user_number, type) values (\"%d\", \"%s\", \"%s\");" % (created_user_id, phone_1, phone_1_type))
    CUR.execute(add_home_number)
    add_work_number = ("insert into user_numbers (user_id, user_number, type) values (\"%d\", \"%s\", \"%s\");" % (created_user_id, phone_2, phone_2_type))
    CUR.execute(add_work_number)
    add_mobile_number = ("insert into user_numbers (user_id, user_number, type) values (\"%d\", \"%s\", \"%s\");" % (created_user_id, phone_3, phone_3_type))
    CUR.execute(add_mobile_number)
    # End loop
    CONX.commit()
    return redirect("/")

@PHONEBOOK.route("/details", methods=["GET"])
#need to pass in the id
def details():
    user_id = int(request.args.get('id'))
    CUR.execute(
        """
        SELECT
        id,
        first_name fname,
        last_name lname,
        profile_img pimg,
        github_link github
        FROM user_names
        WHERE
        id = %d;
        """
        % user_id
    )
    return render_template("details.html", contact_details=CUR.fetchone())

@PHONEBOOK.route("/edit_person", methods=["GET"])
def edit_person():
    """
    Form to allow changing of existing entry data
    """
    user_id = int(request.args.get('id'))
    CUR.execute(
    """
    SELECT
    first_name,
    last_name,
    profile_img,
    github_link,
    id
    FROM user_names
    WHERE
    id = %d;
    """
        % user_id
    )
    user_names_info = CUR.fetchone()
    CUR.execute(
    """
    SELECT
    user_number,
    type
    FROM user_numbers
    WHERE
    id = %d;
    """
    % user_id)
    user_phone_info = CUR.fetchall()
    print user_names_info[4]
    # New contact info comes back in
    return render_template("edit_person.html", user_info=user_names_info, user_contact_info= user_phone_info)

@PHONEBOOK.route("/update_person", methods=["POST"])
def update_person():
    """
    Replaces existing user data with whatever was entered into the
    edit_person form
    """
    # Get updated values from params
    user_id = request.form.get("user_id")
    print user_id
    new_user_fname = request.form.get("first_name")
    print new_user_fname
    new_user_lname = request.form.get("last_name")
    print new_user_lname
    new_user_github = request.form.get("github_link")
    new_user_profile_img = request.form.get("profile_img")
    new_user_home_num = request.form.get("user_number_home")
    new_user_work_num = request.form.get("user_number_work")
    new_user_home_mobile = request.form.get("user_number_mobile")
    # Update contact details
    CUR.execute(
    """
    UPDATE user_names
    SET first_name='%s', last_name='%s', profile_img='%s', github_link='%s'
    WHERE
        id=%s
    """
    % (new_user_fname, new_user_lname, new_user_profile_img, new_user_github, user_id)
    )
    CONX.commit()
    return redirect("/")

@PHONEBOOK.route("/confirm_delete", methods=["GET"])
def confirm_delete():
    user_id_to_confirm = request.args.get("id")
    return render_template("/confirm_delete.html", id=user_id_to_confirm)

@PHONEBOOK.route("/delete_person", methods=["POST"])
def delete_person():
    """
    Soft deletes a person from the phonebook index
    """
    id_to_delete = request.form.get("id")
    print id_to_delete
    # Delete entries from user_names table
    delete_numbers =\
    """
    DELETE
    FROM user_numbers
    WHERE
    user_id = %s
    """\
    % id_to_delete
    CUR.execute(delete_numbers)
    CONX.commit()

    delete_names =\
    """
    DELETE
    FROM user_names
    WHERE
        id = %s
    """\
    % id_to_delete

    # Delete entries from user_numbers table

    # Execute statements & commit the update
    CUR.execute(delete_names)
    CONX.commit()
    return redirect('/')

if __name__ == "__main__":
    PHONEBOOK.run()

CUR.close()
CONX.close()
