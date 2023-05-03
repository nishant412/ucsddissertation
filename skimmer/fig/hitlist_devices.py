#!/usr/bin/env python

# Note: Assumes the input is ascending sorted

from sys import stdin

macint_prev = 0

for line in stdin:
    sp = line.split()
    mac_bytes = sp[0].split(':')

    macint =                         \
      (int(mac_bytes[5],16) << 0)  + \
      (int(mac_bytes[4],16) << 8)  + \
      (int(mac_bytes[3],16) << 16) + \
      (int(mac_bytes[2],16) << 24) + \
      (int(mac_bytes[1],16) << 32) + \
      (int(mac_bytes[0],16) << 40)

    if ((macint_prev >> 24) & 0xFFFFFF == (macint >> 24) & 0xFFFFFF):
        print macint - macint_prev

    macint_prev = macint
