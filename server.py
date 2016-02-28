"""Basic Map App using Google's API"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
import geocoder
from model import connect_to_db, db, Route, Run
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
@app.route("/new-route", methods=['POST'])
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

    # print "start is %s, end is %s, name is %s, distance is %s, favorite is %s" % (start, end, route, distance, favorite)
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
    """Show list of runs."""

    runs = Run.query.order_by('run_date').all()
    return render_template("run_list.html", runs=runs)


@app.route("/runs/<int:run_id>")
def run_detail(run_id):
    """Show info about route."""

    run = Run.query.get(run_id)

    return render_template("run.html", run=run)


@app.route('/new-run', methods=['POST'])
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
    return "your run was saved"


# USER PROFILE
@app.route("/profile")
def show_profile():
    """Show the current user's profile page."""

    # TODO: Add user, routes and runs, and pass to template
    # runs = Run.query.order_by('run_date').all()
    return render_template("profile.html")


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run()
