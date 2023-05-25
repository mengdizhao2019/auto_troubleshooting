import re
from time import time
import datetime
import os
import os.path
import string
import re
import sys
import json

def convert_to_mb(integer):
    mb = integer / (1024 ** 2)
    return mb

def convert_special_characters(filename):
    # 移除文件名中的特殊字符
    cleaned_filename = ''.join(c for c in filename if c.isalnum() or c in ['_', '-', '.'])

    # 规范化文件路径，处理斜杠和特殊字符
    normalized_path = os.path.normpath(cleaned_filename)

    return normalized_path

def convert_to_filename(string):
    # 用正则表达式替换非字母数字字符为下划线
    return re.sub(r'\W+', '_', string)

def delete_all_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            delete_all_files(dir_path)
            os.rmdir(dir_path)

def calucate_cost(timestamp_string_begin, timestamp_string_end):
    datetime_diff = string_to_datetime(timestamp_string_end).timestamp() - string_to_datetime(timestamp_string_begin).timestamp()
    datetime_diff = round(datetime_diff * 1000)
    return datetime_diff

def ms_cost_to_timestring(ms):
    m, s = divmod(ms / 1000, 60)
    h, m = divmod(m, 60)
    return ("%02d:%02d:%02d %03d" % (h, m, s, ms%1000))

def get_timestamp_string(line):
    return line[0 : len("2018-03-12 05:55:26 943")]

def string_to_datetime(timestamp_string):

    index_2 = len("2018-03-12 05:55:26 943")
    if len(timestamp_string) > index_2:
        timestamp_string = timestamp_string[0:index_2]
        
    length = len(timestamp_string)
    time_string = timestamp_string[0 : length - 4]
    msec = int(timestamp_string[length - 3 : length])
    datetime_temp = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
    datetime_temp = datetime_temp + datetime.timedelta(microseconds = msec * 1000)
    return datetime_temp

def find_pid_tid(line, onlypid = False):
    ret = re.search(r'\[(\d+:\d+)]', line)
    if ret:
        if onlypid:
            return ret.group(1)[:ret.group(1).find(':')]
        else:
            return ret.group(1)
    if onlypid:
        return "-1"
    else:
        return "-1:-1"
    
def str_to_datetime(date_string):
    formats = [
        '%Y-%m-%d %H:%M:%S,%f',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d %H',
        '%Y-%m-%d',
    ]
    for format_str in formats:
        try:
            return datetime.datetime.strptime(date_string, format_str)
        except ValueError:
            pass
    raise ValueError(f'Invalid date string: {date_string}')

    
    
if __name__ == "__main__":
    pass
