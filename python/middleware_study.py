# -*- coding:utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
# python 中间件,其实就是一个类，在请求到来和结束后，django会根据自己的规则在合适的时机执行中间件中相应的方法。
# settings模块中，有一个 MIDDLEWARE_CLASSES 变量，其中每一个元素就是一个中间件
# process_request(self,request)
# process_view(self, request, callback, callback_args, callback_kwargs)
# process_exception(self, request, exception)
# process_response(self, request, response)
# 每一个请求都是先通过中间件中的 process_request 函数，这个函数返回 None 或者 HttpResponse 对象，
# 如果返回None ，继续处理其它中间件，如果返回一个 HttpResponse，就处理中止，返回到网页上
# Django 会从 MIDDLEWARE_CLASSES 中按照从上到下的顺序一个个执行中间件中的 process_request 函数，
# 而其中 process_response 函数则是最前面的最后执行。

class RequestMiddleware1(object):

    def process_request(self,request):
        print "process_request 1111111111111"
    def process_view(self,rquest,callback,callback_args,callback_kwargs):
        print "processs_view 1111111111111111"
    def process_exception(self,request,exception):
        print "pocess_exception 11111111111111"
    def process_response(self,request,response):
        print "process response 11111111111111111"
        return response


class RequestMiddleware2(object):
    def process_request(self, request):
        print "process_request 22222222222222222222"

    def process_view(self, rquest, callback, callback_args, callback_kwargs):
        print "processs_view 22222222222222222222222"

    def process_exception(self, request, exception):
        print "pocess_exception 2222222222222222222"

    def process_response(self, request, response):
        print "process response 2222222222222222222"
        return response


# 在settings.py中将中间件引入
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session相关的中间件
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # 跨站请求伪造相关的中间件
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'study.middleware_study.RequestMiddleware1',   # 注册测试的中间件
    'study.middleware_study.RequestMiddleware2',   # 注册测试的中间件
)