"""
Phonebook app with basic CRUD, using Flask and Jinja2 templating.
"""

from flask import Flask, render_template, request, redirect
import mysql.connector
import config

phonebook = Flask("Phonebook")
phonebook.debug = True

conx = mysql.connector.connect(
    user=config.db_args['user'],
    password=config.db_args['password'],
    host=config.db_args['host'],
    database=config.db_args['database']
)

cur = conx.cursor()

@phonebook.route("/")
def home():
    """
    Phonebook homepage. Displays list of entries phonebook.
    """
    phonebook_entries = ("SELECT id, profile_img, first_name, last_name, github_link FROM user_names ORDER BY last_name ASC")
    cur.execute(phonebook_entries)
    return render_template("index.html", entries=cur.fetchall(), title="All Entries")

@phonebook.route("/add_person", methods=["GET"])
def add_person():
    """
    Form to allow adding a new person to the phonebook
    """
    return render_template("add_person.html")

@phonebook.route("/create_person", methods=["POST"])
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
    cur.execute(create_user)
    conx.commit()
    created_user_id = cur.lastrowid
    # Put this in a loop
    add_home_number = ("insert into user_numbers (user_id, user_number, type) values (\"%d\", \"%s\", \"%s\");" % (created_user_id, phone_1, phone_1_type))
    cur.execute(add_home_number)
    add_work_number = ("insert into user_numbers (user_id, user_number, type) values (\"%d\", \"%s\", \"%s\");" % (created_user_id, phone_2, phone_2_type))
    cur.execute(add_work_number)
    add_mobile_number = ("insert into user_numbers (user_id, user_number, type) values (\"%d\", \"%s\", \"%s\");" % (created_user_id, phone_3, phone_3_type))
    cur.execute(add_mobile_number)
    # End loop
    conx.commit()
    return redirect("/")

@phonebook.route("/details", methods=["GET"])
#need to pass in the id
def details():
    user_id = int(request.args.get('id'))
    cur.execute(
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
    return render_template("details.html", contact_details=cur.fetchone())

@phonebook.route("/edit_person", methods=["GET"])
def edit_person():
    """
    Form to allow changing of existing entry data
    """
    user_id = int(request.args.get('id'))
    cur.execute(
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
    user_names_info = cur.fetchone()
    cur.execute(
    """
    SELECT
    user_number,
    type
    FROM user_numbers
    WHERE
    id = %d;
    """
    % user_id)
    user_phone_info = cur.fetchall()
    print user_names_info[4]
    # New contact info comes back in
    return render_template("edit_person.html", user_info=user_names_info, user_contact_info= user_phone_info)

@phonebook.route("/update_person", methods=["POST"])
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
    cur.execute(
    """
    UPDATE user_names
    SET first_name='%s', last_name='%s', profile_img='%s', github_link='%s'
    WHERE
        id=%s
    """
    % (new_user_fname, new_user_lname, new_user_profile_img, new_user_github, user_id)
    )
    conx.commit()
    return redirect("/")


    # Update phone details


@phonebook.route("/delete_person")
def delete_person():
    """
    Deletes a person from the phonebook index
    """

@phonebook.route("/destroy_person")
def destroy_person():
    """
    Destroys the deleted entry from the database.
    """

if __name__ == "__main__":
    phonebook.run()

cur.close()
conx.close()
