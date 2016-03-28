"""Models and database functions for Running App."""

from flask_sqlalchemy import SQLAlchemy

from config import username, password

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    """User of SafeRun website."""

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
    def add(cls, email, password):
        """Add a new user to the database"""

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    @classmethod
    def get_by_email(cls, some_email):
        """Return the user with the specified email from the database"""

        return User.query.filter_by(email=some_email).first()


class Route(db.Model):
    """A route on a map"""

    __tablename__ = "routes"

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
    polyline = db.Column(db.String(1500))
    directions_text = db.Column(db.String(2000))
    directions_distance = db.Column(db.String(200))
    start_address = db.Column(db.String(100))
    end_address = db.Column(db.String(100))

    # Define relationship to user: a user has many routes
    user = db.relationship("User", backref=db.backref("routes"))

    def __init__(self, user_id, route_name, add_date, start_lat, start_long,
                 end_lat, end_long, route_distance, favorite, polyline,
                 directions_text, directions_distance, start_address,
                 end_address):
        self.user_id = user_id
        self.route_name = route_name
        self.add_date = add_date
        self.start_lat = start_lat
        self.start_long = start_long
        self.end_lat = end_lat
        self.end_long = end_long
        self.route_distance = route_distance
        self.favorite = favorite
        self.polyline = polyline
        self.directions_text = directions_text
        self.directions_distance = directions_distance
        self.start_address = start_address
        self.end_address = end_address

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s, Route route_id=%s, route_name=%s, add_date=%s, start_lat=%s,start_long=%s, end_lat=%s, end_long=%s, route_distance=%s, favorite=%s, polyline=%s, directions_text=%s, directions_distance=%s, start_address=%s, end_address=%s>" % (self.user_id, self.route_id, self.route_name, self.add_date, self.start_lat, self.start_long, self.end_lat, self.end_long, self.route_distance, self.favorite, self.polyline, self.directions_text, self.directions_distance, self.start_address, self.end_address)

    @classmethod
    def get_all(cls):
        """Return all routes from the database"""

        return Route.query.all()

    @classmethod
    def get_by_id(cls, route_id):
        """Return a route with a given id from the database"""

        return Route.query.get(route_id)

    @classmethod
    def get_by_route_name(cls, search_term):
        """Return a route with a given name from the database"""

        print Route.query.filter_by(route_name=search_term).first()
        return Route.query.filter_by(route_name=search_term).first()

    def add(self):
        """Add a new route to the database"""

        new_route = Route(user_id=self.user_id, route_name=self.route_name,
                          add_date=self.add_date, start_lat=self.start_lat,
                          start_long=self.start_long, end_lat=self.end_lat,
                          end_long=self.end_long,
                          route_distance=self.route_distance,
                          favorite=self.favorite,
                          polyline=self.polyline,
                          directions_text=self.directions_text,
                          directions_distance=self.directions_distance,
                          start_address=self.start_address,
                          end_address=self.end_address
                          )
        db.session.add(new_route)
        db.session.commit()
        print "route added in model"


class Run(db.Model):
    """A route on a map, that user has run."""

    __tablename__ = "runs"

    run_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    run_date = db.Column(db.Date)
    duration = db.Column(db.Integer)

    # Define relationship to route: a route has many runs
    route = db.relationship("Route", backref=db.backref("runs", order_by=run_id))

    # Define relationship to user: a user has many runs
    user = db.relationship("User", backref=db.backref("users"))

    def __init__(self, user_id, route_id, run_date, duration):
        self.user_id = user_id
        self.route_id = route_id
        self.run_date = run_date
        self.duration = duration

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Run_id=%s Route_id=%s run_date=%s duration=%s>" % (self.run_id, self.route_id, self.run_date, self.duration)

    def add(self):
        """Add a new run to the database"""

        new_run = Run(user_id=self.user_id, route_id=self.route_id, run_date=self.run_date,
                      duration=self.duration)
        db.session.add(new_run)
        db.session.commit()
        print "run added in model"


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


def connect_to_test_db(app):
    """Connect a test database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://' + username + ':' + password + '@localhost/testdb'

    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
