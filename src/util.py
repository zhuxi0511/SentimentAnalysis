#!/user/bin/env python
# coding: utf-8

import os
import sys
import datetime
import const

def save_preprocessed_result(result, file_name):
    data_dir = const.config_dict['data_dir']
    f = open(os.path.join(data_dir, file_name), 'w')
    for item_id, value in result.iteritems():
        tag = value['tag']
        feature_dict = value['feature']
        feature_list = map(lambda feature:':'.join(feature), 
                feature_dict.iteritems())
        f.write('%s\t%s\t%s\n' % (item_id, tag, ' '.join(feature_list)))

def save_feature_dict(feature_dict, file_name):
    data_dir = const.config_dict['data_dir']
    f = open(os.path.join(data_dir, file_name), 'w')
    for feature, feature_id in feature_dict.iteritems():
        f.write('%s\t%s\n' % (feature_id, feature))

def list_file(data_dir, data_file, class_of_data='train'):
    if data_file == 'ALL':
        name = '*'
    else:
        name = data_file
    data_file = os.path.join(data_dir, '%s.%s' % (name, class_of_data))
    res = os.popen('ls %s' % data_file)
    res_list = list(res.readlines())
    if len(res) == 0:
        return None, -1
    return map(lambda x:x.strip(), res_list), 0

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
