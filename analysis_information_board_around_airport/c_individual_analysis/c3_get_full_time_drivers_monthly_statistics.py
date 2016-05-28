from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import ftd_shift_dir
from supports._setting import ftd_shift_prefix, full_time_drivers_prefix
from supports._setting import ftd_trips_dir, ftd_trips_prefix
from supports._setting import ap_trips_economic_profits_dir, ap_trips_ecoprof_prefix
from supports._setting import ns_trips_economic_profits_dir, ns_trips_ecoprof_prefix
#
from supports._setting import ftd_general_stat_dir, ftd_general_stat_prefix
from supports._setting import ftd_prev_in_ap_stat_dir, ftd_prev_in_ap_stat_prefix
from supports._setting import ftd_prev_out_ap_stat_dir, ftd_prev_out_ap_stat_prefix
from supports._setting import ftd_prev_in_ns_stat_dir, ftd_prev_in_ns_stat_prefix
from supports._setting import ftd_prev_out_ns_stat_dir, ftd_prev_out_ns_stat_prefix
from supports._setting import DInAP_PInAP, DOutAP_PInAP
from supports._setting import DInNS_PInNS, DOutNS_PInNS
from supports.etc_functions import remove_creat_dir
from supports.etc_functions import load_picle_file
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
import pandas as pd
#
SEC = 60
#
def run():
    for dn in [ftd_general_stat_dir, ftd_prev_in_ap_stat_dir, ftd_prev_out_ap_stat_dir, ftd_prev_in_ns_stat_dir, ftd_prev_out_ns_stat_dir]:
        remove_creat_dir(dn)
    #
    init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
