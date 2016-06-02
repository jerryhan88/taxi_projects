from __future__ import division
#
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
import csv
#
TAXI_HOME = '/home/taxi'
USER_HOME = '/home/temp'
YEARS = ['2011', '2012']
MONTHS = ['01', '02', '03', '04', '05', '06',
          '07', '08', '09', '10', '11', '12']

def combine_trip_data():
    print 'Start combine'
    for y in YEARS:
        y_two_digit = y[-2:]
        for m in MONTHS:
            if os.path.exists(USER_HOME + '/taxi/trips/trips-%s%s.csv' % (y_two_digit, m)):
                continue
            normal_file = TAXI_HOME + '/%s/%s/trips/trips-%s%s-normal.csv' % (y, m, y_two_digit, m)
            ext_file = TAXI_HOME + '/%s/%s/trips/trips-%s%s-normal-ext.csv' % (y, m, y_two_digit, m)
            read_write_a_trip(normal_file, ext_file)
    

def combine_trip_data_with_multi():
    '''
    In the server, when two files are combined, a trip can totally be expressed
    A trip data shows the below information;
    
    trip-id,job-id,start-time,end-time,start-long,start-lat,end-long,end-lat,vehicle-id,distance,fare,duration,start-dow,start-day,start-hour,start-minute,end-dow,end-day,end-hour,end-minute,start-zone,end-zone,start-postal,end-postal,driver-id
    
    ex.
    6029L09010100005,001010000,1230739200,1230739680,103.95029,1.37226,103.93417,1.38599,8069,3.4,850,480,4,1,0,0,4,1,0,8,51,51,518457,519355,20108
    
    '''
    print 'Start combine'
    for y in YEARS:
        y_two_digit = y[-2:]
        for m in MONTHS:
            normal_file = TAXI_HOME + '/%s/%s/trips/trips-%s%s-normal.csv' % (y, m, y_two_digit, m)
            ext_file = TAXI_HOME + '/%s/%s/trips/trips-%s%s-normal-ext.csv' % (y, m, y_two_digit, m)
            read_write_a_trip(normal_file, ext_file)

def read_write_a_trip(nf, ef):
    target_period = nf.split('/')[-1].split('-')[1]
    # Read data from files
    normal_data = csv_read_whole(nf)
    if normal_data == None:
        return None 
    #
    ext_data = csv_read_whole(ef)
    #
    assert len(normal_data) == len(ext_data), (target_period, len(normal_data), len(ext_data)) 
    # Write a combined file
    combined_file = USER_HOME + '/trips_merged/trips-%s.csv' % (target_period)
    with open(combined_file, 'wt') as csvfile:
        writer = csv.writer(csvfile)
        for i in xrange(len(normal_data)):
            writer.writerow(normal_data[i] + ext_data[i])
    del normal_data, ext_data  
            
def csv_read_whole(fn):
    rv = []
    with open(fn, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rv.append(row)
    return rv

def test_single_run():
    normal_file = TAXI_HOME + '/2009/01/trips/trips-0901-normal.csv'
    ext_file = TAXI_HOME + '/2009/01/trips/trips-0901-normal-ext.csv'
    read_write_a_trip(normal_file, ext_file)

if __name__ == '__main__':
    '''
    just test!!
    '''
    
#     from shapely.geometry import Polygon
#     print 'test!!'
#     test_single_run()
#     combine_trip_data_with_multi()
    combine_trip_data()
    