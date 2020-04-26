from marshmallow import Schema, fields


class EventSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()
    date = fields.Date()
    time = fields.Time()
    event_type = fields.String()
    category_type = fields.String()
    address = fields.String()
    seats = fields.Integer()
    location = fields.Nested("LocationsSchema")


class ParticipatesSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    email = fields.String()
    password = fields.String()
    picture = fields.String()
    location = fields.String()
    about = fields.String()
    enrollmants = fields.Nested("EnrollmentsSchema")
    events = fields.Nested("EventSchema")


class EnrollmentsSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date()
    event = fields.Nested("EventSchema")
    participant = fields.Nested("ParticipatesSchema")


class LocationsSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    code = fields.String()


class AccossiationShema(Schema):
    id = fields.Integer(dump_only=True)
    event_id = fields.Nested("EventSchema")
    participant_id = fields.Nested("ParticipatesSchema")
    event = fields.Nested("EventSchema")
    participant = fields.Nested("ParticipatesSchema")
