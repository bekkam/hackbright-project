"""Basic Map App using Google's API"""

from datetime import datetime

from flask import Flask, render_template, request, jsonify, redirect, session, flash, g
from jinja2 import StrictUndefined

from model import connect_to_db, db, User, Route, Run, Outage
import server_utilities as util

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined

JS_TESTING_MODE = False


# @app.before_request runs before every web request - we put code here
# that should execute then
@app.before_request
def add_tests():

    # g variable is Flask's "request global", an object you can attach
    # arbitrary instance attributes to.  It is automatically passsed to each
    # template rendering, so we can use it as a way to pass info to templates
    # w/o having to explicitly wire that into each call to render_template()
    g.jasmine_tests = JS_TESTING_MODE


@app.route('/', methods=['GET'])
def login_form():
    """Show form for user signup"""

    return render_template("login_form.html")


# Login, logout, and registration functions
@app.route('/register', methods=['POST', 'GET'])
def registration_process():
    """Process registration."""

    email = request.form["register-email"]
    password = request.form["password"]

    if User.get_by_email(email):
        flash("That email is already registered.  ")
        flash("Please register with a different email.")

        print "email already taken"
        return redirect("/")

    User.add(email, password)

    flash("Registration successful.  Welcome %s!" % email)
    return render_template("homepage.html")


