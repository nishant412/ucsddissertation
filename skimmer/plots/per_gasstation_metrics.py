import utils
import numpy as np
import matplotlib.pyplot as plt
import query.query as query

DEFAULT_CDF_TITLE = ''.join(
    ["# of classic/ble devices seen in a 10 minute interval\n",
     "within 50 feet of a gas station."
     ])
SEEN_TWICE_CDF_TITLE = ''.join(
    ["# of seen twice classic/ble devices seen in a 10 minute interval\n",
     "within 50 feet of a gas station."
     ])


def cluster_gs_points(points):
    ''' Creates gas station point clusters '''
    point_clusters = {}
    for point in points:
        gsloc = point[-2]
        dt = utils.round_dt(point[0], 10)
        mac = point[2]
        if gsloc not in point_clusters:
            point_clusters[gsloc] = {}
        if dt not in point_clusters[gsloc]:
            point_clusters[gsloc][dt] = {}
        if mac not in point_clusters[gsloc][dt]:
            point_clusters[gsloc][dt][mac] = []
            point_clusters[gsloc][dt][mac].append(point)

    return point_clusters


def gen_cl_ble_cdfs(bt_point_clusts):
    cl_counts = []
    ble_counts = []
    for loc, timechunks in bt_point_clusts.items():
        for time, macchunks in timechunks.items():
            classic_count = 0
            ble_count = 0
            for mac, pointArr in macchunks.items():
                p = pointArr[-1]
                devtype = p[-3]
                if devtype == 1 or devtype == 3:
                    classic_count += 1
                elif devtype == 2:
                    ble_count += 1
                    cl_counts.append(classic_count)
                    ble_counts.append(ble_count)

    cl_counts_sorted = np.sort(cl_counts)
    ble_counts_sorted = np.sort(ble_counts)
    cl_p = np.linspace(0, 1, len(cl_counts_sorted))
    ble_p = np.linspace(0, 1, len(ble_counts_sorted))

    plt.plot(cl_counts_sorted, cl_p, 'r', label='Classic')
    plt.plot(ble_counts_sorted, ble_p, 'b', label='BLE')
    plt.xlabel('$Number of CL/BLE Devices$')
    plt.ylabel('$p$')
    plt.legend(loc='bottom left')


def gen_cl_ble_cdfs_plot(points):
    points = query.create_pickle(
        'pickle/clusters_for_stations.pickle',
        ['SELECT * FROM (SELECT a.*,b.loc from',
         'near_gasstation a left join fuelsta b',
         'on a.loc <@> b.loc < 0.01::double precision) as foo',
         'WHERE fuelsta_loc IS NOT NULL;'])
    gas_station_point_clusters = cluster_gs_points(points)
    gen_cl_ble_cdfs(gas_station_point_clusters)
    plt.suptitle(SEEN_TWICE_CDF_TITLE)
    # plt.suptitle(DEFAULT_CDF_TITLE)
    plt.show()


def get_points_seen_twice(points):
    seen_twice_points = query.create_pickle(
        'pickle/seen_twice_enqresp.pckle',
        ["SELECT DISTINCT mac FROM enqresp a WHERE EXISTS",
         "(SELECT * FROM enqresp b WHERE",
         "	a.t - b.t > interval '1 hour' OR",
         "	a.t - b.t > interval '1 hour'",
         "	AND b.mac = a.mac);"]
    )
    points = [p for p in points if p.mac in seen_twice_points]
