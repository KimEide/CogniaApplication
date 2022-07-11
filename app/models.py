from email.policy import default
from sqlalchemy import true
from app import db

class RestAreas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    num_small_vehicle = db.Column(db.Integer, index=True, unique=True)
    num_big_vehicle = db.Column(db.Integer, index=True, unique=True)
    lokasjon = db.Column(db.String(160), index=True, unique=True)
    href = db.Column(db.String(160), index=True, unique=True)

    def __repr__(self):
        return '<RestArea {}>'.format(self.name)

class Dusj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    href = db.Column(db.String(160), index=True, unique=True)

class Drikkevann(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    href = db.Column(db.String(160), index=True, unique=True)

class Strøm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    href = db.Column(db.String(160), index=True, unique=True)  

class Parkeringsområde(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parkeringstilbyderNavn = db.Column(db.String(160), index=True, unique=True)
    breddegrad = db.Column()
    lengdegrad = db.Column()
    deaktivert = db.Column(db.Boolean, default=False)
    versjonsnumber = db.Column(db.Integer)
    navn = db.Column(db.String(160), index=True, unique=True)
    adresse = db.Column(db.String(160), index=True, unique=True)
    postnummer = db.Column(db.Integer)
    poststed = db.Column(db.String(160), index=True, unique=True)
    aktiveringsTidspunkt = db.Column(db.String(160), index=True, unique=True)

class Parkeringstilbyder(db.Model):
    id = db.Column(db.Integer)
    organisasjonsnummer = db.Column(db.Integer)
    navn = db.Column(db.String(160), index=True, unique=True, primary_key=True)