@app.route('/login_form', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.get_by_email(email)

    if not user:
        flash("No such user")
        return redirect("/")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/")

    session["user_id"] = user.user_id

    flash("Logged in.  Welcome %s!" % email)
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

    start_lat, start_long = util.get_lat_long(start)
    end_lat, end_long = util.get_lat_long(end)

    return render_template("show-map.html",
                           start_lat=start_lat,
                           start_long=start_long,
                           end_lat=end_lat,
                           end_long=end_long)


# ROUTES
@app.route("/new-route", methods=["POST"])
def add_route():
    """Add a running route to the database"""

    print "/new-route called"
    user_id = session["user_id"]
    print user_id
    route = request.form.get("route")

    polyline = request.form.get("overview-polyline")
    # print "polyline is ", polyline

    directions_text = request.form.get("directions-text")
    directions_distance = request.form.get("directions-distance")

    print directions_text
    print directions_distance

    new_route = Route(user_id=user_id, route_name=route,
                      add_date=datetime.now(),
                      start_lat=request.form.get("start-lat"),
                      start_long=request.form.get("start-long"),
                      end_lat=request.form.get("end-lat"),
                      end_long=request.form.get("end-long"),
                      route_distance=request.form.get("distance"),
                      favorite=request.form.get("favorite"),
                      polyline=polyline,
                      directions_text=directions_text,
                      directions_distance=directions_distance
                      )
    new_route.add()

    return "Route %s has been saved to your routes" % route


@app.route("/routes")
def route_list():
    """Show list of routes."""

    return render_template("route_list.html")


@app.route('/all-route-data.json')
def all_route_data():
    """Return JSON of all routes."""

    allroutedata = {}

    routes = Route.get_all()

    for route in routes:
        string_add_date = datetime.strftime(route.add_date, "%m/%d/%Y")
        allroutedata[route.route_id] = {"route_id": route.route_id,
                                        "route_name": route.route_name,
                                        "add_date": string_add_date,
                                        "route_distance": route.route_distance}

    return jsonify(allroutedata)


@app.route("/routes/<int:route_id>")
def route_detail(route_id):
    """Show info about route."""

    print Route.get_by_id(route_id)

    return render_template("route.html", route=Route.get_by_id(route_id))


@app.route("/route-detail.json", methods=['POST'])
def route_detail_json():
    """Return JSON of individual route."""

    route_data = {}

    route_id = request.form.get("routeId")
    route = Route.get_by_id(route_id)

    string_add_date = datetime.strftime(route.add_date, "%m/%d/%Y")

    waypoints = util.decode_polyline(route.polyline)

    route_data = {"route_id": route.route_id,
                  "route_name": route.route_name,
                  "add_date": string_add_date,
                  "route_distance": route.route_distance,
                  "waypoints": waypoints,
                  "directions_text": route.directions_text,
                  "directions_distance": route.directions_distance
                  }
    # print route_data
    return jsonify(route_data)


@app.route("/get-saved-route")
def search_route_detail_by_name():
    """Show info about route."""

    print "search term is ", request.args.get("search")
    route = Route.get_by_route_name(request.args.get("search"))
    print route

    return redirect("routes/%s" % route.route_id)


#  RUNS
@app.route("/runs")
def run_list():
    """Show list of runs, and the route information for each."""

    return render_template("run_list.html")


@app.route('/all-run-data.json')
def all_run_data():
    """Return JSON of all routes."""

    all_run_data = {}
    ran_routes = db.session.query(Run, Route).join(Route).all()

    for ran_route in ran_routes:
        string_run_date = datetime.strftime(ran_route[0].run_date, "%m/%d/%Y")
        all_run_data[ran_route[0].run_id] = {"run_id": ran_route[0].run_id,
                                             "route_name": ran_route[1].route_name,
                                             "run_date": string_run_date,
                                             "route_distance": ran_route[1].route_distance,
                                             "duration": ran_route[0].duration}
    return jsonify(all_run_data)


@app.route("/runs/<int:run_id>")
def run_detail(run_id):
    """Show info about route."""

    run = Run.query.get(run_id)
    route = Route.query.get(run.route_id)

    return render_template("run.html", run=run, route=route)


@app.route("/run-detail.json", methods=['POST'])
def run_detail_json():
    """Return JSON of individual run."""

    run_data = {}

    run_id = request.form.get("runId")
    run = Run.query.get(run_id)
    route = Route.get_by_id(run.route_id)

    string_run_date = datetime.strftime(run.run_date, "%m/%d/%Y")

    waypoints = util.decode_polyline(route.polyline)

    run_data = {"run_id": run.run_id,
                "route_name": route.route_name,
                "run_date": string_run_date,
                "route_distance": route.route_distance,
                "duration": run.duration,
                "waypoints": waypoints}
    # print run_data
    return jsonify(run_data)


@app.route('/new-run', methods=["POST"])
def add_route_and_run():
    """Add a run to the database."""

    print "/new-run in server.py called"
    start_lat = request.form.get("start-lat")
    start_long = request.form.get("start-long")
    end_lat = request.form.get("end-lat")
    end_long = request.form.get("end-long")

    add_date = datetime.now()
    route = request.form.get("route")
    distance = request.form.get("distance")
    favorite = request.form.get("favorite")
    date = request.form.get("date")
    user_id = session["user_id"]
    polyline = request.form.get("overview-polyline")

    # print "start_lat is %s, start_long is %s, end_lat is %s, end_long is %s, name is %s, distance is %s, favorite is %s" % (start_lat, start_long, end_lat, end_long, route, distance, favorite)

    new_route = Route(user_id=user_id, route_name=route, add_date=add_date,
                      start_lat=start_lat, start_long=start_long,
                      end_lat=end_lat, end_long=end_long,
                      route_distance=distance, favorite=favorite,
                      polyline=polyline
                      )

    new_route.add()
    # print "route committed"

    route_id = Route.get_by_route_name(route).route_id
    d = datetime.strptime(date, "%m/%d/%Y")
    duration = request.form.get("duration")
    duration = int(duration)

    new_run = Run(user_id=user_id, route_id=route_id, run_date=d, duration=duration)
    new_run.add()

    return "Your run was saved"


# USER PROFILE
@app.route("/profile")
def show_profile():
    """Show the current user's profile page."""

    return render_template("profile.html")


@app.route('/three-recent-routes.json')
def recent_route_data():
    """Return JSON of the three most recently added routes."""

    recent_routes_data = {}
    recent_routes = Route.query.order_by(Route.add_date.desc()).limit(3).all()

    for recent_route in recent_routes:
        string_add_date = datetime.strftime(recent_route.add_date, "%m/%d/%Y")
        recent_routes_data[recent_route.route_id] = {"route_id": recent_route.route_id,
                                                     "route_name": recent_route.route_name,
                                                     "add_date": string_add_date,
                                                     "route_distance": recent_route.route_distance}

    return jsonify(recent_routes_data)


@app.route('/three-recent-runs.json')
def recent_run_data():
    """Return JSON of the three most recent runs."""

    recent_runs_data = {}
    recent_runs = db.session.query(Run, Route).join(Route).order_by(Run.run_date.desc()).limit(3).all()

    for recent_run in recent_runs:
        string_run_date = datetime.strftime(recent_run[0].run_date, "%m/%d/%Y")
        recent_runs_data[recent_run[0].run_id] = {"run_id": recent_run[0].run_id,
                                                  "route_name": recent_run[1].route_name,
                                                  "run_date": string_run_date,
                                                  "route_distance": recent_run[1].route_distance,
                                                  "duration": recent_run[0].duration}

    return jsonify(recent_runs_data)


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

    import sys
    if sys.argv[-1] == "jstest":
        JS_TESTING_MODE = True

    connect_to_db(app)
    app.run(debug=True)

    # app.run()
