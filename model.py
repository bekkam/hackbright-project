"""Models and database functions for Running App project."""
# To access operating system environment variables
import os

from flask_sqlalchemy import SQLAlchemy

username = os.environ['PGUSER']
password = os.environ['PGPASSWORD']

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    """User of run mapping website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s password=%s>" % (self.user_id, self.email, self.password)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @classmethod
    def email_in_database(cls, some_email):
        """Return true if a given email is in the User table"""

        return True if User.query.filter_by(email=some_email).first() is not None else False


class Route(db.Model):
    """A route on a map"""

    __tablename__ = "routes"

    # _SELECT_SQL = "SELECT * FROM Routes WHERE route_id = :route_id"

    route_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    route_name = db.Column(db.String(100))
    add_date = db.Column(db.Date)
    start_lat = db.Column(db.Float)
    start_long = db.Column(db.Float)
    end_lat = db.Column(db.Float)
    end_long = db.Column(db.Float)
    route_distance = db.Column(db.Float)
    favorite = db.Column(db.Boolean)

    # Define relationship to user: a user has many routes
    user = db.relationship("User",
                           backref=db.backref("routes"))
    # def __init__(self, name):
    #     self.name = name

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Route route_id=%s, route_name=%s, add_date=%s, start_lat=%s, start_long=%s, end_lat=%s, end_long=%s, route_distance=%s, favorite=%s>" % (self.route_id, self.route_name, self.add_date, self.start_lat, self.start_long, self.end_lat, self.end_long, self.route_distance, self.favorite)

# ################# new code
    @classmethod
    def get_by_id(cls, route_id):
        """Get a route with a given id from database."""

        return cls.query.get(route_id)

# ############## new code


class Run(db.Model):
    """A route on a map, that user has run."""

    __tablename__ = "runs"

    run_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    run_date = db.Column(db.Date)
    duration = db.Column(db.Integer)

    # Define relationship to route: a route has many runs
    route = db.relationship("Route",
                            backref=db.backref("runs", order_by=run_id))

    # Define relationship to user: a user has many runs
    user = db.relationship("User",
                           backref=db.backref("users"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Run_id=%s Route_id=%s run_date=%s duration=%s>" % (self.run_id, self.route_id, self.run_date, self.duration)


class Outage(db.Model):
    """A location on a map, corresponding to a streetlight outage."""

    __tablename__ = "outages"

    marker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    outage_lat = db.Column(db.String(20))
    outage_long = db.Column(db.String(20))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<marker_id=%s, outage_lat=%s, outage_long=%s>" % (self.marker_id, self.outage_lat, self.outage_long)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://' + username + ':' + password + '@localhost/runningapp'

    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
