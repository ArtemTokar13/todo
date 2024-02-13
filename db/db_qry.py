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