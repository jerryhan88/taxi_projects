import os, sys, platform
#
# Check environments and set a prefix for finding files and libraries
#
taxi_home, taxi_data = None, None
#
py_vinfo = sys.version_info
if type(sys.version_info) == type(()):
    print 'This python is not 2.7 version'
    assert False
if py_vinfo.major == 2 and py_vinfo.minor == 7:
    plf = platform.platform()
    if plf.startswith('Linux'):
        # Linux server
        sys.path.append('/home/ckhan/local/lib/python2.7/site-packages')
        sys.path.append('/home/ckhan/local/lib64/python2.7/site-packages')
        taxi_data = '/home/ckhan/taxi_data'
    elif plf.startswith('Darwin'):
        # Mac
        taxi_data = '/Users/JerryHan88/taxi_data'
        pass
    else:
        # Window ?
        taxi_data = 'C:\Users/ckhan.2015/taxi_data'
        pass
    sys.path.append(os.getcwd() + '/..')
#     sys.path.append(os.getcwd() + '/../taxi_common/test')
else:
    print 'This python is not 2.7 version'
    assert False
#
singapore_poly_fn = os.path.dirname(os.path.realpath(__file__)) + '/Singapore_polygon'
#
def get_taxi_home_path():
    return taxi_home

def get_taxi_data_path():
    return taxi_data