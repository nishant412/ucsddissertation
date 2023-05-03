#!/usr/bin/python
import sys
import json
from tabulate import tabulate


def js_r(filename):
   with open(filename) as f_in:
       return(json.load(f_in))

if __name__ == "__main__":
    module_state_data = js_r(sys.argv[1])
    print('Number of devices in total for each state.')
    table = [['','None','Module A', 'Module B', 'Module C']]
    for state,station_list in module_state_data.items():
        data = [state,0,0,0,0]
        for station in station_list:
            for dev in station:
                if dev[:8] == '00:06:66':
            	    data[2] += 1
                elif dev[:5] == '20:18':
                    data[3] += 1
                elif dev[:5] == '20:17':
                    data[4] += 1
                else:
                    data[1] += 1
        table.append(data)
    print(tabulate(table, tablefmt="latex"))
    print('Number of stations containing device for each state.')
    table = [['','Module A', 'Module B', 'Module C']]
    for state,station_list in module_state_data.items():
        data = [state,0,0,0]
        for station in station_list:
            modA = 0
            modB = 0
            modC = 0
            for dev in station:
                if dev[:8] == '00:06:66':
                    modA = 1
                if dev[:5] == '20:18':
                    modB = 1
                if dev[:5] == '20:17':
                    modC = 1
            data[1] += modA
            data[2] += modB
            data[3] += modC
        table.append(data)
    print(tabulate(table, tablefmt="latex"))
    
