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

def create_user(db, user):
    user = dict(user)
    db.users.insert_one(user)

def update_user(db, id, user):
    user = dict(user)
    res = db.users.update_one({'_id': ObjectId(id)}, {'$set': user})
    return res.modified_count 

def delete_user(db, id):
    res = db.users.delete_one({'_id': ObjectId(id)})
    return res.deleted_count

def create_category(db, category):
    category = dict(category)
    db.categories.insert_one(category)

def update_category(db, id, category):
    category = dict(category)
    res = db.categories.update_one({'_id': ObjectId(id)}, {'$set': category})
    return res.modified_count 

def delete_category(db, id):
    res = db.categories.delete_one({'_id': ObjectId(id)})
    return res.deleted_count