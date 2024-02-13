from bson.objectid import ObjectId


def create_task(db, task):
    task = dict(task)
    db.todos.insert_one(task)

def update_task(db, id, task):
    task = dict(task)
    res = db.todos.update_one({'_id': ObjectId(id)}, {'$set': task})
    return res.modified_count 

def update_status(db, id, status):
    db.todos.update_one({'_id': ObjectId(id)}, {'$set': {'is_active': not status}})

def delete_task(db, id):
    res = db.todos.delete_one({'_id': ObjectId(id)})
    return res.deleted_count