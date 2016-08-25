import __init__
#
from information_boards.__init__ import AM2, AM5
from b_aggregated_analysis.__init__ import shifts_dir, shift_prefix
from b_aggregated_analysis.__init__ import shift_pro_dur_dir, shift_pro_dur_prefix
from b_aggregated_analysis.__init__ import vehicle_sharing_dir, vehicle_sharing_prefix
#
from taxi_common.file_handling_functions import remove_create_dir, save_pickle_file
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, gzip


def run():
    remove_create_dir(shift_pro_dur_dir); remove_create_dir(vehicle_sharing_dir)
    #
    init_multiprocessor(3)
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)

    # process_file('0901')


def process_file(yymm):
    print 'handle the file; %s' % yymm
    #        
    vehicle_sharing = {}
    productive_state = ['dur%d' % x for x in [0, 3, 4, 5, 6, 7, 8, 9, 10]]
    with gzip.open('%s/%s%s.csv.gz' % (shifts_dir, shift_prefix, yymm), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        with open('%s/%s%s.csv' % (shift_pro_dur_dir, shift_pro_dur_prefix, yymm), 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['yy', 'mm', 'dd', 'hh', 'vid', 'did', 'pro-dur']
            writer.writerow(new_headers)
            for row in reader:
                vid, did = row[hid['vehicle-id']], row[hid['driver-id']]
                #
                # Only consider trips whose start time is before 2 AM and after 6 AM
                #
                hh = eval(row[hid['hour']])
                if AM2 <= hh and hh <= AM5:
                    continue
                #
                productive_duration = sum(int(row[hid[dur]]) for dur in productive_state)
                writer.writerow([row[hid['year']][-2:], row[hid['month']], row[hid['day']], row[hid['hour']],
                                 vid, did, productive_duration])
                if not vehicle_sharing.has_key(vid):
                    vehicle_sharing[vid] = set()
                vehicle_sharing[vid].add(did)
    save_pickle_file('%s/%s%s.pkl' % (vehicle_sharing_dir, vehicle_sharing_prefix, yymm), vehicle_sharing)
    print 'end the file; %s' % yymm
    
if __name__ == '__main__':
    run()
