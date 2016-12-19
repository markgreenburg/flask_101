"""
Defines CRUD models for the phonebook
"""

from __init__ import db

class Contact(db.Model):
    """
    Defines a unique contact. Has ID (PK, NN, AI), fname, lname, and a link to
    a profile image
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(35))
    lname = db.Column(db.String(35))
    profile_img = db.Column(db.String(250))
