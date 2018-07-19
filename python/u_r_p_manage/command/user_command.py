# -*- encoding:utf-8 -*-
import json
import sys
import traceback
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import JsonResponse
from u_r_p.models import User
from django.contrib import auth
from rest_framework import status
from u_r_p_manage import common
from trans_data.trans_data_command import trans_user_registration_info, trans_user_authenticate_info, \
    trans_user_change_password
reload(sys)
sys.setdefaultencoding('utf-8')

def user_registration(request):
    """
    注册用户信息，创建用户名和密码,auth模块不存储用户密码明文而是存储一个Hash值, 比如迭代使用Md5算法.
    :param request:
    :return:
    """
    result = {}
    user_data = trans_user_registration_info(request)
    if 'password' not in user_data:
        user_data['password'] = '123456'
    user_name = user_data['username']
    role_id = user_data['role_id']
    user_data['is_active'] = '1'
    user_data['is_staff'] = '1'
    del user_data['role_id']
    print user_data
    if user_data:
        query_data = User.objects.filter(username=user_name)
        if query_data.exists():
            return common.ui_message_response(200, '用户名已经被占用', "用户名已经被占用", status.HTTP_200_OK)
        else:
            user = User.objects.create_user(**user_data)
            user.save()
            print user
            user_select = User.objects.filter(username=user_name)
            for user in user_select:
                group_select = Group.objects.filter(id=role_id)
                try:
                    for group in group_select:
                        user.groups.add(group)
                        result['flag'] = "success"
                        return common.ui_message_response(200, '用户注册成功', result, status.HTTP_200_OK)
                except Exception:
                    traceback.print_exc()
                    return common.ui_message_response(500, '用户注册失败', '用户注册失败',
                                                      status.HTTP_500_INTERNAL_SERVER_ERROR)


def user_authenticate(request):
    """
    authenticate模块校验用户,认证用户的密码是否有效, 若有效则返回代表该用户的user对象, 若无效则返回None。需要注意的是：该方法不检查is_active标志位。
    :param request:
    :return:
    """
    result = {}
    user_data = trans_user_authenticate_info(request)
    user = authenticate(**user_data)
    if user:
        print user
        result['flag'] = "success"
    else:
        result['flag'] = "failure"
    return JsonResponse(result, safe=False)


def user_change_password(request):
    """
    修改用户密码
    :param request:
    :return:
    """
    try:
        result = {}
        user_data = {}
        request_data = trans_user_change_password(request)
        user_data['username'] = request_data['username']
        user_data['password'] = request_data['old_password']
        print user_data
        user = auth.authenticate(**user_data)
        if user is not None:
            user.set_password(request_data['new_password'])
            user.save()
            result['flag'] = "success"
            return common.ui_message_response(200, '修改密码成功', result, status.HTTP_200_OK)
        else:
            return common.ui_message_response(200, '修改密码失败', '原密码输入错误', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '修改密码失败', '修改密码失败',
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)


def user_login(request):
    """
    登录校验
    :param request:
    :return:
    """
    result = {}
    user_data = trans_user_authenticate_info(request)
    user = authenticate(**user_data)
    if user is not None:
        # if user.is_active:
        login(request, user)
        print user
        result['username'] = user_data['username']
        result['permission_id_list'] = [1,2,3]
        result['flag'] = "success"
    else:
        result['flag'] = "failure"
    return JsonResponse(result, safe=False)


