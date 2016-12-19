"""
Module consists of basic CRUD routes for the wiki APP.
"""

from flask import Flask, render_template, request, redirect, flash
import models

# Initialize new Flask App
APP = Flask("awesome_wiki")
# Load root-level config.py file -> not in version control. Contains DB
# and debug settings
APP.config.from_object('config')
APP.secret_key = '123456'

@APP.route("/")
def homepage():
    """
    Directory of all pages in the wiki
    """
    page_list = models.Page.get_pages()
    return render_template("homepage.html", page_list=page_list, title="Mark's\
                           Wiki")

@APP.route("/view/<page_id>")
def show_page(page_id):
    """
    Shows the contents of a specific page, or shows an error page.
    """
    page = models.Page(page_id)
    if page.page_id:
        return render_template("view.html", page_id = page.page_id, \
        title=page.title, content=page.content, \
        last_modified=page.last_modified, modified_by=page.modified_by)
    else:
        return render_template("not_a_page.html")

@APP.route("/edit/<page_id>")
def edit_page():
    """
    Shows form to edit the content of the current page
    """


@APP.route("/new_page")
def new_page():
    return render_template("new_page.html")

@APP.route("/new_page_save", methods=["GET", "POST"])
def save_page():
    """
    Saves the new form content
    """
    page = models.Page()
    page.title = request.form.get("title")
    page.content = request.form.get("content")
    page.modified_by = request.form.get("modified_by")
    print page.title
    print page.content
    print page.page_id
    page.save()
    flash("Page '%s' created successfully" % page.title)
    return redirect ("/")


@APP.route("/<page_name>/delete")
def delete_page():
    """
    Soft deletes a specific page
    """
    

if __name__ == "__main__":
    APP.run()
