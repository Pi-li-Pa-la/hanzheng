# ! /usr/bin/python
# -*- coding: utf-8 -*-

import time, struct, os
# from openpyxl import Workbook, load_workbook
from jinja2 import Environment, FileSystemLoader

log_config = {
}


def set_log_path():
    # 日志函数辅助函数
    fmt = '%Y%m%d%H%M%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    log_config['file'] = 'logs/log.{}.txt'.format(dt)


def log(*args, **kwargs):
    # 日志函数，直接调用即可输出日志
    fmt = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    path = log_config.get('file')
    if path is None:
        set_log_path()
        path = log_config['file']
    with open(path, 'a') as f:
        print(dt, *args, file=f, **kwargs)


path = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)


# 此函数作为valid_data_type函数的补充函数。
# 此函数意在检测字符串格式是否符合mysql int类型数据的格式。
def m(str):
    import re
    if re.match(r"^[0-9]{1,11}$", str):
        return True
    elif re.match(r"^[0-9\-][0-9]{1,10}$", str):
        return True
    return False


# mysql data_type验证函数,验证字符串是否符合mysql int类型数据的格式
def valid_int_type(valid_str):
    if m(valid_str):
        if (int(valid_str) > -2147483648) and (int(valid_str) < 4294967295):
            return True
    return False
