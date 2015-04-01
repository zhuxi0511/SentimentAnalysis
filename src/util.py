#!/user/bin/env python
# coding: utf-8

import os
import sys
import datetime
import const

def save_preprocessed_result(result, file_name):
    data_dir = const.config_dict['data_dir']
    f = open(os.path.join(data_dir, file_name), 'w')
    for item in result:
        item_id = item['item_id']
        value = item['value']
        value = map(lambda feature:':'.join(feature), value.items())
        f.write('%s\t%s\n' % (item_id, '\t'.join(value)))

def get_file_to_local(hadoop_bin, hadoop_dir, local_file, type):
    """ get hadoop file to local directory"""

    if (type=='file'):
        test_hadoop_cmd = hadoop_bin + ' fs -test -e ' + hadoop_dir
        test_local_cmd = 'test -e ' + local_file
        rm_local_cmd = 'rm ' + local_file
        get_cmd = hadoop_bin + ' fs -get ' + hadoop_dir + ' ' + local_file
    elif (type=='dir'):
        test_hadoop_cmd = hadoop_bin + ' fs -test -d ' + hadoop_dir
        test_local_cmd = 'test -e ' + local_file
        rm_local_cmd = 'rm ' + local_file
        get_cmd = hadoop_bin + ' fs -getmerge ' + hadoop_dir + ' ' + local_file
    else:
        print >> sys.stderr, "function GetFileToLocal param error."
        return 1
    if os.system(test_hadoop_cmd) != 0:
        print >> sys.stderr, "Hadoop file do not exist"
        return 1
    if os.system(test_local_cmd) == 0:
        os.system(rm_local_cmd)
    os.system(get_cmd)
    return 0


def put_file_to_hadoop(hadoop_bin, hadoop_file, local_file):
    """ put local file to hadoop """

    test_hadoop_cmd = hadoop_bin + ' fs -test -e ' + hadoop_file
    test_local_cmd = 'test -e ' + local_file
    rm_hadoop_cmd = hadoop_bin + ' fs -rm ' + hadoop_file
    put_cmd = hadoop_bin + ' fs -put ' + local_file + ' ' + hadoop_file
    if os.system(test_local_cmd) != 0:
        print >> sys.stderr, "Local file do not exist"
        return 1
    if os.system(test_hadoop_cmd) == 0:
        os.system(rm_hadoop_cmd)
    print put_cmd
    os.system(put_cmd)
    return 0

# class DateHour
class DateHour(object):
    def __init__(self):
        self.datetime = datetime.datetime.now()

    def __str__( self ):
        return self.datetime.strftime("%Y-%m-%d %H:%M:%S")

    def set_date_hour(self, year, month, day, hour=0, minute=0, second=0, microsecond=0):
        self.datetime = datetime.datetime(year, month, day, hour, minute, second, microsecond)

    def shift(self, days=0, hours=0):
        _days = days
        _seconds = 60*60*hours
        self.datetime = self.datetime + datetime.timedelta(days=_days, seconds=_seconds)
        
    def get_date_hour( self, days=0, hours=0):
        _days = days
        _seconds = 60*60*hours
        _datetime = self.datetime + datetime.timedelta(days=_days, seconds=_seconds)
        
        date = '%04d%02d%02d' %(_datetime.year, _datetime.month, _datetime.day)
        hour = '%02d:%02d:%02d' %(_datetime.hour, _datetime.minute, _datetime.second)
        return (date, hour)

if __name__ == '__main__':
    d = DateHour()
    print d.get_date_hour()
