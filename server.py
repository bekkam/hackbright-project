"""Basic Map App using Google's API"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import geocoder

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def index():
    """Show form for creating route"""

    return render_template("index.html")


@app.route('/get-route')
def get_addresses():
    """Create map with route & based on user entered start and end address text"""

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



if __name__ == "__main__":
    app.debug = True
    # connect_to_db(app)
    DebugToolbarExtension(app)
    app.run()
