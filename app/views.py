from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import app, db
from app.schemas import LocationsSchema, EventSchema
from app.models import Locations, Event, Participants


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
    data = request.json
    try:
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        location = data.get('location')
        about = data.get('location')
    except KeyError:
        return jsonify({"status": "error"})
    if Participants.query.filter_by(email=email).first():
        return jsonify({"status": "error"})
    participant=Participants(
        name=name,
        email=email,
        location=location,
        about=about
    )
    participant.set_password(password)
    participant.save()
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
    name = request.get_json()['name']
    password = request.get_json()['password']
    user = Participants.query.filter_by(name=name).first()
    if user is None or not user.password_valid(password):
        return jsonify({"message": "Bad username or password"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


@app.route('/profile/', methods=["GET"])
@jwt_required
def api_get_profile():
    current_identity = get_jwt_identity()
    return jsonify(current_identity)

