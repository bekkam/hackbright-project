"""Basic Map App using Google's API"""

from datetime import datetime

from flask import Flask, render_template, request, jsonify, redirect, session, flash, g
from jinja2 import StrictUndefined

from model import connect_to_db, db, User, Course, Run, Outage
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


@app.route('/draw-course')
def get_addresses():
    """Draw path on map based on user entered text for start and end address"""

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
@app.route("/new-course", methods=["POST"])
def add_course():
    """Add a running course to the database"""

    print "/new-course called"
    user_id = session["user_id"]
    print user_id
    course = request.form.get("course")

    polyline = request.form.get("overview-polyline")
    # print "polyline is ", polyline

    directions_text = request.form.get("directions-text")
    directions_distance = request.form.get("directions-distance")

    start_address = request.form.get("start-address")
    end_address = request.form.get("end-address")

    new_course = Course(user_id=user_id, course_name=course,
                        add_date=datetime.now(),
                        start_lat=request.form.get("start-lat"),
                        start_long=request.form.get("start-long"),
                        end_lat=request.form.get("end-lat"),
                        end_long=request.form.get("end-long"),
                        course_distance=request.form.get("distance"),
                        favorite=request.form.get("favorite"),
                        polyline=polyline,
                        directions_text=directions_text,
                        directions_distance=directions_distance,
                        start_address=start_address,
                        end_address=end_address
                        )
    new_course.add()

    return "Course %s has been saved to your courses" % course


@app.route("/courses")
def course_list():
    """Show list of courses."""

    return render_template("course_list.html")


@app.route('/all-course-data.json')
def all_course_data():
    """Return JSON of all courses."""

    all_course_data = {}

    courses = Course.get_all()

    for course in courses:
        string_add_date = datetime.strftime(course.add_date, "%m/%d/%Y")
        all_course_data[course.course_id] = {"course_id": course.course_id,
                                             "course_name": course.course_name,
                                             "add_date": string_add_date,
                                             "course_distance": course.course_distance}

    return jsonify(all_course_data)


@app.route("/courses/<int:course_id>")
def route_detail(course_id):
    """Show info about course."""

    print Course.get_by_id(course_id)

    return render_template("course.html", course=Course.get_by_id(course_id))


@app.route("/course-detail.json", methods=['POST'])
def course_detail_json():
    """Return JSON of individual course."""

    course_data = {}

    course_id = request.form.get("courseId")
    course = Course.get_by_id(course_id)

    string_add_date = datetime.strftime(course.add_date, "%m/%d/%Y")

    waypoints = util.decode_polyline(course.polyline)

    course_data = {"course_id": course.course_id,
                   "course_name": course.course_name,
                   "add_date": string_add_date,
                   "course_distance": course.course_distance,
                   "waypoints": waypoints,
                   "directions_text": course.directions_text,
                   "directions_distance": course.directions_distance,
                   "start_address": course.start_address,
                   "end_address": course.end_address
                   }
    print course_data
    return jsonify(course_data)


@app.route("/get-saved-course")
def search_course_detail_by_name():
    """Show info about course."""

    print "search term is ", request.args.get("search")
    course = Course.get_by_course_name(request.args.get("search"))
    print course

    return redirect("courses/%s" % course.course_id)


#  RUNS
@app.route("/runs")
def run_list():
    """Show list of runs, and the course information for each."""

    return render_template("run_list.html")


@app.route('/all-run-data.json')
def all_run_data():
    """Return JSON of all runs."""

    all_run_data = {}
    courses_ran = db.session.query(Run, Course).join(Course).all()

    for course_ran in courses_ran:
        string_run_date = datetime.strftime(course_ran[0].run_date, "%m/%d/%Y")
        all_run_data[course_ran[0].run_id] = {"run_id": course_ran[0].run_id,
                                              "course_name": course_ran[1].course_name,
                                              "run_date": string_run_date,
                                              "course_distance": course_ran[1].course_distance,
                                              "duration": course_ran[0].duration}
    return jsonify(all_run_data)


@app.route("/runs/<int:run_id>")
def run_detail(run_id):
    """Show info about run."""

    run = Run.query.get(run_id)
    course = Course.query.get(run.course_id)

    return render_template("run.html", run=run, course=course)


