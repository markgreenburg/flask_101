"""
Module consists of basic CRUD routes for the wiki APP.
"""

from flask import Flask, render_template, request, redirect
import models

# Initialize new Flask App
APP = Flask("awesome_wiki")
# Load root-level config.py file -> not in version control. Contains DB
# and debug settings
APP.config.from_object('config')

@APP.route("/")
def homepage():
    """
    Directory of all pages in the wiki
    """
    page_list = models.Page.get_pages()
    return render_template("homepage.html", page_list=page_list, title="Mark's\
                           Wiki")


@APP.route("/<page_id>")
def show_page(page_id):
    """
    Shows the contents of a specific page, or shows an error page.
    """
    page = models.Page(page_id)
    if page.page_id:
        return render_template("page_details.html", title=page.title, content=\
        page.content, last_modified=page.last_modified, modified_by=page.\
        modified_by)
    else:
        return render_template("not_a_page.html")

@APP.route("/<page_name>/edit")
def edit_page():
    """
    Shows form to edit the content of the current page
    """


@APP.route("/<page_name>/save")
def save_page():
    """
    Saves the new form content
    """


@APP.route("/<page_name>/delete")
def delete_page():
    """
    Soft deletes a specific page
    """
