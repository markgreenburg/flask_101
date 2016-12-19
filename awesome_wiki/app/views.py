from flask import Flask, render_template, request, redirect
import mysql.connector
from models import *
import config

# Initialize new Flask app
app = Flask("awesome_wiki")
# Load root-level config.py file -> not in version control. Contains DB
# and debug settings
app.config.from_object('config')

@app.route("/")
def homepage():
    """
    Directory of all pages in the wiki
    """

@app.route("/<page_name>")
def show_page():
    """
    Shows the contents of a specific page
    """

@app.route("/<page_name>/edit")
def edit_page():
    """
    Shows form to edit the content of the current page
    """


@app.route("/<page_name>/save")
def save_page():
    """
    Saves the new form content
    """


@app.route("/<page_name>/delete")
def delete_page():
    """
    Soft deletes a specific page
    """
