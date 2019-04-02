"""
Driver for making maps of GPS accelerations before/after a certain time. 
In this case, EQcoords is just the center of the map. 
"""

import Mend_map_accel

EQ0="20060101"  # earthquake was 20050615. We want to skip six months
EQ0_end="20100110"  # the earthquake time
EQ1="20100703"  # earthquake was 20100110. We want to skip six months. 
EQ2="20140310"
EQ3="20161208"
EQ4="20180915"


Center_Coords=[-124.0, 38.5]; # Western US everything
filter_type='lssq'; # OPTIONS: lssq, notch, stl, grace, gldas, nldas, shasta, oroville, none. 
size='huge';  # OPTIONS: small, medium, huge
network='unr';  # choices: unr, pbo, cwu, nmt, nldas, gldas, noah025
refname='ITRF'; # choices: NA, ITRF
# stations=["P349","ORVB"];  # In case you only want to do a few stations manually. 

# LEAST SQUARES
Mend_map_accel.driver(Center_Coords, size, network, refname, filter_type, [EQ1,EQ2],[EQ2,EQ3], "2014"); # 
Mend_map_accel.driver(Center_Coords, size, network, refname, filter_type, [EQ2,EQ3],[EQ3,EQ4], "2016"); # 
Mend_map_accel.driver(Center_Coords, size, network, refname, filter_type, [EQ0,EQ0_end],[EQ1,EQ2], "2010"); # 
Mend_map_accel.driver(Center_Coords, size, network, refname, filter_type, [EQ1,EQ2],[EQ3,EQ4], "2010_2016");

# Mend_map_accel.driver(Center_Coords, size, network, refname, ["20110824","20140824"],["20140824","20170824"], "NAPA");


