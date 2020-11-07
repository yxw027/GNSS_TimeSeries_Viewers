# Python functions to generate a list of GNSS station names/locations that are
# within a certain radius of that point or a given box.
# num_years is the minimum duration of the time series
# max_sigma is the formal uncertainty on the velocity in mm

import numpy as np
import sys
import haversine
import read_kml
import gps_io_functions
import gps_vel_functions
import matplotlib.path as mpltPath


# DRIVER 1: STATIONS WITHIN RADIUS
def get_stations_within_radius(data_config_file, center, radius, coord_box=(-126, -110, 30.0, 49), network='pbo',
                               num_years=3.0, max_sigma=2):
    # default coord box is western US
    myParams = gps_io_functions.read_config_file(data_config_file);
    myVelfield = inputs_velfield(myParams, network, num_years, max_sigma, coord_box);
    close_stations, lon, lat, rad_distance = compute_circle(myVelfield, center, radius);
    return close_stations, lon, lat, rad_distance;


# DRIVER 2: STATIONS WITHIN BOX
def get_stations_within_box(data_config_file, coord_box, network='pbo', num_years=3.0, max_sigma=2):
    myParams = gps_io_functions.read_config_file(data_config_file);
    myVelfield = inputs_velfield(myParams, network, num_years, max_sigma, coord_box);
    within_stations, lon, lat = compute_box(myVelfield, coord_box);
    return within_stations, lon, lat;


# DRIVER 3: STATIONS WITHIN A USER-DEFINED KML BORDER
def get_stations_within_polygon(data_config_file, polygon_file, coord_box=(-126, -110, 30.0, 49), network='pbo',
                                num_years=3.0, max_sigma=2):
    myParams = gps_io_functions.read_config_file(data_config_file);
    [polygon_lon, polygon_lat] = read_kml.read_simple_kml(polygon_file);
    myVelfield = inputs_velfield(myParams, network, num_years, max_sigma, coord_box);
    within_stations, lon, lat = compute_within_polygon(myVelfield, polygon_lon, polygon_lat);
    return within_stations, lon, lat;


# ------------ INPUTS ------------------ #
def inputs_velfield(myParams, network, num_years, max_sigma, coord_box):
    # Purpose: generate input velocity field.
    print("Searching for GNSS stations in the %s network " % network);
    if network == 'pbo' or network == 'cwu' or network == 'nmt':
        [myVelfield] = gps_io_functions.read_pbo_vel_file(myParams.pbo_velocities);
    elif network == 'unr':
        [myVelfield] = gps_io_functions.read_unr_vel_file(myParams.unr_velocities, myParams.unr_coords_file);
    elif network == 'usgs':
        [myVelfield] = gps_io_functions.read_usgs_velfile(myParams.usgs_vel_dir+'/ITRF_Pacific_Northwest_vels.txt', myParams.usgs_cache_file);
    else:
        print("ERROR: Network %s not recognized (try pbo/cwu/nmt/unr/usgs)" % network);
        sys.exit(0);

    [myVelfield] = gps_vel_functions.clean_velfield(myVelfield, num_years=num_years, max_horiz_sigma=max_sigma,
                                                    max_vert_sigma=max_sigma * 3, coord_box=coord_box);
    [myVelfield] = gps_vel_functions.remove_duplicates(myVelfield);
    return myVelfield;


# ----------- CIRCLE FUNCTIONS ---------------- # 
def compute_circle(myVelfield, center, radius):
    close_stations = [];
    rad_distance = [];
    lon, lat = [], [];
    for i in range(len(myVelfield.name)):
        mydist = haversine.distance([center[1], center[0]], [myVelfield.nlat[i], myVelfield.elon[i]])
        if mydist <= radius:
            rad_distance.append(mydist);
            lon.append(myVelfield.elon[i]);
            lat.append(myVelfield.nlat[i]);
            close_stations.append(myVelfield.name[i]);
    print("Returning %d stations within %.3f km of %.4f, %.4f" % (len(close_stations), radius, center[0], center[1]));
    return close_stations, lon, lat, rad_distance;


# ----------- BOX FUNCTIONS ---------------- # 

def compute_box(myVelfield, coord_box):
    close_stations, lon, lat = [], [], [];
    for i in range(len(myVelfield.name)):
        if coord_box[0] <= myVelfield.elon[i] <= coord_box[1]:
            if coord_box[2] <= myVelfield.nlat[i] <= coord_box[3]:
                close_stations.append(myVelfield.name[i]);
                lon.append(myVelfield.elon[i]);
                lat.append(myVelfield.nlat[i]);
    print("Returning %d stations within box" % (len(close_stations)));
    return close_stations, lon, lat;


# ----------- POLYGON FUNCTIONS ---------------- # 

def compute_within_polygon(myVelfield, polygon_lon, polygon_lat):
    # If within the polygon:
    lon, lat = [], [];
    polygon = np.row_stack((np.array(polygon_lon), np.array(polygon_lat))).T;
    points = np.row_stack((np.array(myVelfield.elon), myVelfield.nlat)).T;
    path = mpltPath.Path(polygon);
    inside2 = path.contains_points(points);
    within_stations = [i for (i, v) in zip(myVelfield.name, inside2) if v];
    print("Returning %d stations within the given polygon" % (len(within_stations)));
    return within_stations, lon, lat;


if __name__ == "__main__":
    center = [-124, 40];
    radius = 80;
    data_config_file = "/Users/kmaterna/Documents/B_Research/Mendocino_Geodesy/GPS_POS_DATA/config.txt"
    close_stations, lons, lats, rad_distance = get_stations_within_radius(data_config_file, center, radius, network='usgs');
    print(close_stations);
