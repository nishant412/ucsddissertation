import matplotlib.pyplot as plt
import numpy as np

import query.query as query


def main():
    near_gasstation = run_query()
    fuelsta_points = create_fuelsta_points(near_gasstation)
    dev_types_per_station = get_types_per_station(fuelsta_points)

    (cl, ble) = get_nums_cl_ble_seen(dev_types_per_station)
    (uncl, clas) = get_nums_uncl_clas(dev_types_per_station)

    # gen_cdf(
    #     uncl, 'Unclassified Classic Near Station', ble,
    #     'Classified Classic Near Station',
    #     'CDF of Number of Unclassified/Classified Classic Devices' +
    #     ' seen in a typical gasstation.'
    # )

    gen_cdf(cl, 'Classic Near Station', ble, 'BLE Near Station',
            'CDF of Number of CL/BLE Devices seen in a typical gasstation.'
            )


def run_query():
    near_station_macs = {}
    near_gasstation = query.create_pickle_file(
        'pickle/near_gasstation_points.pickle',
        'sql/near_gasstation_points.sql', recreate=True)
    return near_gasstation


def create_fuelsta_points(near_gasstation):
    fuelsta_points = {}
    for point in near_gasstation:
        if point[-1]:
            if point[-1] in fuelsta_points:
                fuelsta_points[point[-1]].append(point)
            else:
                fuelsta_points[point[-1]] = [point]
    return fuelsta_points


def get_types_per_station(fuelsta_points):
    dev_types_per_station = {}
    for fuelsta_loc, pointList in fuelsta_points.items():
        macDict = {}
        for point in pointList:
            if point[2] not in macDict:
                macDict[point[2]] = {
                    'devtype': point[-2],
                    'devclass': (point[-4], point[-3])
                }
        dev_types_per_station[fuelsta_loc] = macDict
    return dev_types_per_station


def get_nums_uncl_clas(dev_types_per_station):
    uncl_seen = []
    clas_seen = []
    for (loc, macDict) in dev_types_per_station.items():
        uncl = 0
        clas = 0
        for devclass in [x['devclass'] for x in macDict.values() if
                         x['devtype'] == 1 or x['devtype'] == 3]:
            if devclass[0] == 31 and devclass[1] == 0:
                uncl += 1
            else:
                clas += 1
        uncl_seen.append(uncl)
        clas_seen.append(clas)
    return (uncl_seen, clas_seen)


def get_nums_cl_ble_seen(dev_types_per_station):
    cl_seen = []
    ble_seen = []
    for (loc, macDict) in dev_types_per_station.items():
        cl = 0
        ble = 0
        for devtype in [x['devtype'] for x in macDict.values()]:
            cl += devtype == 1 or devtype == 3
            ble += devtype == 2
        cl_seen.append(cl)
        ble_seen.append(ble)

    return (cl_seen, ble_seen)


def gen_cdf(cl_seen, fst_label, ble_seen, snd_label, xAxisLabel):
    cl_seen_sorted = np.sort(cl_seen)
    ble_seen_sorted = np.sort(ble_seen)
    cl_p = np.linspace(0, 1, len(cl_seen_sorted))
    ble_p = np.linspace(0, 1, len(ble_seen_sorted))
    plt.plot(cl_seen_sorted, cl_p, 'r', label=fst_label)
    plt.plot(ble_seen_sorted, ble_p, 'b', label=snd_label)
    plt.xlabel(xAxisLabel)
    plt.yticks(np.arange(0, 1.0, 0.1))
    plt.ylabel('$p$')
    plt.legend()

    plt.show()


if __name__ == '__main__':
    main()
