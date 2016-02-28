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
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Route(db.Model):
    """A route on a map"""

    __tablename__ = "routes"

    route_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    route_name = db.Column(db.String(100))
    add_date = db.Column(db.DateTime)
    start_lat_long = db.Column(db.String(80))
    end_lat_long = db.Column(db.String(80))
    route_distance = db.Column(db.Float)
    favorite = db.Column(db.Boolean)

    # Define relationship to user: a user has many routes
    # user = db.relationship("User",
    #                        backref=db.backref("routes"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Route route_id=%s, route_name=%s, start_lat_long=%s, end_lat_long=%s, route_distance=%s >" % (self.route_id, self.route_name, self.start_lat_long, self.end_lat_long, self.route_distance)


class Run(db.Model):
    """A route on a map, that user has run."""

    __tablename__ = "runs"

    run_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    run_date = db.Column(db.Date)
    duration = db.Column(db.Integer)

    # Define relationship to route: a route has many runs
    route = db.relationship("Route",
                            backref=db.backref("runs", order_by=run_date))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Run_id=%s run_date=%s>" % (self.run_id, self.run_date)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://' + username + ':' + password + '@localhost/runningapp'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rmurphy:hackbright@localhost/runningapp'


    # in seed file, use db.create_all() to create tables .. or by hand for now

    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
