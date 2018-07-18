# -*- coding: utf-8 -*-
from django.db.models import Q, F, Sum

from models_study.models import UserLogin, RoleLogin


def save_user():
    """
    增加用户
    :return:
    """
    user_query = UserLogin.objects.all()
    for user in user_query:
        print user
    user_query_1 = UserLogin.objects.all()[0:2]
    user_query_2 = UserLogin.objects.filter(user_id__iexact=1)  # list=BookInfo.books.filter(id=1)
    user_query_3 = UserLogin.objects.filter(user_name__contains='wang')
    user_query_4 = UserLogin.objects.filter(user_name__startswith='w')  # user_name__endswith
    user_query_5 = UserLogin.objects.filter(user_name__isnull=False)
    # 以上运算符都区分大小写，在这些运算符前加上i表示不区分大小写，如iexact、icontains、istartswith、iendswith
    user_query_6 = UserLogin.objects.filter(pk__in=[1,2,3]) # in：是否包含在范围内
    # gt、gte、lt、lte：大于、大于等于、小于、小于等于
    user_query_7 = UserLogin.objects.filter(id__gt=3)
    # 不等于使用等于的运算符，使用exclude()过滤器
    user_query_8 = UserLogin.objects.exclude(id=3)
    # year、month、day、week_day、hour、minute、second：对日期时间类型的属性进行运算
    user_query_9 = UserLogin.objects.filter(create_time__year=2017)
    # 查询1980年1月1日后注册的账户
    user_query_10 = UserLogin.objects.filter(create_time__gt=(2017,10,15))

    # 关联关系
    # 关联模型类名小写__属性名__运算符=值，
    role_query_1 = RoleLogin.objects.filter(userlogin__user_name__contains='wang')
    role_query_2 = UserLogin.objects.filter(role_id__exact=1)

    # F对象 之前的查询都是对象的属性与常量值比较，两个属性怎么比较呢？ 答：使用F对象，被定义在django.db.models中
    UserLogin.objects.filter(userlogin__id__gt=F('id'))


    # Q对象 多个过滤器逐个调用表示逻辑与关系，同sql语句中where部分的and关键字
    UserLogin.objects.filter(user_id=1,user_name='wangyan')
    UserLogin.objects.filter(user_id=1).filter(user_name='wangyan')

    # 如果需要实现逻辑或or的查询，需要使用Q()对象结合|运算符,Q对象被义在django.db.models中
    # Q(属性名__运算符=值)
    UserLogin.objects.filter(Q(user_id__gt=1))
    # Q对象可以使用&、|连接，&表示逻辑与，|表示逻辑或
    UserLogin.objects.filter(Q(user_id__gt=20) | Q(pk__lt=3))
    # Q对象前可以使用~操作符，表示非not
    UserLogin.objects.filter(~Q(pk=3))

    # 聚合函数, 使用aggregate()过滤器调用聚合函数, 聚合函数包括：Avg，Count，Max，Min，Sum，被定义在django.db.models中
    UserLogin.objects.aggregate(Sum('user_id'))


    return "hello"

if __name__ == '__main__':
    save_user()