from __future__ import division

import platform, sys

# Check environments and set a prefix for finding files and libraries
plf = platform.platform()
if plf.startswith('Linux'):
    # This would be the server
    prefix = '/home/ckhan/taxi_data'
    py_vinfo = sys.version_info
    if py_vinfo.major == 2 and py_vinfo.minor == 7:
        sys.path.append('/home/ckhan/local/lib/python2.7/site-packages')
        sys.path.append('/home/ckhan/local/lib64/python2.7/site-packages')
    else:
        print 'This python is not 2.7 version'
        assert False
    #
elif plf.startswith('Darwin'):
    # This is my Macbook Pro
    prefix = '/Users/JerryHan88/taxi_data'
else:
    # TODO
#     assert False, 'Windows?'
    prefix = 'C:\Users/ckhan.2015/taxi_data'
assert prefix
#
# original data path in the server
#
taxi_home = '/home/taxi'
#
# path for polygons' information
#
ap_poly_info = '../src/airport_polygons'
ns_poly_info = '../src/night_safari_polygon'
#
# trips(_merged)
#
merged_trip_dir = prefix + '/trips_merged'
trips_dir, trip_prefix = prefix + '/trips', 'whole-trip-'
airport_trips_dir, ap_trip_prefix = trips_dir + '/airport_trips', 'airport-trip-'
nightsafari_trips_dir, ns_trip_prefix = trips_dir + '/nightsafari_trips', 'nightsafari-trip-'
#
# logs
#
logs_dir = prefix + '/logs'
log_last_day_dir = logs_dir + '/logs_last_day'
#
# shifts
#
shifts_dir, shifts_prefix = prefix + '/shifts', 'shift-hour-state-'
shift_pro_dur_dir, shift_pro_dur_prefix = shifts_dir + '/shift_pro_dur', 'shift-pro-dur-'
vehicle_drivers_dir, vehicle_drivers_prefix = shifts_dir + '/vehicle_drivers', 'vehicle-drivers-'
#
# hourly_productivities
#
hourly_productivities_dir = prefix + '/hourly_productivities'
general_dur_fare_dir, general_dur_fare_prefix = hourly_productivities_dir + '/general_dur_fare', 'gdf-'
ap_dur_fare_q_time_dir, ap_dur_fare_q_time_prefix = hourly_productivities_dir + '/ap_dur_fare_q_time', 'adfqt-'
ns_dur_fare_q_time_dir, ns_dur_fare_q_time_prefix = hourly_productivities_dir + '/ns_dur_fare_q_time', 'ndfqt-'
#
# economic_profits_dir
#
economic_profits_dir = prefix + '/economic_profits'
ap_trips_economic_profits_dir = economic_profits_dir + '/ap_trips_economic_profits'
ap_trips_ecoprof_prefix = 'ap-trip-ecoprof-'
ns_trips_economic_profits_dir = economic_profits_dir + '/ns_trips_economic_profits'
ns_trips_ecoprof_prefix = 'ns-trip-ecoprof-'
#
# full time drivers data
#
full_time_drivers_dir = prefix + '/full_time_drivers'
ftd_shift_dir = full_time_drivers_dir + '/full_time_drivers_shift'
ftd_shift_prefix, full_time_drivers_prefix = 'full-time-drivers-shift-', 'full-time-drivers-'
ftd_trips_dir, ftd_trips_prefix = full_time_drivers_dir + '/full_time_drivers_trips', 'full-time-drivers-trips-'
ftd_general_stat_dir, ftd_general_stat_prefix = \
             full_time_drivers_dir + '/full_time_drivers_general_stat', 'full-time-drivers-general-stat-'
ftd_prev_in_ap_stat_dir, ftd_prev_in_ap_stat_prefix = \
             full_time_drivers_dir + '/full_time_drivers_prev_in_ap_stat', 'full-time-drivers-prev-in-ap-stat-'
ftd_prev_out_ap_stat_dir, ftd_prev_out_ap_stat_prefix = \
             full_time_drivers_dir + '/full_time_drivers_prev_out_ap_stat', 'full-time-drivers-prev-out-ap-stat-'
ftd_prev_in_ns_stat_dir, ftd_prev_in_ns_stat_prefix = \
             full_time_drivers_dir + '/full_time_drivers_prev_in_ns_stat', 'full-time-drivers-prev-in-ns-stat-'
ftd_prev_out_ns_stat_dir, ftd_prev_out_ns_stat_prefix = \
             full_time_drivers_dir + '/full_time_drivers_prev_out_ns_stat', 'full-time-drivers-prev-out-ns-stat-'
