"""Basic Map App using Google's API"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
import geocoder
from model import connect_to_db, db, Route, Run, Outage
from datetime import datetime

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def index():
    """Show blank map and form for addresses"""

    return render_template("index.html")


@app.route('/draw-route')
def get_addresses():
    """Draw route on map based on user entered text for start and end address"""

    # get user entered start addresses, and convert it to latlng
    start = request.args.get("start")
    end = request.args.get("end")
    print "start is ", start

    start_lat = geocoder.google(start).latlng[0]
    start_long = geocoder.google(start).latlng[1]

    end_lat = geocoder.google(end).latlng[0]
    end_long = geocoder.google(end).latlng[1]

    print "start_lat is ", start_lat
    return render_template("show-map.html",
                           start_lat=start_lat,
                           start_long=start_long,
                           end_lat=end_lat,
                           end_long=end_long)
    # return jsonify({"start_latitude": start_lat, "start_longitude": start_long,
    #             "end_latitude": end_lat, "end_longitude": end_long})


# ROUTES
@app.route("/new-route", methods=["POST"])
def add_route():
    """Add a running route to the database"""

    start = request.form.get("start")
    end = request.form.get("end")
    date = datetime.now()
    route = request.form.get("route")
    distance = request.form.get("distance")
    favorite = request.form.get("favorite")

    # # write to db
    new_route = Route(route_name=route, add_date=date, start_lat_long=start, end_lat_long=end, route_distance=distance, favorite=favorite)
    db.session.add(new_route)
    db.session.commit()

    print "start is %s, end is %s, name is %s, distance is %s, favorite is %s" % (start, end, route, distance, favorite)
    return "Route %s has been saved to your routes" % route


@app.route("/routes")
def route_list():
    """Show list of routes."""

    routes = Route.query.all()
    return render_template("route_list.html", routes=routes)


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
    """Add a run to the database"""

    start = request.form.get("start")
    end = request.form.get("end")
    date = datetime.now()
    route = request.form.get("route")
    distance = request.form.get("distance")
    favorite = request.form.get("favorite")

    print "route name is %s" % route
    new_route = Route(route_name=route, add_date=date, start_lat_long=start, end_lat_long=end, route_distance=distance, favorite=favorite)
    db.session.add(new_route)
    db.session.commit()

    run_date = request.form.get("date")
    d = datetime.strptime(run_date, "%m/%d/%Y")

    duration = request.form.get("duration")
    duration = int(duration)

    new_run = Run(run_date=d, route_id=new_route.route_id, duration=duration)
    db.session.add(new_run)
    db.session.commit()

    # print "d is %s, duration is %s" % (d, duration)
    return "Your run was saved"


# USER PROFILE
@app.route("/profile")
def show_profile():
    """Show the current user's profile page."""

    ran_routes = db.session.query(Run, Route).join(Route).order_by(Run.run_date.desc()).limit(3).all()
    # runs = Run.query.order_by(Run.run_date.desc()).limit(3).all()
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
        date = item[0]
        labels.append(str(date))
        distance = item[1]
        distance = str(distance)
        data.append(distance)

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
    run_date_distance_duration = db.session.query(Run.run_date, Route.route_distance, Run.duration).join(Route).all()

    for item in run_date_distance_duration:
        date = item[0]
        labels.append(str(date))

        distance = item[1]
        duration = item[2]
        km_per_hour = (distance/duration) * 60
        km_per_hour = str(round(km_per_hour, 2))
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
    app.debug = True

    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run()
