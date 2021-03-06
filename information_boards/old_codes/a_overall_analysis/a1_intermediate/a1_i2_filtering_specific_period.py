#
import csv
import datetime

from information_boards import error_hours
from information_boards.old_codes.a_overall_analysis import trips_dpath, trip_prefix


def run():
    for ys, ms, ds, hs in error_hours:
        yymm = '%02d%02d' % (int(ys), int(ms))
        dd, hh = int(ds), int(hs)
        fpath = '%s/%s%s.csv' % (trips_dpath, trip_prefix, yymm)
        temp_fpath = '%s/%s%s.csv.tmp' % (trips_dpath, trip_prefix, yymm)
        with open(fpath, 'rb') as r_csvfile1:
            reader = csv.reader(r_csvfile1)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            with open(temp_fpath, 'wb') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow(headers)
                for row in reader:
                    t = eval(row[hid['start-time']])
                    cur_dt = datetime.datetime.fromtimestamp(t)
                    if cur_dt.day == dd and cur_dt.hour == hh:
                        continue
                    writer.writerow(row)


if __name__ == '__main__':
    run()