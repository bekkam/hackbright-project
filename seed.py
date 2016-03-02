import re

"""Utility file to seed streetlight outage database with SF OpenData SF311 cases"""


def d():
    """Load streetlight outage lat longs into database."""

    data_file = open("test-data.txt")
    for row in data_file:
        # print line.split(',')[-1]
        row = row.rstrip()
        # latlng = row.split(',')[14:15]
        # print latlng

        # print re.search(r"org", row)

        # prints org :)
        # point = re.search(r"org", row)
        # if point:
        #     print point.group(0)

        point = re.search(r"\((\d)*\.(\d)*\,\s(\d*)", row)
        # print point
        if point:
            print point.group(0)
            print point.group(1)
        # print "line is", row
        # items = line.split(',').rstrip()
        # print "items in line are", items


        # print items[-2]
        # print item[0]
        # for i in item:
        #     print i
