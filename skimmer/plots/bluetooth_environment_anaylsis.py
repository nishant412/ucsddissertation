import utils
import pickle
import query.query as query
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import time


class Observer:
    def __init__(self, name):
        self.name = name
        (pts_not_by_station, pts_by_station) = utils.get_points(name)

        print("Creating not near gas station snapshots, for obs %s" % name)
        self.envir_snapshots_not_by_station = []
        for (t, mac_clusters) in pts_not_by_station.items():
            self.envir_snapshots_not_by_station.append(
                BluetoothEnvironment(t, mac_clusters))

        print("Creating near gas station snapshots, for obs %s" % name)
        self.envir_snapshots_by_station = []
        for (t, mac_clusters) in pts_by_station.items():
            self.envir_snapshots_by_station.append(
                BluetoothEnvironment(t, mac_clusters))


class BluetoothEnvironment:
    def __init__(self, time, mac_clusters):
        self.time = time
        self.mac_clusters = mac_clusters
        self.classics = 0
        self.bles = 0
        for (mac, pointList) in mac_clusters.items():
            devtype = pointList[-1][-1]
            if devtype == 1 or devtype == 3:
                self.classics += 1
            elif devtype == 2:
                self.bles += 1


if __name__ == '__main__':
    observer_list = []
    obsmacs = query.create_pickle(
        'pickle/obsmacs.pickle',
        ['select mac from observer;']
    )

    obs_list_pickle = Path('pickle/obs_list.pickle')

    if not obs_list_pickle.is_file():
        for obsmac in obsmacs:
            print('Adding obs %s to list of observers' % obsmac)
            start = time.time()
            observer_list.append(Observer(obsmac))
            print('That took %d seconds' % (start - time.time()))
        with obs_list_pickle.open('wb') as out:
            pickle.dump(observer_list, out)
    else:
        with obs_list_pickle.open('rb') as inp:
            observer_list = pickle.load(inp)

    classic_devs_seen_not_near = []
    ble_devs_seen_not_near = []
    classic_devs_seen_near = []
    ble_devs_seen_near = []

    for observer in observer_list:
        for envir in observer.envir_snapshots_not_by_station:
            if envir.classics < 100:
                classic_devs_seen_not_near.append(envir.classics)
            if envir.bles < 100:
                ble_devs_seen_not_near.append(envir.bles)
        for envir in observer.envir_snapshots_by_station:
            if envir.classics < 100:
                classic_devs_seen_near.append(envir.classics)
            if envir.bles < 100:
                ble_devs_seen_near.append(envir.bles)

    cl_near_sorted = np.sort(classic_devs_seen_near)
    ble_near_sorted = np.sort(ble_devs_seen_near)
    cl_not_near_sorted = np.sort(classic_devs_seen_not_near)
    ble_not_near_sorted = np.sort(ble_devs_seen_not_near)

    cl_p_near = np.linspace(0, 1, len(cl_near_sorted))
    ble_p_near = np.linspace(0, 1, len(ble_near_sorted))
    cl_p_not_near = np.linspace(0, 1, len(cl_not_near_sorted))
    ble_p_not_near = np.linspace(0, 1, len(ble_not_near_sorted))
    plt.plot(cl_near_sorted, cl_p_near, 'r', label='Classic Near Station')
    plt.plot(ble_near_sorted, ble_p_near, 'b', label='BLE Near Station')
    plt.plot(cl_not_near_sorted,cl_p_not_near,  'g',
             label='Classic Not Near Station')
    plt.plot(ble_not_near_sorted, ble_p_not_near, 'k',
             label='BLE Not Near Station')
    plt.xlabel(' '.join([
        'CDF of Number of CL/BLE Devices seen in a typical 10',
        'minute interval.'])
    )
    plt.yticks(np.arange(0, 1.0, 0.1))
    plt.ylabel('$p$')
    plt.legend(loc='bottom left')

    plt.show()
