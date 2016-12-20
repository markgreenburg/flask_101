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

@APP.route("/new_page")
def new_page():
    return render_template("new_page.html", page=models.Page())

@APP.route("/new_page_save", methods=["POST"])
def insert_page():
    """
    Saves the new form content
    """
    page = models.Page()
    page.title = request.form.get("title")
    page.content = request.form.get("content")
    page.modified_by = request.form.get("modified_by")
    page.save()
    flash("Page '%s' created successfully" % page.title)
    return redirect ("/")

@APP.route("/view/<page_id>")
def show_page(page_id):
    """
    Shows the contents of a specific page
    """
    page = models.Page(page_id)
    return render_template("view.html", page_id = page.page_id, \
                           title=page.title, content=page.content,\
                           last_modified=page.last_modified,\
                           modified_by=page.modified_by)

@APP.route("/edit/<page_id>", methods=["GET"])
def edit_page(page_id):
    """
    Shows form to edit the content of the current page. Current values are
    displayed in the form by default.
    """
    page = models.Page(page_id)
    return render_template("edit.html", page_id = page.page_id, \
                           title=page.title, content=page.content,\
                           modified_by=page.modified_by)

@APP.route("/edit_page_save/<page_id>", methods=["POST"])
def update_page(page_id):
    """
    Updates data for a given page id.
    """
    page = models.Page(page_id)
    page.title = request.form.get("title")
    page.content = request.form.get("content")
    page.modified_by = request.form.get("modified_by")
    page.save()
    flash("Page '%s' updated successfully" % page.title)
    return redirect("/")

@APP.route("/delete/<page_id>")
def delete_page(page_id):
    """
    Soft deletes a specific page. Flashes link to user to undo action
    """
    page = models.Page(page_id)
    page.set_delete()
    flash("Page '%s' deleted successfully. <a href='/undelete/%d'>Undo</a>" % (page.title, page.page_id))
    return redirect("/")

@APP.route("/undelete/<page_id>")
def undelete_page(page_id):
    """
    Sets 'deleted' attribute back to 0, effectively restoring the page.
    """
    page = models.Page(page_id)
    page.set_delete(0)
    flash("Page %s restored successfully." % page.title)
    return redirect("/")

if __name__ == "__main__":
    APP.run()
