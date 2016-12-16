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

@phonebook.route("/add_person")
def add_person():
    """
    Form to allow adding a new person to the phonebook
    """

@phonebook.route("/create_person")
def create_person():
    """
    Creates the person entered into the add_person form
    """
# do we really need a route for this? Probably not.

@phonebook.route("/edit_person")
def edit_person():
    """
    Form to allow changing of existing entry data
    """

@phonebook.route("/update_person")
def update_person():
    """
    Replaces existing user data with whatever was entered into the
    edit_person form
    """

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
