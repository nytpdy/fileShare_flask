# 用户操作，对users.json的操作
# 文件格式
# {
#     users:[
#         {id:id, username:username, password:password, permissions:permissions},
#         {id:id, username:username, password:password, permissions:permissions}
#     ]
# }
# ----------------------------------------------------------------------------------------
from flask_login import UserMixin
import json


class User(UserMixin):
    pass


with open(r'E:\FileSrc\users.json', 'r') as load_f:
    users = json.load(load_f)


# 查找用户
def query_user(user_id):
    for user in users['users']:
        if user_id == user['id']:
            return user


# 添加用户
def add_user(id, username, password):
    dic = {
        'id': id,
        'username': username,
        'password': password,
        'permissions': 0
    }
    users['users'].append(dic)


# 删除用户
def delete_user(id):
    user = query_user(id)
    users['users'].remove(user)


# 添加json字段
def add_field():
    for i, user in enumerate(users['users']):
        users['users'][i]['permissions'] = 0


# 修改信息(信息几乎固定，不用修改，延缓)
# def update_user(id)


# 执行到文件
def doit():
    with open('users.json', 'w') as f:
        json.dump(users, f)


if __name__ == '__main__':
    # print(users)
    # print(users['users'])
    # print(users['users'][0])
    # print(users['users'][0]['id'])

    for user in users['users']:
        print(user)
