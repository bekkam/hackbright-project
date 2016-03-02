"""Utility file to seed streetlight outage database with SF OpenData SF311 cases"""

import re


def get_outage_latlngs():
    """Get streetlight outage lat longs from data file."""

    data_file = open("streetlight-data.csv")
    for row in data_file:
        row = row.rstrip()

        point = re.search(r"(\d)*\.(\d)*\,\s\-(\d)*\.(\d)*", row)
        if point:
            latlng = point.group(0)
            # print latlng
            # print type(latlng)
            pairs = latlng.split(',')
            print "pairs is ", pairs
            lat = pairs[0]
            lng = pairs[1]
            # print "lat:", lat
            # print "lng:", lng

            # TODO: add each pair to db, after confirming format is appropriate for google markers
    #         streetlight = Streetlight(lat=lat, lng=lng)
    #         db.session.add(streetlight)

    # db.session.commit()
