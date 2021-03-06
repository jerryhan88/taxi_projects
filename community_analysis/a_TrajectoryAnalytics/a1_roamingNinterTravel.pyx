import __init__
#
'''

'''
#
from community_analysis import FRI, SAT, SUN
from community_analysis import AM10, PM8
from community_analysis import taxi_home
from community_analysis import dpaths, prefixs
from community_analysis import FREE
from community_analysis import MIN20
#
from taxi_common import ss_drivers_dpath, ss_drivers_prefix
from taxi_common.sg_grid_zone import get_sg_grid_xy_points
from taxi_common.file_handling_functions import load_pickle_file, check_dir_create, check_path_exist
from taxi_common.log_handling_functions import get_logger
#
from bisect import bisect
import csv, datetime
#
logger = get_logger()

of_dpath = dpaths['roamingNinterTravel']
of_prefixs = prefixs['roamingNinterTravel']

try:
    check_dir_create(of_dpath)
except OSError:
    pass


def process_month(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        yy, mm = yymm[:2], yymm[2:]
        trip_normal_fpath = '%s/20%s/%s/trips/trips-%s-normal.csv' % (taxi_home, yy, mm, yymm)
        trip_ext_fpath = '%s/20%s/%s/trips/trips-%s-normal-ext.csv' % (taxi_home, yy, mm, yymm)
        log_fpath = '%s/20%s/%s/logs/logs-%s-normal.csv' % (taxi_home, yy, mm, yymm)
        if not check_path_exist(trip_normal_fpath):
            logger.info('The file X exists; %s' % yymm)
            return None
        ss_drivers_fpath = '%s/%s%s.pkl' % (ss_drivers_dpath, ss_drivers_prefix, yymm)
        if not check_path_exist(ss_drivers_fpath):
            logger.info('The file X exists; %s' % ss_drivers_fpath)
            return None
        ss_drivers = load_pickle_file(ss_drivers_fpath)
        x_points, y_points = get_sg_grid_xy_points()
        #
        ofpath = '%s/%s%s.csv' % (of_dpath, of_prefixs, yymm)
        if check_path_exist(ofpath):
            logger.info('The file had already been processed; %s' % yymm)
            return None
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['did',
                             'hour', 'zi', 'zj',
                             'time', 'day', 'month',
                             'start-long', 'start-lat',
                             'distance', 'duration', 'fare',
                             'roamingTime', 'interTravelTime'])
        with open(trip_normal_fpath, 'rb') as tripFileN:
            tripReaderN = csv.reader(tripFileN)
            tripHeaderN = tripReaderN.next()
            # {'trip-id': 0, 'job-id': 1, 'start-time': 2, 'end-time': 3,
            #  'start-long': 4, 'start-lat': 5, 'end-long': 6, 'end-lat': 7,
            #  'vehicle-id': 8, 'distance': 9, 'fare': 10, 'duration': 11,
            #  'start-dow': 12, 'start-day': 13, 'start-hour': 14, 'start-minute': 15,
            #  'end-dow': 16, 'end-day': 17, 'end-hour': 18, 'end-minute': 19}
            hidN = {h: i for i, h in enumerate(tripHeaderN)}
            with open(trip_ext_fpath, 'rb') as tripFileE:
                tripReaderE = csv.reader(tripFileE)
                tripHeaderE = tripReaderE.next()
                #
                # {'start-zone': 0, 'end-zone': 1, 'start-postal': 2, 'driver-id': 4, 'end-postal': 3}
                #
                hidE = {h: i for i, h in enumerate(tripHeaderE)}
                with open(log_fpath, 'rb') as logFile:
                    logReader = csv.reader(logFile)
                    logHeader = logReader.next()
                    hidL = {h: i for i, h in enumerate(logHeader)}
                    handling_day = 0
                    drivers = {}
                    for rowN in tripReaderN:
                        rowE = tripReaderE.next()
                        didT = int(rowE[hidE['driver-id']])
                        if didT not in ss_drivers:
                            continue
                        tripTime = eval(rowN[hidN['start-time']])
                        cur_dtT = datetime.datetime.fromtimestamp(tripTime)
                        if handling_day != cur_dtT.day:
                            handling_day = cur_dtT.day
                            logger.info('Processing %s %dth day' % (yymm, cur_dtT.day))
                        if cur_dtT.weekday() in [FRI, SAT, SUN]:
                            continue
                        if cur_dtT.hour < AM10:
                            continue
                        if PM8 <= cur_dtT.hour:
                            continue
                        while True:
                            rowL = logReader.next()
                            logTime = eval(rowL[hidL['time']])
                            didL = int(rowL[hidL['driver-id']])
                            if didL not in ss_drivers:
                                continue
                            t = eval(rowL[hidL['time']])
                            cur_dtL = datetime.datetime.fromtimestamp(t)
                            if cur_dtL.weekday() in [FRI, SAT, SUN]:
                                continue
                            if cur_dtL.hour < AM10:
                                continue
                            if PM8 <= cur_dtL.hour:
                                continue
                            longitude, latitude = eval(rowL[hidL['longitude']]), eval(rowL[hidL['latitude']])
                            zi, zj = bisect(x_points, longitude) - 1, bisect(y_points, latitude) - 1
                            if zi < 0 or zj < 0:
                                continue
                            t, s = eval(rowL[hidL['time']]), eval(rowL[hidL['state']])
                            z = (zi, zj)
                            cur_dt = datetime.datetime.fromtimestamp(t)
                            if handling_day != cur_dt.day:
                                handling_day = cur_dt.day
                                logger.info('Processing %s %dth day' % (yymm, cur_dt.day))
                            if not drivers.has_key(didL):
                                drivers[didL] = driver(didL, t, z, s)
                            else:
                                drivers[didL].update(t, z, s)
                            if tripTime <= logTime:
                                break
                        s_long, s_lat = eval(rowN[hidN['start-long']]), eval(rowN[hidN['start-lat']])
                        zi, zj = bisect(x_points, s_long) - 1, bisect(y_points, s_lat) - 1
                        if zi < 0 or zj < 0:
                            continue
                        if not drivers.has_key(didT):
                            continue
                        if drivers[didT].firstFreeStateTime == -1:
                            continue
                        roamingTime = tripTime - drivers[didT].zoneEnteredTime
                        interTravelTime = tripTime - drivers[didT].firstFreeStateTime
                        with open(ofpath, 'a') as w_csvfile:
                            writer = csv.writer(w_csvfile, lineterminator='\n')
                            writer.writerow([didT,
                                             cur_dtT.hour, zi, zj,
                                             tripTime, cur_dtT.day, cur_dtT.month,
                                             s_long, s_lat,
                                             rowN[hidN['distance']], rowN[hidN['duration']], rowN[hidN['fare']],
                                             roamingTime, interTravelTime])
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


class driver(object):
    def __init__(self, did, cl_time, cl_zone, cl_state):
        self.did = did
        self.pl_time, self.pl_zone, self.pl_state = cl_time, cl_zone, cl_state
        if self.pl_state == FREE:
            self.firstFreeStateTime = self.pl_time
        else:
            self.firstFreeStateTime = -1
        self.zoneEnteredTime = self.pl_time

    def update(self, cl_time, cl_zone, cl_state):
        if cl_state != FREE:
            self.firstFreeStateTime = -1
        else:
            # Handle previous log's state is not FREE
            if self.firstFreeStateTime == -1:
                self.firstFreeStateTime = cl_time
            # Handle driver's break
            if self.pl_state == FREE and (cl_time - self.pl_time) > MIN20:
                self.firstFreeStateTime = cl_time
        #
        if self.pl_zone != cl_zone:
            self.zoneEnteredTime = cl_time
        self.pl_time, self.pl_zone, self.pl_state = cl_time, cl_zone, cl_state


if __name__ == '__main__':
    run()
