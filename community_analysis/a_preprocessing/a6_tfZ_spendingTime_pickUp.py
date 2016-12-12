import __init__
#
'''

'''
#
from community_analysis import tfZ_SP_dpath, tfZ_SP_prepix
from community_analysis import tfZ_spendingTime_dpath, tfZ_spendingTime_prepix
from community_analysis import tfZ_pickUp_dpath, tfZ_pickUp_prepix
from community_analysis import X_PICKUP, O_PICKUP
from community_analysis import HOUR1
#
from taxi_common import ss_drivers_dpath, ss_drivers_prefix
from taxi_common.file_handling_functions import check_dir_create, get_all_directories, check_path_exist, load_pickle_file, get_all_files
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv

logger = get_logger()


def run():
    check_dir_create(tfZ_SP_dpath)
    #
    # init_multiprocessor(11)
    # count_num_jobs = 0
    # for y in range(9, 10):
    #     for m in range(1, 13):
    #         yymm = '%02d%02d' % (y, m)
    #         # process_file(yymm)
    #         put_task(process_month, [yymm])
    #         count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)
    #
    numWorker = 11
    init_multiprocessor(numWorker)
    count_num_jobs = 0
    numReducers = numWorker * 10
    for y in range(9, 10):
        yyyy = '20%02d' % (y)
        logger.info('loading ss drivers %s' % yyyy)
        ss_drivers_fpath = '%s/%s%s.pkl' % (ss_drivers_dpath, ss_drivers_prefix, yyyy)
        ss_drivers = load_pickle_file(ss_drivers_fpath)
        driver_subsets = [[] for _ in range(numReducers)]
        for i, did in enumerate(ss_drivers):
            driver_subsets[i % numReducers].append(did)

        for i, driver_subset in enumerate(driver_subsets):
            # year_arrangement(yyyy, i, driver_subset)
            put_task(year_arrangement, [yyyy, i, driver_subset])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    #


def process_month(yymm):
    from traceback import format_exc
    #
    try:
        logger.info('Handle %s' % yymm)
        yy, mm = yymm[:2], yymm[-2:]
        yyyy = '20%s' % yy
        tfZ_DP_fpath = '%s/%s%s.csv' % (tfZ_SP_dpath, tfZ_SP_prepix, yymm)
        ss_drivers_fpath = '%s/%s%s.pkl' % (ss_drivers_dpath, ss_drivers_prefix, yyyy)
        tfZ_pickUp_fpath = '%s/%s%s.pkl' % (tfZ_pickUp_dpath, tfZ_pickUp_prepix, yymm)
        tfZ_duration_fpath = '%s/%s%s.pkl' % (tfZ_spendingTime_dpath, tfZ_spendingTime_prepix, yymm)
        if check_path_exist(tfZ_DP_fpath):
            logger.info('Already handled %s' % yymm)
            return None
        #
        logger.info('loading ss drivers %s' % yymm)
        ss_drivers = load_pickle_file(ss_drivers_fpath)
        #
        logger.info('Loading pickUp %s' % yymm)
        pickUp = load_pickle_file(tfZ_pickUp_fpath)
        #
        logger.info('Loading duration %s' % yymm)
        tfZ_duration = load_pickle_file(tfZ_duration_fpath)
        #
        logger.info('Generate duration-pickUp %s' % yymm)
        with open(tfZ_DP_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['month', 'day', 'timeFrame', 'zi', 'zj', 'tfZ', 'did', 'spendingTime']
            for did in ss_drivers:
                header.append(did)
            writer.writerow(header)
        #
        old_per, per_interval = 0, 5
        for i, ((did1, month, day, timeFrame, zi, zj), rt) in enumerate(tfZ_duration.iteritems()):
            if rt <= 0:
                continue
            if rt >= HOUR1:
                continue
            tfZ = '(%d,%d,%d)' % (timeFrame, zi, zj)
            with open(tfZ_DP_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_row = [month, day, timeFrame, zi, zj,
                           tfZ, did1, rt]
                for did0 in ss_drivers:
                    k = (did0, month, day, timeFrame, zi, zj)
                    new_row.append(O_PICKUP if k in pickUp else X_PICKUP)
                writer.writerow(new_row)
            cur_per = i / float(len(tfZ_duration)) * 100
            if old_per + per_interval < cur_per:
                logger.info('\t processed %.2f  %s' % (cur_per, yymm))
                old_per += per_interval
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


def year_arrangement(yyyy, reducerID, driver_subset):
    from traceback import format_exc
    #
    try:
        logger.info('Handle arrange %s(%d)' % (yyyy, reducerID))
        tfZ_DP_year_fpath = '%s/%s%s-%d.csv' % (tfZ_SP_dpath, tfZ_SP_prepix, yyyy, reducerID)
        yy = yyyy[2:]
        for tfZ_DP_month_fn in get_all_files(tfZ_SP_dpath, '%s%s*.csv' % (tfZ_SP_prepix, yy)):
            tfZ_DP_month_fpath = '%s/%s' % (tfZ_SP_dpath, tfZ_DP_month_fn)
            logger.info('Handling %s(%d); %s' % (yyyy, reducerID, tfZ_DP_month_fpath))
            with open(tfZ_DP_month_fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                header = reader.next()
                hid = {h: i for i, h in enumerate(header)}
                if not check_path_exist(tfZ_DP_year_fpath):
                    with open(tfZ_DP_year_fpath, 'wt') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow(header)
                for row in reader:
                    did = int(row[hid['did']])
                    if did not in driver_subset:
                        continue
                    with open(tfZ_DP_year_fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow(row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yyyy), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    import time
    time.sleep(90 * 60)
    run()