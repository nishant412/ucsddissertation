set term pdf size 5in,3in font "Helvetica,18"
set output 'hitlist_devices.pdf'

set key center at 2**16,0.15

set ylabel "CDF"
set ytics 0.1

set grid x lw 2 lt -1 dt 2

set label "1 Byte" center at 16,1.08
set label "2 Bytes" center at (2**12),1.08
set label "3 Bytes" center at (2**20),1.08

set tmargin 1.5

set xlabel "Difference in MAC address space"
set logscale x 2
set format x "2^{%L}"
set mxtics 8
set xtics scale 2 256 
set xrange [2**0:2**24]

p '<grep    "Skimmer" hitlist_devices-sorted | ./hitlist_devices.py | ./cdf_count.py' u 1:2 w li lw 4  lc rgb '#FF0000' ti 'Skimmers',\
  '<grep -v "Skimmer" hitlist_devices-sorted | ./hitlist_devices.py | ./cdf_count.py' u 1:2 w li lw 4 lc rgb '#3093DB' ti 'Other HC or RN'
