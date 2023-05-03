import pickle
import time
import datetime
from pathlib import Path
import query.query as query


def round_dt(tm, minutes):
    ''' Rounds a datetime to a minute mark '''
    discard = datetime.timedelta(minutes=tm.minute % minutes,
                                 seconds=tm.second,
                                 microseconds=tm.microsecond)
    tm -= discard
    if discard >= datetime.timedelta(minutes=(minutes / 2)):
        tm += datetime.timedelta(minutes=minutes)

    return tm


def get_points(obsmac):
    print("Creating enqresp for obs %s" % obsmac)
    enqresp_points = query.create_pickle(
        'pickle/enqresp_%s.pickle' % obsmac,
        ["SELECT * FROM enqresp where obsmac = '%s';" % obsmac]
    )
    print("Creating near_gasstation for obs %s" % obsmac)
    near_station_macs = {}
    near_gasstation = query.create_pickle(
        'pickle/near_gasstation_macs.pickle',
        ['SELECT mac FROM (SELECT a.*,b.loc from',
         'near_gasstation a left join fuelsta b',
         'on a.loc <@> b.loc < 0.01::double precision) as foo',
         'WHERE fuelsta_loc IS NOT NULL;']
    )
    for mac in near_gasstation:
        near_station_macs[mac[0]] = True

    print("Creating time, mac clusters for obs %s" % obsmac)
    not_near_station_clusters = {}
    near_station_clusters = {}

    for i, point in enumerate(enqresp_points):
        dt = round_dt(point[0], 10)
        mac = point[2]
        if mac not in near_station_macs:
            if dt not in not_near_station_clusters:
                not_near_station_clusters[dt] = {}
                not_near_station_clusters[dt][mac] = [point]
            elif mac not in not_near_station_clusters[dt]:
                not_near_station_clusters[dt][mac] = [point]
            else:
                not_near_station_clusters[dt][mac].append(point)
        else:
            if dt not in near_station_clusters:
                near_station_clusters[dt] = {}
                near_station_clusters[dt][mac] = [point]
            elif mac not in near_station_clusters[dt]:
                near_station_clusters[dt][mac] = [point]
            else:
                near_station_clusters[dt][mac].append(point)
    print("Creating time, mac clusters for obs %s" % obsmac)
    return (not_near_station_clusters, near_station_clusters)


def read_pickle(file_name):
    with open(file_name) as pickle_read:
        res = pickle.load(pickle_read)
        return res
