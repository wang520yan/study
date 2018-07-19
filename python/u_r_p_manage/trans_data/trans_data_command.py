# -*- encoding:utf-8 -*-

def trans_user_registration_info(request):
    """
    解析用户注册的信息。
    :param request:
    :return:
    """
    registration_info = {}
    registration_info['username'] = 'wangyan'
    registration_info['role_id'] = 1
    registration_info['node_id'] = 'C'
    print request.POST
    if 'user_name' in request.POST:
        registration_info['username'] = request.POST['user_name']
    if 'password' in request.POST:
        registration_info['password'] = request.POST['password']
    if 'email' in request.POST:
        registration_info['email'] = request.POST['email']
    if 'first_name' in request.POST:
        registration_info['first_name'] = request.POST['first_name']
    if 'last_name' in request.POST:
        registration_info['last_name'] = request.POST['last_name']
    if 'role_id' in request.POST:
        registration_info['role_id'] = request.POST['role_id']
    if 'node_id' in request.POST:
        registration_info['node_id'] = request.POST['node_id']
    return registration_info


def trans_user_authenticate_info(request):
    """
    authenticate模块校验用户,认证用户的密码是否有效, 若有效则返回代表该用户的user对象, 若无效则返回None。需要注意的是：该方法不检查is_active标志位。
    :param request_data:
    :return:
    """
    authenticate_info = {}
    if 'user_name' in request.POST:
        authenticate_info['username'] = request.POST['user_name']
    if 'password' in request.POST:
        authenticate_info['password'] = request.POST['password']

    return authenticate_info


def trans_user_change_password(request):
    """
    解析修改密码
    :param request_data:
    :return:
    """
    user_info = {}
    if 'user_name' in request.POST:
        user_info['username'] = request.POST['user_name']
    if 'old_password' in request.POST:
        user_info['old_password'] = request.POST['old_password']
    if 'new_password' in request.POST:
        user_info['new_password'] = request.POST['new_password']

    return user_info