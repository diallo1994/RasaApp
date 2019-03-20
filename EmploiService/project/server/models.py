# project/server/models.py
import datetime
from project.server import app, db, bcrypt

class Offres(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "offres"

    idoffre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomentreprise = db.Column(db.String(255), unique=False, nullable=False)
    zone= db.Column(db.String(255), unique=False, nullable=False)
    libelle = db.Column(db.String(255), unique=False, nullable=False)
    nomentreprise = db.Column(db.String(255), unique=False, nullable=False)
    idemploi = db.Column(db.Integer, db.ForeignKey('emplois.idemploi'),
        nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    url=nomentreprise = db.Column(db.String(500), unique=False, nullable=False)

class Metier(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "metier"

    idmetier = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nommetier = db.Column(db.String(255), unique=False, nullable=False)
    secteur = db.Column(db.Integer, db.ForeignKey('secteur.idSecteur'),
        nullable=False)
    emplois = db.relationship('Emplois', backref='metier', lazy=True)

class Secteur(db.Model):
    __tablename__ = "secteur"
    idsecteur=db.Column(db.Integer,primary_key=True, autoincrement=True)
    nomsecteur=db.Column(db.String(255), unique=False, nullable=False)
    metier=db.relationship('Metier', backref='secteur', lazy='true')

class Emplois(db.Model):
    __tablename__ = "emplois"
    idemploi=db.Column(db.Integer,primary_key=True, autoincrement=True)
    nomemploi=db.Column(db.String(255), unique=False, nullable=False)
    offres=db.relationship('Offres', backref='emplois', lazy='true')
