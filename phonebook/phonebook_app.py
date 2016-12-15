"""
Phonebook app with basic CRUD, using Flask and Jinja2 templating.
"""

from flask import Flask, render_template, request, redirect
import mysql.connector

phonebook = Flask("Phonebook")

conn = mysql.connector.connect(
user="root",
password="myfirstsql",
host="127.0.0.1",
database="simple_cms_development"
)
