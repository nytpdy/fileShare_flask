from tinydb import TinyDB, Query

# 创建数据库并插入数据
db = TinyDB('db.json')
db.insert({'name': 'John', 'age': 25})
db.insert({'name': 'Alice', 'age': 30})

# 查询数据
User = Query()
result = db.search(User)
print(result)
# result = db.search(User.name == 'John')
# print(result)
