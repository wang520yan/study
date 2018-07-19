# -*- coding: utf-8 -*-
import hashlib
import json
import os
import re
import time
import datetime
from functools import wraps
import logging
from rest_framework.response import Response
from rest_framework import status

# 响应头的通用字段
RESPONSE_HEADER = {
    "Server": "IIE CAS",
    # "Date": datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
}


# 打印请求头和请求数据，返回请求数据
def print_header_data(request):
    request_data = ''
    if request.method == 'GET':
        request_data = request.GET
    elif request.method == 'POST':
        request_data = request.data
    return request_data


def ui_message_response(code, log_message, message, status_code=status.HTTP_400_BAD_REQUEST,
                        headers=RESPONSE_HEADER):
    """
    自定义UI响应消息.

    :param code:               响应消息编码（自定义）
    :param log_message:        日志信息（开发者查看）
    :param message:            响应信息（请求用户查看）
    :param status_code:        响应状态码
    :param headers:            响应头
    :return:                   a REST framework's Response object
    """
    resp_data = {
        'code': code,
        'msg': message
    }
    if status_code != status.HTTP_200_OK:
        print '[ Error ] %d: %s(%d)' % (code, log_message, status_code)
    else:
        print '[ Success ] %d: %s(%d)' % (code, log_message, status_code)
    return Response(resp_data, status_code, headers=headers, content_type='application/json;charset=utf-8')



def get_current_time():
    """
    获取指定格式的当前时间.
    时间格式：yyyy-MM-dd HH:mm:ss
    """
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')


def get_last_days(num):
    """
    获得最近num天（包括当前日期）的日期字符串列表.
    """
    str_now = time.strftime('%Y-%m-%d', time.localtime())
    now_date = datetime.datetime.strptime(str_now, '%Y-%m-%d')
    date_list = []
    for day in range(num - 1, -1, -1):
        date = now_date - datetime.timedelta(days=day)
        date_list.append(date.strftime("%Y-%m-%d"))
    return date_list


def detector_message_response(code, log_message, message, status_code=status.HTTP_400_BAD_REQUEST,
                              headers=RESPONSE_HEADER):
    """
    自定义前端检测器消息响应.

    :param code:               响应消息编码（自定义）
    :param log_message:        日志信息（开发者查看）
    :param message:            响应信息（前端监测器查看）
    :param status_code:        HTTP响应状态码
    :param headers:            响应头
    :return:                   a REST framework's Response object
    """
    # resp_data = {
    #     'type': code,
    #     'message': message
    # }
    if status_code != status.HTTP_200_OK:
        resp_data = {'message': message}
        print '[ Error ] %d: %s(%d)' % (code, log_message, status_code)
    else:
        resp_data = message
        print '[ Success ] %d: %s(%d)' % (code, log_message, status_code)
    return Response(resp_data, status_code, headers=headers)


def ui_message_response(code, log_message, message, status_code=status.HTTP_400_BAD_REQUEST,
                        headers=RESPONSE_HEADER):
    """
    自定义UI响应消息.

    :param code:               响应消息编码（自定义）
    :param log_message:        日志信息（开发者查看）
    :param message:            响应信息（请求用户查看）
    :param status_code:        响应状态码
    :param headers:            响应头
    :return:                   a REST framework's Response object
    """
    resp_data = {
        'code': code,
        'msg': message
    }
    if status_code != status.HTTP_200_OK:
        print '[ Error ] %d: %s(%d)' % (code, log_message, status_code)
    else:
        print '[ Success ] %d: %s(%d)' % (code, log_message, status_code)
    return Response(resp_data, status_code, headers=headers, content_type='application/json;charset=utf-8')


def is_valid_user_agent(user_agent):
    """
    检验User_Agent是否符合要求.
    User_Agent的标准：device_id/soft_version(vendor_name).其中，
    device_id：     12位数字的字符串；
    soft_version：  不超过32位的字符串，其前8位是表示日期的数字，第9位是下划线；
    vendor_name：   不超过32位的字符串
    """
    if isinstance(user_agent, basestring):
        m = re.match(r'\d{12}[/]\d{8}[_].{0,23}[(].{0,32}[)]', user_agent)
        if str(m) != 'None':
            try:
                time.strptime(user_agent[13:21], '%Y%m%d')
                return True
            except Exception:
                return False
        else:
            return False
    else:
        return False


def get_detector_id(request):
    """
    判断并获取请求头中的检测器ID
    """
    user_agent = request.META.get('HTTP_USER_AGENT')   # 请求头中的User-Agent
    if user_agent is None:
        return detector_message_response(400, '请求头中没有User-Agent字段', '请求头中没有User-Agent字段')
    elif not is_valid_user_agent(user_agent):
        return detector_message_response(400, '请求头中的User_Agent字段不符合要求',
                                         '请求头中的User_Agent字段不符合要求')
    else:
        return user_agent[0:12]   # 从User-Agent中提取检测器ID并返回



# 文件上传，保存在服务器上
def handle_upload_file(absolute_path, f, save_name=''):
    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)
    if save_name != '':
        file_name = os.path.join(absolute_path, save_name)
    else:
        file_name = os.path.join(absolute_path, f.name)
    if os.path.exists(file_name):
        return False
    else:
        file_save = open(file_name, 'wb')
        for chunk in f.chunks():
            file_save.write(chunk)
        # for line in f:
        #     file_save.write(line)
        file_save.close()
        return True


# 获取文件的md5值(每次读取一部分进行计算，避免一次性读取大文件)
def calc_md5(file_path, chunk_size=512):
    md5obj = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            md5obj.update(data)
    return md5obj.hexdigest()

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
       # 'rest_framework.renderers.BrowsableAPIRenderer',
    ),
 'PAGE_SIZE': 10,
}


# 获取界面显示每页起始条目和每页条数
def get_page_data(request_data):
    page_num = int(request_data.get('pn', 1))                                 # 页码，默认为第一页
    page_size = int(request_data.get('p_size', REST_FRAMEWORK['PAGE_SIZE']))  # 每页条数，默认为预设值

    start_pos = (page_num - 1) * page_size                                    # 每页起始条码
    end_pos = page_num * page_size                                            # 每页结束条码

    return start_pos, end_pos, page_size


class ComplexEncoder(json.JSONEncoder):
    """
    json扩展，支持datetime类型
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def timethis(func):
    """
    Decorator that reports the execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper


def logged(level, name=None, message=None):
    """
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    日志级别：
        critical > error > warning > info > debug,notset
        级别越高打印的日志越少，反之亦然，即
        logging.DEBUG   debug    : 打印全部的日志(notset等同于debug)
        logging.INFO    info     : 打印info,warning,error,critical级别的日志
        logging.WARNING   warning  : 打印warning,error,critical级别的日志
        logging.ERROR     error    : 打印error,critical级别的日志
        logging.CRITICAL   critical : 打印critical级别
    """
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate

if __name__ == '__main__':
    print get_current_time()
    ui_message_response(200, '查询成功', ' 结果集', status.HTTP_200_OK)