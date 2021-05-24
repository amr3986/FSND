from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    Migrate(app, db)
    return db



class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    v_name = db.Column(db.String,nullable = False)
    city = db.Column(db.String(120),nullable = False)
    state = db.Column(db.String(120),nullable = False)
    address = db.Column(db.String(120),nullable = False)
    phone = db.Column(db.String(120),nullable = False)
    image_link = db.Column(db.String(500),nullable = True)
    facebook_link = db.Column(db.String(120),nullable = True)
  
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String))
    seek_description = db.Column(db.String(120),nullable = True,default='')
    seek_talent = db.Column(db.String(10),nullable = True,default = 'f')
    website = db.Column(db.String(500),nullable = True)
    show = db.relationship('Show',backref = 'venue',lazy ='dynamic')
    
class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable = False)
    city = db.Column(db.String(120),nullable = False)
    state = db.Column(db.String(120),nullable = False)
    phone = db.Column(db.String(120),nullable = False)
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500),nullable = True)
    facebook_link = db.Column(db.String(120),nullable = True,default = '')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    seek_description = db.Column(db.String(120),nullable = True,default='')
    seek_venue = db.Column(db.String(10),nullable = True,default = 'f')
    website = db.Column(db.String(500),nullable = True,default = '')
    show = db.relationship('Show',backref = 'artist',lazy ='dynamic')

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = "Show"
    id = db.Column(db.Integer,primary_key = True)
    start_time = db.Column(db.String(),nullable = False)
    artist_id= db.Column(db.Integer, db.ForeignKey('Artist.id'),nullable=False)
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'),nullable = False)