#             process_files(yymm)
            put_task(process_files, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    
def process_files(yymm):
    print 'handle the file; %s' % yymm
    #
    init_csv_files(yymm)
    #
    full_dids = sorted([eval(x) for x in load_picle_file('%s/%s%s.pkl' % (ftd_shift_dir, full_time_drivers_prefix, yymm))])
    s_df = pd.read_csv('%s/%s%s.csv' % (ftd_shift_dir, ftd_shift_prefix, yymm))
    trip_df = pd.read_csv('%s/%s%s.csv' % (ftd_trips_dir, ftd_trips_prefix, yymm))
    ap_trip_df = pd.read_csv('%s/%s%s.csv' % (ap_trips_economic_profits_dir, ap_trips_ecoprof_prefix, yymm))
    ns_trip_df = pd.read_csv('%s/%s%s.csv' % (ns_trips_economic_profits_dir, ns_trips_ecoprof_prefix, yymm))
    #
    yy, mm = int(yymm[:2]), int(yymm[2:])
    for did in full_dids:
        #
        # General
        #
        did_sh = s_df[(s_df['did'] == did)]
        pro_dur = sum(did_sh['pro-dur']) * SEC
        did_wt = trip_df[(trip_df['did'] == did)]
        total_fare = sum(did_wt['fare'])
        if pro_dur > 0 and total_fare != 0:
            total_prod = total_fare / pro_dur
            with open('%s/%s%s.csv' % (ftd_general_stat_dir, ftd_general_stat_prefix, yymm), 'a') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow([yy, mm, did, pro_dur, total_fare, total_prod])
        #
        # airport trips
        #
        did_ap = ap_trip_df[(ap_trip_df['did'] == did)]
        prev_in_ap_trip = did_ap[(did_ap['ap-trip-mode'] == DInAP_PInAP)]
        prev_out_ap_trip = did_ap[(did_ap['ap-trip-mode'] == DOutAP_PInAP)]
        #
        if len(did_ap) != 0:
            #
            # prev in ap trip
            #
            ap_qu, ap_dur = sum(prev_in_ap_trip['ap-queue-time']), sum(prev_in_ap_trip['duration'])
            ap_fare = sum(prev_in_ap_trip['fare'])
            ap_eco_profit = sum(prev_in_ap_trip['economic-profit'])
            if ap_qu + ap_dur > 0 and ap_fare != 0:
                ap_prod = ap_fare / (ap_qu + ap_dur)
                with open('%s/%s%s.csv' % (ftd_prev_in_ap_stat_dir, ftd_prev_in_ap_stat_prefix, yymm), 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow([yy, mm, did, ap_qu, ap_dur, ap_fare, ap_prod, ap_eco_profit])
            #
            # prev out ap trip
            #
            ap_qu, ap_dur = sum(prev_out_ap_trip['ap-queue-time']), sum(prev_out_ap_trip['duration'])
            ap_fare = sum(prev_out_ap_trip['fare'])
            ap_eco_profit = sum(prev_out_ap_trip['economic-profit'])
            if ap_qu + ap_dur > 0 and ap_fare != 0:
                ap_prod = ap_fare / (ap_qu + ap_dur)
                with open('%s/%s%s.csv' % (ftd_prev_out_ap_stat_dir, ftd_prev_out_ap_stat_prefix, yymm), 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow([yy, mm, did, ap_qu, ap_dur, ap_fare, ap_prod, ap_eco_profit])    
        #
        # night safari trips
        #
        did_ns = ns_trip_df[(ns_trip_df['did'] == did)]
        prev_in_ns_trip = did_ns[(did_ns['ns-trip-mode'] == DInNS_PInNS)]
        prev_out_ns_trip = did_ns[(did_ns['ns-trip-mode'] == DOutNS_PInNS)]
        #
        if len(did_ns) != 0:
            #
            # prev in ns trip
            #
            ns_qu, ns_dur = sum(prev_in_ns_trip['ns-queue-time']), sum(prev_in_ns_trip['duration'])
            ns_fare = sum(prev_in_ns_trip['fare'])
            ns_eco_profit = sum(prev_in_ns_trip['economic-profit'])
            if ns_qu + ns_dur > 0 and ns_fare != 0:
                ns_prod = ns_fare / (ns_qu + ns_dur)
                with open('%s/%s%s.csv' % (ftd_prev_in_ns_stat_dir, ftd_prev_in_ns_stat_prefix, yymm), 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow([yy, mm, did, ns_qu, ns_dur, ns_fare, ns_prod, ns_eco_profit])
            #
            # prev out ns trip
            #
            ns_qu, ns_dur = sum(prev_out_ns_trip['ns-queue-time']), sum(prev_out_ns_trip['duration'])
            ns_fare = sum(prev_out_ns_trip['fare'])
            ns_eco_profit = sum(prev_out_ns_trip['economic-profit'])
            if ns_qu + ns_dur > 0 and ns_fare != 0:
                ns_prod = ns_fare / (ns_qu + ns_dur)
                with open('%s/%s%s.csv' % (ftd_prev_out_ns_stat_dir, ftd_prev_out_ns_stat_prefix, yymm), 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow([yy, mm, did, ns_qu, ns_dur, ns_fare, ns_prod, ns_eco_profit])
    print 'End the file; %s' % yymm

def init_csv_files(yymm):
    with open('%s/%s%s.csv' % (ftd_general_stat_dir, ftd_general_stat_prefix, yymm), 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        headers = ['yy', 'mm', 'did', 'total-pro-dur', 'total-fare', 'total-prod']
        writer.writerow(headers)
    #
    for dn, fn_prefix in [(ftd_prev_in_ap_stat_dir, ftd_prev_in_ap_stat_prefix), (ftd_prev_out_ap_stat_dir, ftd_prev_in_ap_stat_prefix)]:
        with open('%s/%s%s.csv' % (dn, fn_prefix, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            headers = ['yy', 'mm', 'did', 'ap-queue-time', 'ap-dur', 'ap-fare', 'ap-prod', 'ap-eco-profit']
            writer.writerow(headers)
    #
    for dn, fn_prefix in [(ftd_prev_in_ns_stat_dir, ftd_prev_in_ns_stat_prefix), (ftd_prev_out_ns_stat_dir, ftd_prev_in_ns_stat_prefix)]:
        with open('%s/%s%s.csv' % (dn, fn_prefix, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            headers = ['yy', 'mm', 'did', 'ns-queue-time', 'ns-dur', 'ns-fare', 'ns-prod', 'ns-eco-profit']
            writer.writerow(headers)

if __name__ == '__main__':
    run()
    