def user_query_all(request):
    """
    检索账户信息
    :param request:
    :return:
    """
    role_id = request.POST.get('role_id')
    username = request.POST.get('user_name')
    result = {}
    user_list = []
    request_data = common.print_header_data(request)
    start_pos, end_pos, page_size = common.get_page_data(request_data)
    if username is not None:
        query_terms = {}
        query_terms['username__contains'] = username
        query_result = User.objects.filter(**query_terms)
    else:
        query_result = User.objects.all()
    if role_id is not None:
        user_result_list = []
        query_result = query_result.order_by('-id')
        for user in query_result:
            role_query = user.groups.all()
            for role in role_query:
                if role.id == int(role_id):
                    user_result_list.append(user)
        for user in user_result_list:
            user_dict = {}
            user_dict['user_id'] = user.id
            user_dict['username'] = user.username
            role_query = user.groups.all()
            if len(role_query) > 0:
                for role in role_query:
                    role_name = role.name
                    role_id = role.id
                    user_dict['role_name'] = str(role_name)
                    user_dict['role_id'] = int(str(role_id))
            user_list.append(user_dict)
        user_count = len(user_result_list)
    else:
        user_count = query_result.count()
        query_result = query_result.order_by('-id')
        for user in query_result:
            user_dict = {}
            user_dict['user_id'] = user.id
            user_dict['username'] = user.username
            role_query = user.groups.all()
            if len(role_query) > 0:
                for role in role_query:
                    role_name = role.name
                    role_id = role.id
                    user_dict['role_name'] = str(role_name)
                    user_dict['role_id'] = int(str(role_id))
            user_list.append(user_dict)
    result['user_query'] = user_list[start_pos:end_pos]
    result['user_count'] = user_count

    return JsonResponse(result, safe=False)


def get_user_number(request):
    """
    获取用户数量
    :param request:
    :return:
    """
    try:
        result = {}
        query_result = User.objects.all()
        user_count = query_result.count()
        result['user_count'] = user_count
        return common.ui_message_response(200, '查询成功', result, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)


def user_logout(request):
    """
    用户注销
    :param request:
    :return:
    """
    logout(request)


def user_to_role(request):
    """
    用户选择角色
    :param request:
    :return:
    """
    result = {}
    result['flag'] = "failure"
    user_name = request.get('username')
    role_name = request.get('rolename')
    user_select = User.objects.filter(username=user_name)
    for user in user_select:
        group_select = Group.objects.filter(name=role_name)
        for group in group_select:
            user.groups.add(group)
            result['flag'] = "success"
    return JsonResponse(result, safe=False)


def user_remove_role(request):
    """
    用户退出角色选择
    :param request:
    :return:
    """
    result = {}
    result['flag'] = "failure"
    user_name = request.get('username')
    role_name = request.get('rolename')
    user_select = User.objects.filter(username=user_name)
    for user in user_select:
        group_select = Group.objects.filter(name=role_name)
        for group in group_select:
            user.groups.remove(group)
            result['flag'] = "success"
    return JsonResponse(result, safe=False)


def user_remove_all(request):
    """
    用户退出所有角色
    :param request:
    :return:
    """
    result = {}
    result['flag'] = "failure"
    user_name = request.get('username')
    user_select = User.objects.filter(username=user_name)
    for user in user_select:
        user.groups.clear()
        result['flag'] = "success"
    return JsonResponse(result, safe=False)


def delete_user(request):
    """
    根据用户id删除用户信息
    :param request:
    :return:
    """
    try:
        result = {}
        if 'user_id_list' in request.POST:
            user_id_list = request.POST['user_id_list']
            user_id_list = json.loads(user_id_list)
            for user_id in user_id_list:
                user_query = User.objects.filter(id=user_id)
                for user in user_query:
                    user.delete()
                    result['flag'] = "success"
        return common.ui_message_response(200, '用户删除成功', result, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '用户删除失败', '用户删除失败',
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)


def change_user_info(request):
    """
    修改用户信息
    :param request:
    :return:
    """
    result = {}
    user_id = request.POST.get('user_id')
    user_name = request.POST.get('user_name')
    role_id = request.POST.get('role_id')
    if user_id is not None:
        try:
            User.objects.filter(id=user_id).update(username=user_name)
            user_query = User.objects.filter(username=user_name)
            if user_query:
                for user in user_query:
                    if user.groups.all():
                        user.groups.clear()
                    user_choice_role(user_name, role_id)
                    result['flag'] = "success"
                    return common.ui_message_response(200, '用户信息修改成功', result, status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                              status.HTTP_500_INTERNAL_SERVER_ERROR)


def user_choice_role(user_name,role_id):
    """
    用户选择角色
    :param user_name:
    :param role_id:
    :return:
    """
    result = {}
    user_select = User.objects.filter(username=user_name)
    for user in user_select:
        group_select = Group.objects.filter(id=role_id)
        for group in group_select:
            user.groups.add(group)
            result['flag'] = "success"
    return result
