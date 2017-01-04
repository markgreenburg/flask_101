"""
Module consists of basic CRUD routes for the wiki APP.
"""

from flask import Flask, Markup, render_template, request, redirect, flash, \
session
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
import models
from wiki_linkify import wiki_linkify
import markdown

# Initialize new Flask App
APP = Flask("awesome_wiki")
# Load root-level config.py file -> not in version control. Contains DB
# and debug settings
APP.config.from_object('config')
APP.secret_key = '123456'
Breadcrumbs(app=APP)

@APP.route("/")
@register_breadcrumb(APP, '.', 'Home')
def homepage():
    """
    Directory of all pages in the wiki
    """
    page_list = models.Page.get_pages()
    return render_template("homepage.html", page_list=page_list, \
    title="Page Index")

@APP.route("/submit_search", methods=["GET"])
@register_breadcrumb(APP, '.search', 'Search Results')
def submit_search():
    """
    Posts search form contents and redirects to a results page.
    """
    search_query = request.args.get("search_string")
    print search_query
    page_list = models.Page.find_pages(search_query)
    return render_template("homepage.html", page_list=page_list, \
    title="Search Results")

@APP.route("/login")
@register_breadcrumb(APP, '.login', 'Log In')
def login():
    """
    Presents login form to user.
    """
    return render_template("login.html")

@APP.route("/submit_login", methods=["POST"])
def submit_login():
    """
    submits login credentials to authenticate user, or redirects to login page.
    """
    entered_username = request.form.get('username')
    entered_password = request.form.get('password')
    user = models.User.get_user(entered_username)
    if user.password == entered_password:
        session['username'] = user.username
        return redirect("/")
    flash("Incorrect username or password")
    return redirect("/login")

@APP.route("/logout")
def logout():
    """
    Logs out current user by deleting their username from the session
    """
    del session['username']
    return redirect("/")

@APP.route("/new_page")
@register_breadcrumb(APP, '.new_page', 'Add Page')
def new_page():
    """
    Displays form to allow entry of data for new page creation.
    """
    if 'username' in session:
        return render_template("new_page.html", page=models.Page())
    flash("You must be logged in to add a page")
    return redirect("/login")

@APP.route("/new_page_save", methods=["POST"])
def insert_page():
    """
    Saves the new form content
    """
    page = models.Page()
    page.title = request.form.get("title")
    page.content = request.form.get("content")
    page.modified_by = session['username']
    page.save()
    flash("Page '%s' created successfully" % page.title)
    return redirect("/")

@APP.route("/view/<int:page_id>")
@register_breadcrumb(APP, '.view', 'View Page')
def show_page(page_id):
    """
    Shows the contents of a specific page
    """
    page = models.Page(page_id)
    page.content = wiki_linkify(page.content)
    page.content = Markup(markdown.markdown(page.content))
    return render_template("view.html", page_id=page.page_id, \
                           title=page.title, \
                           content=page.content,\
                           last_modified=page.last_modified,\
                           modified_by=page.modified_by)

@APP.route("/edit/<int:page_id>", methods=["GET"])
@register_breadcrumb(APP, '.view.edit', 'Edit Page')
def edit_page(page_id):
    """
    Shows form to edit the content of the current page. Current values are
    displayed in the form by default.
    """
    if 'username' in session:
        page = models.Page(page_id)
        return render_template("edit.html", page_id=page.page_id, \
                               title=page.title, content=page.content,\
                               modified_by=page.modified_by)
    flash("You must be logged in to edit a page")
    return redirect("/login")

@APP.route("/edit_page_save/<int:page_id>", methods=["POST"])
def update_page(page_id):
    """
    Updates data for a given page id.
    """
    page = models.Page(page_id)
    page.title = request.form.get("title")
    page.content = request.form.get("content")
    page.modified_by = session['username']
    page.save()
    flash("Page '%s' updated successfully" % page.title)
    return redirect("/")

@APP.route("/delete/<int:page_id>")
def delete_page(page_id):
    """
    Soft deletes a specific page. Flashes link to user to undo action
    """
    if 'username' in session:
        page = models.Page(page_id)
        page.set_delete()
        flash("Page '%s' deleted successfully. <a href='/undelete/%d'>Undo</a>"\
         % (page.title, page.page_id))
        return redirect("/")
    flash("You must be logged in to delete a page")
    return redirect("/login")

@APP.route("/undelete/<int:page_id>")
def undelete_page(page_id):
    """
    Sets 'deleted' attribute back to 0, effectively restoring the page.
    """
    page = models.Page(page_id)
    page.set_delete(False)
    flash("Page '%s' restored successfully." % page.title)
    return redirect("/")

@APP.route("/history/<int:page_id>")
@register_breadcrumb(APP, '.view.history', 'Revision History')
def show_history(page_id):
    """
    Shows historical versions of a page given the page id.
    """
    if 'username' in session:
        current_version = models.Page(page_id)
        page_list = current_version.get_revisions()
        return render_template("history.html", page_list=page_list, \
        title="Revision History: %s" % current_version.title)
    flash("You must be logged in to view revision history")
    return redirect("/login")

@APP.route("/rollback/<int:revision_id>")
def rollback(revision_id):
    """
    Updates the page table with content from a given historical snapshot in the
    revisions table. Takes the PK id in revisions table as arg
    """
    pull_from = models.Revision(revision_id)
    overwrite_with = models.Page(pull_from.page_id)
    overwrite_with.title = pull_from.title
    overwrite_with.content = pull_from.content
    overwrite_with.modified_by = pull_from.modified_by
    overwrite_with.deleted = pull_from.deleted
    overwrite_with.save()
    flash("Page %s rolled back successfully." % overwrite_with.title)
    return redirect("/")

if __name__ == "__main__":
    APP.run()
