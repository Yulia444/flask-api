from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app, db
from app.models import Event, Participants,  Enrollments
from app.models import Locations

admin = Admin(app)
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Participants, db.session))
admin.add_view(ModelView(Enrollments, db.session))
admin.add_view(ModelView(Locations, db.session))