#
# summary
#
summary_dir = prefix + '/summary'
# overall
ap_tm_num_dur_fare_fn = summary_dir + '/ap-tm-num-dur-fare.csv' 
ns_tm_num_dur_fare_fn = summary_dir + '/ns-tm-num-dur-fare.csv' 
# aggregated
hourly_productivities = summary_dir + '/hourly-productivities.csv'
zero_duration_time_slots = summary_dir + '/zero-duration-time-slots.pkl'
Y09_ap_trips = summary_dir + '/Y09-ap-trips.csv'
Y10_ap_trips = summary_dir + '/Y10-ap-trips.csv'
Y09_ns_trips = summary_dir + '/Y09-ns-trips.csv'
Y10_ns_trips = summary_dir + '/Y10-ns-trips.csv'
driver_monthly_fare_gt = summary_dir + '/driver-monthly-fare-gt.pkl'
driver_monthly_fare_at = summary_dir + '/driver-monthly-fare-at.pkl'
driver_monthly_fare_nt = summary_dir + '/driver-monthly-fare-nt.pkl'
# individual
Y09_ftd_general_stat = summary_dir + '/Y09-ftd-general-stat.csv'
Y10_ftd_general_stat = summary_dir + '/Y10-ftd-general-stat.csv'
Y09_ftd_prev_in_ap_stat = summary_dir + '/Y09-ftd-prev-in-ap-stat.csv'
Y10_ftd_prev_in_ap_stat = summary_dir + '/Y10-ftd-prev-in-ap-stat.csv'
Y09_ftd_prev_in_ns_stat = summary_dir + '/Y09-ftd-prev-in-ns-stat.csv'
Y10_ftd_prev_in_ns_stat = summary_dir + '/Y10-ftd-prev-in-ns-stat.csv'
Y09_ftd_prev_out_ap_stat = summary_dir + '/Y09-ftd-prev-out-ap-stat.csv'
Y10_ftd_prev_out_ap_stat = summary_dir + '/Y10-ftd-prev-out-ap-stat.csv'
Y09_ftd_prev_out_ns_stat = summary_dir + '/Y09-ftd-prev-out-ns-stat.csv'
Y10_ftd_prev_out_ns_stat = summary_dir + '/Y10-ftd-prev-out-ns-stat.csv'
ftd_general_prod_mb = summary_dir + '/ftd-general-prod-months-based.pkl'
ftd_ap_prod_eco_prof_mb = summary_dir + '/ftd-ap-prod-eco-prof-months-based.pkl'
ftd_ns_prod_eco_prof_mb =summary_dir + '/ftd-ns-prod-eco-prof-months-based.pkl'
ftd_general_prod_db_for_ap = summary_dir + '/ftd-general-prod-drivers-based-for-ap.pkl'
ftd_general_prod_db_for_ns = summary_dir + '/ftd-general-prod-drivers-based-for-ns.pkl'
ftd_ap_prod_eco_prof_db = summary_dir + '/ftd-ap-prod-eco-prof-drivers-based.pkl'
ftd_ns_prod_eco_prof_db = summary_dir + '/ftd-ns-prod-eco-prof-drivers-based.pkl'
#
# path for chart saving
#
charts_dir = prefix +'/charts'
row_data_a_a1 = charts_dir + '/fare_duration_per_trip.txt'
row_data_a_a2 = charts_dir + '/statistics_timeslots.txt'
row_data_b_a1 = charts_dir + '/drivers_monthly_fares.txt'
row_data_b_a3 = charts_dir + '/queue_time.txt'
#
# path for table saving
#
tables_dir = prefix +'/tables'
ftd_overall_analysis = tables_dir + '/ftd-overall-analysis.txt'
ftd_group_analysis = tables_dir + '/ftd-group-analysis.txt' 
#
# trip modes
#
DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP = range(4)
DInNS_PInNS, DInNS_POutNS, DOutNS_PInNS, DOutNS_POutNS = range(4)
#
# for checking logs' location
#
IN_AP, OUT_AP = 'O', 'X'
IN_NS, OUT_NS = 'O', 'X'
#
# units
#
SEC3600, SEC60 = 60 * 60, 60
CENT = 100
#
# Labeling for zero duration
#
GENERAL, AIRPORT, NIGHTSAFARI = 'G', 'A', 'N'
#
# etc.
#
DAY_OF_WEEK = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
TIME_SLOTS = range(24)
Q_LIMIT_MIN = 0
TIME_ALARM = SEC60 * 5


