"""Basic Map App using Google's API"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, jsonify, redirect, session, flash
# import geocoder
from model import connect_to_db, db, User, Route, Run, Outage
import server_utilities as util
from datetime import datetime

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def login_form():
    """Show form for user signup"""

    return render_template("login_form.html")


# Login, logout, and registration functions
@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    register_email = request.form["register-email"]
    password = request.form["password"]

    print register_email
    # TODO: check if username is already taken

    if User.email_in_database(register_email) is not None:
        print "not none"
    new_user = User(email=register_email, password=password)
    print new_user

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % register_email)
    print "new user added"

    return redirect("/")


@app.route('/login_form', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/")

    session["user_id"] = user.user_id

    flash("Logged in.  Welcome %s!" % email)
    # return redirect("/users/%s" % user.user_id)
    return render_template("homepage.html")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/homepage')
def show_homepage():
    """Show homepage"""

    return render_template('homepage.html')


@app.route('/draw-route')
def get_addresses():
    """Draw route on map based on user entered text for start and end address"""

    start = request.args.get("start")
    end = request.args.get("end")

    start_coordinates = util.get_lat_long(start)
    end_coordinates = util.get_lat_long(end)

    start_lat, start_long = start_coordinates
    end_lat, end_long = end_coordinates

    return render_template("show-map.html",
                           start_lat=start_lat,
                           start_long=start_long,
                           end_lat=end_lat,
                           end_long=end_long)


# ROUTES
@app.route("/new-route", methods=["POST"])
def add_route():
    """Add a running route to the database"""

    start_lat = request.form.get("start-lat")
    start_long = request.form.get("start-long")
    end_lat = request.form.get("end-lat")
    end_long = request.form.get("end-long")

    date = datetime.now()
    route = request.form.get("route")
    distance = request.form.get("distance")
    favorite = request.form.get("favorite")

    # # write to db
    new_route = Route(route_name=route, add_date=date, start_lat=start_lat, start_long=start_long, end_lat=end_lat, end_long=end_long, route_distance=distance, favorite=favorite)
    db.session.add(new_route)
    db.session.commit()

    print "start_lat is %s, start_long is %s, end_long is %s, end_long is %s, name is %s, distance is %s, favorite is %s" % (start_lat, start_long, end_lat, end_long, route, distance, favorite)
    return "Route %s has been saved to your routes" % route


@app.route("/routes")
def route_list():
    """Show list of routes."""

    routes = Route.query.all()
    return render_template("route_list.html", routes=routes)


# route to return json of data for all routes
@app.route('/all-route-data.json')
def all_route_data():
    """Return JSON of all routes."""

    allroutedata = {}

    routes = Route.query.all()

    for route in routes:
        string_add_date = datetime.strftime(route.add_date, "%m/%d/%Y")
        allroutedata[route.route_id] = {"route_id": route.route_id, "route_name": route.route_name, "add_date": string_add_date, "route_distance": route.route_distance}

    return jsonify(allroutedata)

# route to return json of data for single route
# @app.route("/single-route-data.json")
# def get_route_by_id():
#     """Return JSON of single route."""

#     current = Route.get_by_id(id_number)

#     # for column in current_route:
#     current.id_number = {"route_name": current.route_name, "add_date": current.add_date}
#     print current


@app.route("/routes/<int:route_id>")
def route_detail(route_id):
    """Show info about route."""

    route = Route.query.get(route_id)
    return render_template("route.html", route=route)


@app.route("/get-saved-route")
def search_route_detail_by_name():
    """Show info about route."""

    search = request.args.get("search")
    route = Route.query.filter_by(route_name=search).first()
    return redirect("routes/%s" % route.route_id)


#  RUNS
@app.route("/runs")
def run_list():
    """Show list of runs, and the route information for each."""

    ran_routes = db.session.query(Run, Route).join(Route).all()
    return render_template("run_list.html", ran_routes=ran_routes)


@app.route("/runs/<int:run_id>")
def run_detail(run_id):
    """Show info about route."""

    run = Run.query.get(run_id)
    route = Route.query.get(run.route_id)

    return render_template("run.html", run=run, route=route)


@app.route('/new-run', methods=["POST"])
def add_route_and_run():
    """Add a run to the database."""

    start_lat = request.form.get("start-lat")
    start_long = request.form.get("start-long")
    end_lat = request.form.get("end-lat")
    end_long = request.form.get("end-long")

    add_date = datetime.now()
    route = request.form.get("route")
    distance = request.form.get("distance")
    favorite = request.form.get("favorite")
    date = request.form.get("date")
    date_type = type(date)
    print "date of run is type %s" % date_type
    print "add_date is %s" % add_date

    # print "route name is %s" % route
    print "start_lat is %s, start_long is %s, end_lat is %s, end_long is %s, name is %s, distance is %s, favorite is %s" % (start_lat, start_long, end_lat, end_long, route, distance, favorite)
    new_route = Route(route_name=route, add_date=add_date, start_lat=start_lat, start_long=start_long, end_lat=end_lat, end_long=end_long, route_distance=distance, favorite=favorite)
    db.session.add(new_route)
    db.session.commit()
    print "route committed"
    d = datetime.strptime(date, "%m/%d/%Y")
    print "d is %s" % (d)

    duration = request.form.get("duration")
    duration = int(duration)

    new_run = Run(run_date=d, route_id=new_route.route_id, duration=duration)
    db.session.add(new_run)
    db.session.commit()

    return "Your run was saved"


# USER PROFILE
@app.route("/profile")
def show_profile():
    """Show the current user's profile page."""

    ran_routes = db.session.query(Run, Route).join(Route).order_by(Run.run_date.desc()).limit(3).all()
    routes = Route.query.order_by(Route.add_date.desc()).limit(3).all()
    return render_template("profile.html", routes=routes, ran_routes=ran_routes)


