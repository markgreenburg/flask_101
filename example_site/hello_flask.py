"""
Module finds all entries in Pages table and passes them along to the html
template of root localhost directory.
"""

from flask import Flask, render_template, request #, redirect
import mysql.connector

APP = Flask("MyApp")

# This should go in a separate config.py file, and be gitignored. Then, create
# a config.default file as an example. Should not be uploading sensitive info...
CONN = mysql.connector.connect(
    user="root",
    password="myfirstsql",
    host="127.0.0.1",
    database="simple_cms_development"
    )

CUR = CONN.cursor()

@APP.route("/")
def home():
    """
    Returns the name and ID of each entry in pages table to the corresponding
    HTML template, students.html.
    """
    query = ("SELECT id, name FROM pages")
    CUR.execute(query)
    q = request.args.get('q')
    return render_template("students.html", student_list=CUR.fetchall(), \
    title="Student List", q=q)

@APP.route("/new_student")
def new_student():
    """
    Displays form to add a new user
    """
    return render_template("new_student.html")

@APP.route("/submit_new_student", methods=["POST"])
def submit_new_student():
    """
    Posts new student and
    """
    name = request.form.get('name')
    website = request.form.get('website')
    github_username = request.form.get('github_username')
    query = ("inseert into student (name) values (\"%s\")" % name)
    CUR.execute(query)
    CONN.commit()
    return render_template("submit_new_student.html", name=name,\
    website=website, github_username=github_username)
    # return redirect('/')

if __name__ == "__main__":
    APP.run(debug=True)

CUR.close()
CONN.close()
