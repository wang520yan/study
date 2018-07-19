# -*- encoding:utf-8 -*-
import json
import traceback
from time import timezone
from django.contrib.auth.models import User, Group, Permission
from django.http import JsonResponse
from rest_framework import status
from u_r_p_manage import common

def user_query_permission(request):
    """
    用户查询权限
    :param request:
    :return:
    """
    result = {}
    result['flag'] = 'failure'
    user_name = request.get('username')
    user_select = User.objects.filter(username=user_name)
    for user in user_select:
        # result = user.has_perm('add_logentry')
        query_result = user.get_all_permissions()
        print query_result
        result['flag'] = 'success'
        result['query_result'] = list(query_result)
    return JsonResponse(result, safe=False)


def group_query_permission(request):
    """
    角色查询权限
    :param request:
    :return:
    """
    result = {}
    permission_result = {}
    content_type_id_list = []
    query_result_list_button = []
    query_result_list = {}
    role_id = request.POST.get('role_id')
    role_select = Group.objects.filter(id=role_id)
    for group in role_select:
        query_result = group.permissions.all()
        for permission in query_result:
            content_type_id_list.append(permission.content_type_id)
        content_type_id_list = list(set(content_type_id_list))
        for content_type_id in content_type_id_list:
            for permission in query_result:
                query_result_dict_button = {}
                query_result_dict_menu = {}
                if permission.content_type_id == content_type_id:
                    codename_list = permission.codename.split('|')
                    print codename_list[-1]
                    if codename_list[-1] == 'menu':
                        query_result_dict_menu['id'] = permission.id
                        query_result_dict_menu['name'] = permission.name
                        query_result_dict_menu['content_type_id'] = permission.content_type_id
                        query_result_list['menu'] = query_result_dict_menu
                    if codename_list[-1] == 'button':
                        query_result_dict_button['id'] = permission.id
                        query_result_dict_button['name'] = permission.name
                        query_result_dict_button['content_type_id'] = permission.content_type_id
                        query_result_list_button.append(query_result_dict_button)
                        query_result_list['button'] = query_result_list_button
                        permission_result[permission.content_type_id] = query_result_list
                        result['all_permissions'] = permission_result
    return JsonResponse(result, safe=False)


def role_add_permission(request):
    """
    角色增加权限
    :param request:
    :return:
    """
    result = {}
    result['flag'] = 'failure'
    role_id = request.POST.get('role_id')
    permission_id_list = request.POST.get('permission_id_list')
    role_select = Group.objects.filter(id=role_id)
    for group in role_select:
        try:
            if permission_id_list:
                permission_id_list = json.loads(permission_id_list)
                if group.permissions.all():
                    group.permissions.clear()
                    for permission_id in permission_id_list:
                        group.permissions.add(permission_id)
                        result['flag'] = 'success'
                    return common.ui_message_response(200, '角色添加权限成功', result, status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return common.ui_message_response(500, '角色添加权限失败', '角色添加权限失败',
                                              status.HTTP_500_INTERNAL_SERVER_ERROR)



def role_delete_permission(request):
    """
    角色删除权限
    :param request:
    :return:
    """
    result = {}
    result['flag'] = 'failure'
    role_name = request.get('role_name')
    permission_id = request.get('permission_id')
    role_select = Group.objects.filter(name=role_name)
    for group in role_select:
        group.permissions.remove(permission_id)
        result['flag'] = 'success'
    return JsonResponse(result, safe=False)


def role_delete_all_permission(request):
    """
    角色删除全部权限
    :param request:
    :return:
    """
    result = {}
    result['flag'] = 'failure'
    role_name = request.get('role_name')
    role_select = Group.objects.filter(name=role_name)
    for group in role_select:
        group.permissions.clear()
        result['flag'] = 'success'
    return JsonResponse(result, safe=False)


def query_all_permissions(request):
    """
    查询全部权限
    :param request:
    :return:
    """
    result = {}
    permission_result = {}
    content_type_id_list = []
    query_result_list_button = []
    query_result_list = {}
    query_result = Permission.objects.all()
    for permission in query_result:
        content_type_id_list.append(permission.content_type_id)
    content_type_id_list = list(set(content_type_id_list))
    for content_type_id in content_type_id_list:
        for permission in query_result:
            query_result_dict_button = {}
            query_result_dict_menu = {}
            if permission.content_type_id == content_type_id:
                codename_list = permission.codename.split('|')
                print codename_list[-1]
                if codename_list[-1] == 'menu':
                    query_result_dict_menu['id'] = permission.id
                    query_result_dict_menu['name'] = permission.name
                    query_result_dict_menu['content_type_id'] = permission.content_type_id
                    query_result_list['menu'] = query_result_dict_menu
                if codename_list[-1] == 'button':
                    query_result_dict_button['id'] = permission.id
                    query_result_dict_button['name'] = permission.name
                    query_result_dict_button['content_type_id'] = permission.content_type_id
                    query_result_list_button.append(query_result_dict_button)
                    query_result_list['button'] = query_result_list_button
                    permission_result[permission.content_type_id] = query_result_list
                    result['all_permissions'] = permission_result
    return JsonResponse(result, safe=False)


def get_permission_number(request):
    """
    获取权限数量
    :param request:
    :return:
    """
    try:
        result = {}
        query_result = Permission.objects.all()
        permission_count = query_result.count()
        result['permission_count'] = permission_count
        return common.ui_message_response(200, '查询成功', result, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)















if __name__ == '__main__':
    pass

