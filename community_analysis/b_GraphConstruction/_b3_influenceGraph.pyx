import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
from community_analysis import SIGINIFICANCE_LEVEL, MIN_PICKUP_RATIO, MIN_RATIO_RESIDUAL
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, get_fn_only, check_path_exist, save_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import pandas as pd
import statsmodels.api as sm
from traceback import format_exc

logger = get_logger()
numWorker = 3
#
year = '20%02d' % 9
depVar = 'roamingTime'
# depVar = 'interTravelTime'
#
#
if_dpath = dpaths[depVar, 'priorPresence']
if_prefixs = prefixs[depVar, 'priorPresence']
of_dpath = dpaths[depVar, 'influenceGraph']
of_prefixs = prefixs[depVar, 'influenceGraph']
try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(processorNum):
    for i, fn in enumerate(get_all_files(if_dpath, '%s%s*.csv' % (if_prefixs, year))):
        if i % numWorker != processorNum:
            continue
        fpath = '%s/%s' % (if_dpath, fn)
        process_file(fpath)


def process_file(fpath):
    logger.info('Start handling; %s' % fpath)
    _, _, _, _did1 = get_fn_only(fpath)[:-len('.csv')].split('-')
    try:
        ig_fpath = '%s/%s%s-%s.pkl' % (of_dpath, of_prefixs, year, _did1)
        count_fpath = '%s/%scount-%s-%s.pkl' % (of_dpath, of_prefixs, year, _did1)
        if check_path_exist(ig_fpath):
            return None
        #
        logger.info('Start loading; %s-%s' % (year, _did1))
        df = pd.read_csv(fpath)
        influenceGraph = {}
        countRelation = {k: 0 for k in ['pos', 'neg']}
        did1_df = df.drop(['month', 'day', 'hour', 'zi', 'zj', 'did'], axis=1)
        if _did1 in did1_df.columns:
            did1_df = did1_df.drop([], axis=1)
        #
        inDepVar = [cn for cn in did1_df.columns if cn != depVar]
        y = did1_df[depVar]
        X = did1_df[inDepVar]
        X = sm.add_constant(X)
        res = sm.OLS(y, X, missing='drop').fit()
        for _did0, pv in res.pvalues.iteritems():
            if _did0 == 'const':
                continue
            coef = res.params[_did0]
            if coef < 0:
                countRelation['neg'] += 1
                influenceGraph[int(_did0), int(_did1)] = (pv, coef)
            elif coef > 0:
                countRelation['pos'] += 1
        #
        logger.info('Start pickling; %s-%s' % (year, _did1))
        save_pickle_file(ig_fpath, influenceGraph)
        save_pickle_file(count_fpath, countRelation)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], '%s-%s' % (year, _did1)), 'w') as f:
            f.write(format_exc())
        raise

if __name__ == '__main__':
    run()
