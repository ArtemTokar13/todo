from bson.objectid import ObjectId


def todos(db):
    cursor = db.todos.find()
    todo_list = []
    for document in cursor:
        document['_id'] = str(document['_id'])
        todo_list.append(document)
    return todo_list

def todo(db, id):
    res = db.todos.find_one({'_id': ObjectId(id)})
    if res is not None:
        res['_id'] = str(res['_id'])
    return res

def users(db):
    cursor = db.users.find()
    user_list = []
    for document in cursor:
        document['_id'] = str(document['_id'])
        user_list.append(document)
    return user_list

def user(db, id):
    res = db.users.find_one({'_id': ObjectId(id)})
    if res is not None:
        res['_id'] = str(res['_id'])
    return res

def categories(db):
    cursor = db.categories.find()
    category_list = []
    for document in cursor:
        document['_id'] = str(document['_id'])
        category_list.append(document)
    return category_list

def category(db, id):
    res = db.categories.find_one({'_id': ObjectId(id)})
    if res is not None:
        res['_id'] = str(res['_id'])
    return res