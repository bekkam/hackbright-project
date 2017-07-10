# SafeRun

SafeRun is a fitness tracker and running path generator, made with the nighttime runner in mind. The app uses Google Maps Javascript API to render a map and directions based on user-entered start and end points. Users have the option to view current streetlight outages in the form of markers or a heatmap. In response to such data, they can update their course to avoid unlit areas by dragging the running path polyline; SafeRun will dynamically update the map and directions. After creating a course, users can save it for a future run, or add it to their workout history, along with their run metrics. Users are able to easily discern their run progress over time by navigating to the profile page, which renders workout data, including pace and distance over time, in chart form.

## Technologies Used

- **Frontend**: Javascript (AJAX, JQuery), Bootstrap, HTML, CSS
- **Backend**: Python, Jinja2, Flask, SQLAlchemy, Geocoder, PolylineCodec
- **Database**: PostgreSQL
- **Testing**: Unittest, Doctest (Python), Jasmine (Javascript)
- **APIs**: Google Maps Javascript API, Chart.js, Socrata Open Data API (SODA), SnazzyMaps

## Features
*Creating a Course, Customizing Route*


![create](https://raw.githubusercontent.com/bekkam/safe-run/master/docs/static/createrun.gif "Create")


*Saving a Course with Run Metrics*


![save](https://raw.githubusercontent.com/bekkam/safe-run/master/docs/static/saverun.gif "Save")


*Viewing Live Outage Data*


![markers](https://raw.githubusercontent.com/bekkam/safe-run/master/docs/static/markers.gif "Markers")


*Profile Page*


![profile](https://raw.githubusercontent.com/bekkam/safe-run/master/docs/static/profile.png "Profile")


*Course History*


![allcourses](https://raw.githubusercontent.com/bekkam/safe-run/master/docs/static/allcourses.png "All Courses")


*Run History*


![allruns](https://raw.githubusercontent.com/bekkam/safe-run/master/docs/static/allruns.png "All Runs")