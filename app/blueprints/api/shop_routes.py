from . import bp as api
from .models import Item, Category, Category
from app.blueprints.auth.auth import token_auth
from flask import request, make_response, g

###########################################################
################# CATEGORY API ROUTES #####################
###########################################################

# Get all categories
@api.get('/category')
@token_auth.login_required()
def get_category():
    cats = Category.query.all()
    cats_dicts = [cat.to_dict() for cat in cats]
    return make_response({"categories":cats_dicts},200)

# Create a new cateogry
@api.post('/category')
@token_auth.login_required()
def post_category():
    if not g.current_user.is_admin:
        return make_response("You are not an Admin", 403)
    cat_name = request.get_json().get('name')
    cat = Category(name = cat_name)
    cat.save()
    return make_response(f'Category {cat.id} with name {cat.name} created', 200)

# Change category
@api.patch('/category')
@token_auth.login_required()
def patch_category():
    if not g.current_user.is_admin:
        return make_response("You are not an Admin", 403)
    cat_name = request.get_json().get('name')
    cat_id = request.get_json().get('id')
    if not cat_name or not cat_id:
        return make_response("Invalid payload", 400)
    cat = Category.query.get(cat_id)
    if cat is None:
        return make_response("Invalid category ID", 400)
    cat.name = cat_name
    cat.save()
    return make_response(f"Category {cat.id}'s name has been changed to {cat.name}")

#Delete a category
@api.delete('/category')
@token_auth.login_required()
def del_category():
    if not g.current_user.is_admin:
        return make_response("You are not an Admin", 403)
    cat_id = request.get_json().get('id')
    if not cat_id:
        return make_response("Invalid payload", 400)
    cat = Category.query.get(cat_id)
    if cat is None:
        return make_response("Invalid category ID", 400)
    cat_id = cat.id
    cat.delete()
    return make_response(f"Category {cat_id} has been deleted", 200)

###########################################################
#################### ITEM API ROUTES ######################
###########################################################

# Look up a specific item by its id
@api.get("/item")
@token_auth.login_required()
def get_item():
    id = request.get_json().get('id')
    if not id:
        return make_response("Invalid Payload",400)
    item = Item.query.get(id)
    if item is None:
        return make_response("Invalid item id", 400)
    return make_response(item.to_dict(),200)

## Look up all Items
@api.get("/all_items")
@token_auth.login_required()
def get_all_items():
    all_items = Item.query.all()
    items = [item.to_dict() for item in all_items]
    return make_response({"items":items},200)

## Look Up all Items in a category
@api.get("/items_by_category_id")
@token_auth.login_required()
def items_by_category_id():
    id = request.get_json().get('id') #category id
    if not id:
        return make_response("Invalid Payload",400)
    all_items = Item.query.filter_by(category_id=id).all()
    items = [item.to_dict() for item in all_items]
    return make_response({"items":items},200)

# This will create a new ITEM
    # name   # description   # price   # img   # category_id
@api.post("/item")
@token_auth.login_required()
def post_item():
    if not g.current_user.is_admin:
        return make_response("You Are not Admin",403)
    item_dict = request.get_json()
    if not all(key in item_dict for key in ('name','description','price','img','category_id')):
        return make_response("Invalid Payload",400)
    item = Item(**item_dict)
    item.save()
    return make_response(f"Item {item.name} was created with the id {item.id}",201)

# This will alter the item by looking up from its id
@api.patch("/item")
@token_auth.login_required()
def patch_item():
    if not g.current_user.is_admin:
        return make_response("You Are not Admin",403)
    item_dict = request.get_json()
    if not item_dict.get('id'):
        return make_response("Invalid Payload",400)
    item = Item.query.get(item_dict['id'])
    item.from_dict(item_dict)
    item.save()
    return make_response(f'Item {item.id} was edited', 200)

# This will delete an Item by its id
@api.delete("/item")
@token_auth.login_required()
def delete_item():
    if not g.current_user.is_admin:
        return make_response("You Are not Admin",403)
    id = request.get_json().get('id')
    if not id:
        return make_response("Invalid Payload",400)
    item_to_delete = Item.query.get(id)
    if item_to_delete is None:
        return make_response("Invalid item id", 400)
    item_to_delete.delete()
    return make_response(f"Item id {id} has been deleted")

