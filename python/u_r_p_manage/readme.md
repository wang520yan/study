1.运行项目前必须执行建表操作，首先在mysql中创建名为django_mysql的数据库，之后在u_r_p_manage目录下执行命令python manage.py makemigrations
和python manage.py migrate，此时将会在新创建的数据库中创建表。
2.执行创建用户命令：
python manage.py createsuperuser
# 按照提示输入用户名和对应的密码就好了邮箱可以留空，用户名和密码必填
# 修改 用户密码可以用：
python manage.py changepassword username
此时数据库中user表中将存储注册的账户信息。
3.在该项目中并未对角色表和权限表做继承扩展，读者可以根据自己需要将数据表进行扩展，存储自己的数据。
