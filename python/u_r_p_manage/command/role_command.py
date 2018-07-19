# -*- encoding:utf-8 -*-
import json
import traceback
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework import status
from u_r_p_manage import common


def create_role(request):
    """
    创建角色
    :param request:
    :return:
    """
    try:
        result = {}
        role_name = request.POST.get('rolename')
        if role_name is not None:
            query_data = Group.objects.filter(username=role_name)
            if query_data.exists():
                return common.ui_message_response(200, '角色名已经被占用', "角色名已经被占用", status.HTTP_200_OK)
            else:
                group = Group.objects.create(name=role_name)
                group.save()
                result['flag'] = "success"
                return common.ui_message_response(200, '角色创建成功', result, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '角色创建失败', '角色创建失败',
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)


def delete_role(request):
    """
    删除角色
    :param request:
    :return:
    """
    try:
        result = {}
        result['flag'] = "failure"
        role_id_list = request.POST.get('role_id_list')
        if role_id_list is not None:
            role_id_list = json.loads(role_id_list)
            for role_id in role_id_list:
                user_query = Group.objects.filter(id=role_id)
                for role in user_query:
                    role.delete()
                    result['flag'] = "success"
            return common.ui_message_response(200, '角色删除成功', result, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '角色删除失败', '角色删除失败',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def role_to_user(request):
    """
    角色添加用户
    :param request:
    :return:
    """
    result = {}
    result['flag'] = 'failure'
    role_name = request.get('role_name')
    user_name = request.get('username')
    group_select = Group.objects.filter(name=role_name)
    for group in group_select:
        user_select = User.objects.filter(username=user_name)
        for user in user_select:
            group.user_set.add(user)
            result['flag'] = 'success'

    return JsonResponse(result, safe=False)

def role_remove_user(request):
    """
    角色删除用户
    :param request:
    :return:
    """
    result = {}
    result['flag'] = "failure"
    role_name = request.get('role_name')
    user_name = request.get('username')
    group_select = Group.objects.filter(name=role_name)
    for group in group_select:
        user_select = User.objects.filter(username=user_name)
        for user in user_select:
            group.user_set.remove(user)
            result['flag'] = 'success'
    return JsonResponse(result, safe=False)


def role_remove_all_user(request):
    """
    角色删除所有用户
    :param request:
    :return:
    """
    result = {}
    result['flag'] = "failure"
    role_name = request.get('role_name')
    group_select = Group.objects.filter(name=role_name)
    for group in group_select:
        group.user_set.clear()
        result['flag'] = 'success'
    return JsonResponse(result, safe=False)


def role_query_all(request):
    """
    查询所有角色的信息
    :param request:
    :return:
    """
    result = {}
    role_list = []
    role_name = request.POST.get('role_name')
    request_data = common.print_header_data(request)
    start_pos, end_pos, page_size = common.get_page_data(request_data)
    if role_name is not None:
        query_terms = {}
        query_terms['name__contains'] = role_name
        query_role = Group.objects.filter(**query_terms)
    else:
        query_role = Group.objects.all()
    query_role = query_role.order_by('-id')
    role_count = query_role.count()
    for role in query_role:
        role_dict = {}
        role_dict['id'] = role.id
        role_dict['name'] = role.name
        role_list.append(role_dict)
    result['query_role'] = role_list[start_pos:end_pos]
    result['role_count'] = role_count

    return JsonResponse(result, safe=False)


def get_role_number(request):
    """
    获取角色数量
    :param request:
    :return:
    """
    try:
        result = {}
        query_result = Group.objects.all()
        role_count = query_result.count()
        result['role_count'] = role_count
        return common.ui_message_response(200, '查询成功', result, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)


def change_role_info(request):
    """
    修改角色信息
    :param request:
    :return:
    """
    try:
        role_id = request.POST.get('role_id')
        role_name = request.POST.get('role_name')
        if role_name is not None:
            query_data = Group.objects.filter(name=role_name)
            if query_data.exists():
                return common.ui_message_response(200, '角色名已经被占用', "角色名已经被占用", status.HTTP_200_OK)
            else:
                Group.objects.filter(id=role_id).update(name=role_name)
                return common.ui_message_response(200, '角色信息修改成功', '角色信息修改成功', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '角色信息修改失败', '角色信息修改失败',
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)