# Line chart of distance over time
@app.route('/user-distance.json')
def user_distance_data():
    """Return the data of User's distance (km)."""

    labels = []
    data = []

    # Get the run date and route distance for all of a user's runs, in chronological order:
    run_date_distance = db.session.query(Run.run_date, Route.route_distance).order_by(Run.run_date).join(Route).all()

    # For each date, distance tuple, add the date to labels array and the distance
    # to the data array, in string format

    for item in run_date_distance:
        date, distance = item
        labels.append(str(date))
        data.append(str(distance))

    data_dict = {
        "labels": labels,
        "datasets": [
            {
                "label": "Run Distance(km)",
                "fillColor": "rgba(151,187,205,0.2)",
                "strokeColor": "rgba(151,187,205,1)",
                "pointColor": "rgba(151,187,205,1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(151,187,205,1)",
                "data": data
            }
        ]
    }
    return jsonify(data_dict)


# Line chart for pace over time
@app.route('/user-pace.json')
def user_data():
    """Return the data of User's avg pace over time (km)."""

    labels = []
    data = []

   # Get the run date, duration, and route distance for all of a user's runs:
    run_date_distance_duration = db.session.query(Run.run_date, Route.route_distance, Run.duration).order_by(Run.run_date).join(Route).all()

    for item in run_date_distance_duration:
        date, distance, duration = item
        labels.append(str(date))
        km_per_hour = util.get_distance_per_hour(distance, duration)
        data.append(km_per_hour)

    data_dict = {
        "labels": labels,
        "datasets": [
            {
                "label": "Pace (kilometers/hour)",
                "fillColor": "rgba(34,139,34,0.2)",
                "strokeColor": "rgba(34,139,34, 1)",
                "pointColor": "rgba(134,139,34,1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(34,139,34,1)",
                "data": data
            }
        ]
    }
    return jsonify(data_dict)


# MARKER DATA
@app.route('/outages.json')
def get_markers():
    """JSON information about streetlight outages"""

    markers = {}

    outages = Outage.query.all()

    for outage in outages:
        markers[outage.marker_id] = {"outage_lat": outage.outage_lat, "outage_long": outage.outage_long}

    return jsonify(markers)


# ##################################################


if __name__ == "__main__":

    connect_to_db(app)
    # app.run(debug=True)
    app.run()
