from flask import Flask, jsonify, request
from app import app, db
from app.schemas import LocationsSchema, EventSchema
from app.models import Locations, Event, Participants
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/')
def main():
    return 'Hello!'

@app.route('/locations/', methods=["GET"])
def api_get_locations():
    locations = LocationsSchema(many=True)
    return jsonify(locations.dump(Locations.query.all()))

@app.route('/events/', methods=["GET"])
def api_get_events():
    events = EventSchema(many=True)
    eventtype = request.args.get("eventtype",type=str)
    location = request.args.get("location")
    if eventtype:
        return jsonify(events.dump(Event.query.filter_by(event_type=eventtype).all()))
    if location:
        return jsonify(events.dump(Event.query.filter(Event.location.has(Locations.code==location))))
    return jsonify(events.dump(Event.query.all()))

@app.route('/enrollments/id=<int:eventid>/', methods=["POST","DELETE"])
@jwt_required
def api_post_event():
    return jsonify({'status':'success'})

@app.route('/register/', methods=["POST"])
def api_post_register():
    try:
        name=request.get_json()['name']
        email=request.get_json()['email']
        password=request.get_json()['password']
        location=request.get_json()['location']
        about=request.get_json()['about']
    except KeyError:
        return jsonify({"status": "error"})
    if Participants.query.filter_by(email=email).first():
        return jsonify({"status": "error"})
    participant=Participants(
        name=name,
        email=email,
        password=password,
        location=location,
        about=about
    )
    db.session.add(participant)
    db.session.commit()
    return jsonify(dict(id=Participants.query.count(),
                    name=name,
                    email=email,
                    password=password,
                    location=location,
                    about=about))

@app.route('/auth/', methods=["POST"])
def api_post_auth():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    username = request.get_json()['username']
    password = request.get_json()['password']

    if password != "test":
        return jsonify({"message": "Bad username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/profile/', methods=["GET"])
@jwt_required
def api_get_profile():
    current_identity = request.get_json()
    return jsonify(current_identity)

