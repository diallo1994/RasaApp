# project/server/models.py
import datetime
from project.server import app, db, bcrypt
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
