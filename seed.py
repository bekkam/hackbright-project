"""Utility file to seed streetlight outage database with SF OpenData SF311 cases"""

import re

from model import Outage, connect_to_db, db
from server import app


def get_outages():
    """Get streetlight outage lat longs from data file."""

    data_file = open("streetlight-data.csv")
    for row in data_file:
        row = row.rstrip()

        point = re.search(r"(\d)*\.(\d)*\,\s\-(\d)*\.(\d)*", row)
        if point:
            latlng = point.group(0)
            pairs = latlng.split(',')
            outage_lat = pairs[0]
            outage_long = pairs[1].lstrip()

            outage = Outage(outage_lat=outage_lat, outage_long=outage_long)
            db.session.add(outage)

    print "Finished seeding database"
    db.session.commit()


# #####################################3
if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()

    get_outages()
