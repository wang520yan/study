# -*- coding:utf-8 -*-
# python的装饰器本质上是一个Python函数，它可以让其他函数在不需要做任何代码变动的前提下增加额外功能，装饰器的返回值也是一个函数对象。简单的说装饰器就是一个用来返回函数的函数。
# 它经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景。装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码并继续重用。
# 装饰器
def mywork(func):
    def inner():
        print "do first"
        func()
        print "do second"
    return inner

@mywork
def a1():
    print "test"


# 带一个参数的装饰器
def mywork1(func):
    def inner(arg):
        print "do first 1"
        func(arg)
        print "do second 1"
    return inner

@mywork1
def a2(arg):
    print "test1",arg


# 带动态参数的函数
def mywork2(func):
    def inner(*args,**kwargs):
        print "do first 2"
        func(*args,**kwargs)
        print "do second 2"
    return inner

@mywork2
def a3():
    print "no args"

@mywork2
def a4(arg):
    print "only one arg",arg

@mywork2
def a5(arg1,arg2):
    print "two args",arg1,arg2


# 装饰带返回值的函数
def mywork3(func):
    def inner(*args,**kwargs):
        print "121"
        result = func(*args,**kwargs)
        print "212"
        return result
    return inner

@mywork3
def a6(arg1,arg2):
    print 'i am zhangsan',arg1,arg2
    li = [1, 2, 3, 4, 5, 6]
    return li  # 返回一个列表


# 多个装饰器装饰一个函数
def newwork1(func):
    def inner():
        print "111111111111"
        func()
        print "222222222222"
    return inner
def newwork2(func):
    def inner():
        print "3333333333330"
        func()
        print "4444444444440"
    return inner

@newwork1
@newwork2
def a7():
    print "两层装饰器示例"


# 装饰器加参数
def filter(a1,a2):
    def outer(func):
        def wrapper(request,kargs):
            print a1
            result = func(request,kargs)
            print a2
            return result
        return wrapper
    return outer

aa = 111
bb = 222
@filter(aa,bb)
def a8(request,kargs):
    print request,kargs
    print "装饰器加参数示例"



# @filter(aa,bb)会先执行Filter(aa,bb)函数，获取到返回值outer后拼接成@outer，之后就变成普通的装饰器了
# wrapper函数内可以使用a1,a2,request,kargs 4个参数

if __name__ == '__main__':
    print "#####################################################################"
    a1()
    print "#####################################################################"
    a2("hello world")
    print "#####################################################################"
    a3()
    print "#####################################################################"
    a4("hello")
    print "#####################################################################"
    print a6("hhhh", "wwww")
    print "#####################################################################"
    a5("hello", "world")
    print "#####################################################################"
    a7()
    print "#####################################################################"
    a8("hello", "lisan")
