import __init__
#
from __init__ import taxi_home, grid_info_fn
from __init__ import ZONE_UNIT_KM
from __init__ import FREE, POB
from _classes import cd_zone
#
from taxi_common.file_handling_functions import check_path_exist, save_pickle_file, load_pickle_file
#
from bisect import bisect
import csv, datetime, time
from dateutil.relativedelta import relativedelta


def run(time_from, time_to):
    if not check_path_exist(grid_info_fn):
        from taxi_common.split_into_zones import run as run_split_into_zones
        x_points, y_points, zones = run_split_into_zones(ZONE_UNIT_KM, cd_zone)
        save_pickle_file(grid_info_fn, [x_points, y_points, zones])
    else:
        x_points, y_points, zones = load_pickle_file(grid_info_fn)
    #
    tf_ts = time.mktime(datetime.datetime(*time_from).timetuple())
    tt_ts = time.mktime(datetime.datetime(*time_to).timetuple())
    #
    csv_files = get_csv_files(time_from, time_to)
    for fn in csv_files:
        with open(fn, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            # {'longitude': 3, 'state': 6, 'vehicle-id': 1, 'time': 0, 'latitude': 4, 'speed': 5, 'driver-id': 2}
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                did = row[hid['driver-id']]
                if did == '-1':
                    continue
                t = eval(row[hid['time']])







    drivers_states = {}
    processed_log_fn = get_processed_log_fn(time_from, time_to)
    with open(processed_log_fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        writer.writerow(['time', 'i', 'j', 'did'])
    #
    for fn in csv_files:
        with open(fn, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            # {'longitude': 3, 'state': 6, 'vehicle-id': 1, 'time': 0, 'latitude': 4, 'speed': 5, 'driver-id': 2}
            hid = {h : i for i, h in enumerate(headers)}





            for row in reader:
                t = eval(row[hid['time']])
                did = row[hid['driver-id']]
                if did == '-1':
                    continue
                if t < tf_ts:
                    continue
                if t > tt_ts:
                    break
                longitude, latitude = eval(row[hid['longitude']]), eval(row[hid['latitude']])
                state = int(row[hid['state']])
                if not drivers_states.has_key(did): drivers_states[did] = FREE
                prev_state = drivers_states[did]
                if prev_state == FREE and state == POB:
                    #
                    # Only POB state logs will be recorded
                    # Find a cell in grid
                    i, j = bisect(x_points, longitude) - 1, bisect(y_points, latitude) - 1
                    with open(processed_log_fn, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile)
                        writer.writerow([t, i, j, did])
                drivers_states[did] = state


def get_csv_files(time_from, time_to):
    tf_date, tt_date = datetime.date(*time_from[:3]), datetime.date(*time_to[:3])
    target_date = tf_date
    csv_files = []
    while True:
        yy = '%02d' % (target_date.year - 2000)
        mm = '%02d' % target_date.month
        yymm = yy + mm
        csv_files.append('%s/20%s/%s/logs/logs-%s-normal.csv' % (taxi_home, yy, mm, yymm))
        target_date += relativedelta(months=+1)
        if tt_date <= target_date:
            break
    return csv_files


if __name__ == '__main__':
    run((2009, 1, 1, 0, 0, 0), (2009, 1, 5, 0, 0, 0))
