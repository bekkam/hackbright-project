"""Basic Map App using Google's API"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
import geocoder
from model import connect_to_db, db, Route, Run

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

    start_lat = geocoder.google(start).latlng[0]
    start_long = geocoder.google(start).latlng[1]

    end_lat = geocoder.google(end).latlng[0]
    end_long = geocoder.google(end).latlng[1]

    return render_template("show-map.html",
                            start_lat=start_lat,
                            start_long=start_long,
                            end_lat=end_lat,
                            end_long=end_long)


@app.route('/new-route')
def add_route():
    """Add a running route to the database"""

    start = request.args.get("start")
    end = request.args.get("end")
    route = request.args.get("route")
    distance = request.args.get("distance")

    # write to db
    new_route = Route(route_name=route, start_lat_long=start, end_lat_long=end, route_distance=distance)
    db.session.add(new_route)
    db.session.commit()

    return "start is %s, end is %s, name is %s, distance is %s" % (start, end, route, distance)


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


@app.route("/runs")
def run_list():
    """Show list of runs."""

    runs = Run.query.order_by('run_date').all()
    return render_template("run_list.html", runs=runs)


@app.route("/get-saved-route")
def search_route_detail_by_name():
    """Show info about route."""

    search = request.args.get("search")
    # return search
    route = Route.query.filter_by(route_name=search).first()
    return "route id is %s" % (route.route_id)
    # return redirect("routes/%s" % route.route_id)

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run()
