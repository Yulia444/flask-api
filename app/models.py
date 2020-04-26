from app import db
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ENUM


class Association(db.Model):
    __tablename__ = 'events_participants'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'))

    event = db.relationship('Event', back_populates="participants")
    participant = db.relationship('Participants', back_populates="events")

   
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    date = db.Column(db.DateTime, default=date.today())
    time = db.Column(db.DateTime, default=datetime.now().time())
    event_type = db.Column(db.Enum('HACKATON', 'GAME', 'WORKSHOP',
                                   name='event_type'), default='GAME')
    category_type = db.Column(db.Enum('PYTHON', 'ML', 'PROJECT_MANAGMENT',
                                      name='category_type'), default='PYTHON')
    address = db.Column(db.String(255))
    seats = db.Column(db.Integer)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    location = db.relationship('Locations', back_populates='event')
    participants = db.relationship('Association', back_populates="event")


class Participants(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    picture = db.Column(db.String(50))
    location = db.Column(db.String(255), nullable=False)
    about = db.Column(db.String(1000), nullable=False)
    enrollments = db.relationship('Enrollments', back_populates='participant')
    events = db.relationship('Association', back_populates="participant")

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def password_valid(self, password):
        return check_password_hash(self.password, password)


class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=date.today())
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship('Event')
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'))
    participant = db.relationship('Participants', back_populates='enrollments')


class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    code = db.Column(db.String(10))
    event = db.relationship('Event', uselist=False, back_populates='location')