@app.route("/run-detail.json", methods=['POST'])
def run_detail_json():
    """Return JSON of individual run."""

    run_data = {}

    run_id = request.form.get("runId")
    run = Run.query.get(run_id)
    course = Course.get_by_id(run.course_id)

    print course
    string_run_date = datetime.strftime(run.run_date, "%m/%d/%Y")

    waypoints = util.decode_polyline(course.polyline)

    run_data = {"run_id": run.run_id,
                "course_name": course.course_name,
                "run_date": string_run_date,
                "course_distance": course.course_distance,
                "duration": run.duration,
                "waypoints": waypoints,
                "directions_text": course.directions_text,
                "directions_distance": course.directions_distance,
                "start_address": course.start_address,
                "end_address": course.end_address
                }
    print run_data
    return jsonify(run_data)


@app.route('/new-run', methods=["POST"])
def add_course_and_run():
    """Add a run to the database."""

    print "/new-run in server.py called"
    start_lat = request.form.get("start-lat")
    start_long = request.form.get("start-long")
    end_lat = request.form.get("end-lat")
    end_long = request.form.get("end-long")

    add_date = datetime.now()
    course = request.form.get("course")
    distance = request.form.get("distance")
    favorite = request.form.get("favorite")
    date = request.form.get("date")
    user_id = session["user_id"]
    polyline = request.form.get("overview-polyline")

    directions_text = request.form.get("directions-text")
    directions_distance = request.form.get("directions-distance")

    start_address = request.form.get("start-address")
    end_address = request.form.get("end-address")

    # print "start_lat is %s, start_long is %s, end_lat is %s, end_long is %s, name is %s, distance is %s, favorite is %s" % (start_lat, start_long, end_lat, end_long, course, distance, favorite)

    new_course = Course(user_id=user_id, course_name=course, add_date=add_date,
                        start_lat=start_lat, start_long=start_long,
                        end_lat=end_lat, end_long=end_long,
                        course_distance=distance, favorite=favorite,
                        polyline=polyline,
                        directions_text=directions_text,
                        directions_distance=directions_distance,
                        start_address=start_address,
                        end_address=end_address
                        )

    new_course.add()
    # print "course committed"

    course_id = Course.get_by_course_name(course).course_id
    d = datetime.strptime(date, "%m/%d/%Y")
    duration = request.form.get("duration")
    duration = int(duration)

    new_run = Run(user_id=user_id, course_id=course_id, run_date=d, duration=duration)
    new_run.add()

    return "Your run was saved"


# USER PROFILE
@app.route("/profile")
def show_profile():
    """Show the current user's profile page."""

    return render_template("profile.html")


@app.route('/three-recent-courses.json')
def recent_course_data():
    """Return JSON of the three most recently added courses."""

    recent_courses_data = {}
    recent_courses = Course.query.order_by(Course.add_date.desc()).limit(3).all()

    for recent_course in recent_courses:
        string_add_date = datetime.strftime(recent_course.add_date, "%m/%d/%Y")
        recent_courses_data[recent_course.course_id] = {"course_id": recent_course.course_id,
                                                        "course_name": recent_course.course_name,
                                                        "add_date": string_add_date,
                                                        "course_distance": recent_course.course_distance}

    return jsonify(recent_courses_data)


@app.route('/three-recent-runs.json')
def recent_run_data():
    """Return JSON of the three most recent runs."""

    recent_runs_data = {}
    recent_runs = db.session.query(Run, Course).join(Course).order_by(Run.run_date.desc()).limit(3).all()

    for recent_run in recent_runs:
        string_run_date = datetime.strftime(recent_run[0].run_date, "%m/%d/%Y")
        recent_runs_data[recent_run[0].run_id] = {"run_id": recent_run[0].run_id,
                                                  "course_name": recent_run[1].course_name,
                                                  "run_date": string_run_date,
                                                  "course_distance": recent_run[1].course_distance,
                                                  "duration": recent_run[0].duration}

    return jsonify(recent_runs_data)


# Line chart of distance over time
@app.route('/user-distance.json')
def user_distance_data():
    """Return the data of User's distance (km)."""

    labels = []
    data = []

    # Get the run date and course distance for all of a user's runs, in chronological order:
    run_date_distance = db.session.query(Run.run_date, Course.course_distance).order_by(Run.run_date).join(Course).all()

    # For each date, distance tuple, add the date to labels array and the distance
    # to the data array, in string format

    for item in run_date_distance:
        date, distance = item
        labels.append(datetime.strftime(date, "%m/%d/%Y"))
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

   # Get the run date, duration, and course distance for all of a user's runs:
    run_date_distance_duration = db.session.query(Run.run_date, Course.course_distance, Run.duration).order_by(Run.run_date).join(Course).all()

    for item in run_date_distance_duration:
        date, distance, duration = item
        labels.append(datetime.strftime(date, "%m/%d/%Y"))
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
