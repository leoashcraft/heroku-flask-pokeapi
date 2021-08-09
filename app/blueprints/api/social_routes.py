from . import bp as api
from app.blueprints.social.models import Post
from app.blueprints.auth.models import User
from flask import make_response, request, g
from app.blueprints.auth.auth import token_auth

# Route to show all of the posts in our database
@api.get('/all_posts') #same as above
@token_auth.login_required()
def get_all_posts():
    user = g.current_user
    posts = user.followed_posts()
    response_list=[]
    for post in posts:
        post_dict={
            "id":post.id,
            "body":post.body,
            "date_created":post.date_created,
            "date_updated":post.date_updated,
            "author":post.author.first_name + ' ' + post.author.last_name,
            "author_id": post.author.id
        }
        response_list.append(post_dict)
    return make_response({"post":response_list},200)

# Return a single post by id
@api.get('/posts')
@token_auth.login_required()
def get_post_api():
    user = g.current_user
    data_from_request=request.get_json()
    post = Post.query.get(data_from_request['id'])
    #Does user have access to post?
    if not user.is_following(post.author) and not post.author.id == user.id:
        return make_response("Cannot view post for user. You're not a follower of this user.", 403)
        
    if not post:
        return make_response(f"Post id: {data_from_request['id']} does not exist", 404)
    response_dict={
        "id": post.id,
        "body": post.body,
        "date_created": post.date_created,
        "date_updated": post.date_updated,
        "author": post.author.first_name + ' ' + post.author.last_name,
        "author_id": post.author.id
    }
    return make_response(response_dict, 201)

# POST -- Create a new post
@api.post('/posts')
@token_auth.login_required()
def post_post_api():
    user = g.current_user
    posted_data = request.get_json()
    post_user = User.query.get(posted_data['user_id'])
    if not post_user:
        return make_response(f"User id: {posted_data['user_id']} does not exist", 404)
    if user.id != post_user.id:
        return make_response("You can only post as yourself.", 403)
    post = Post(**posted_data)
    post.save()
    return make_response(f"Post id: {post.id} created!", 201)

# PUT -- Replace the old post with a new post
@api.put('/posts')
@token_auth.login_required()
def put_post_api():
    user = g.current_user
    posted_data = request.get_json()
    post_user = User.query.get(posted_data['user_id'])
    if not post_user:
        return make_response(f"User id: {posted_data['user_id']} does not exist", 404)
    if user.id != post_user.id:
        return make_response("You can only put your own posts.", 403)
    post = Post.query.get(posted_data['id'])
    if not post:
        return make_response(f"Post id: {posted_data['id']} does not exist", 404)
    post.user_id=posted_data['user_id']
    post.body=posted_data['body']
    post.save()
    return make_response(f"Post id: {post.id} has been updated", 200)

# PATCH -- This will update our post with new info
@api.patch('/posts')
@token_auth.login_required()
def patch_post_api():
    user = g.current_user
    posted_data = request.get_json()
    if posted_data.get('user_id'):
        post_user = User.query.get(posted_data['user_id'])
        if not user:
            return make_response(f"User id: {posted_data['user_id']} does not exist", 404)
        if user.id != post_user.id:
            return make_response("You can only patch your own posts.", 403)
    post = Post.query.get(posted_data['id'])
    if not post:
        return make_response(f"Post id: {posted_data['id']} does not exist", 404)
    post.user_id = posted_data['user_id'] if posted_data.get('user_id') and posted_data['user_id']!= post.user_id else post.user_id
    post.body=posted_data['body'] if posted_data.get('body') and posted_data['body'] != post.body else post.body
    post.save()
    return make_response(f"Post id: {post.id} has been updated", 200)

# DELETE -- this will delete a post
@api.delete('/posts')
@token_auth.login_required()
def delete_post_api():
    user = g.current_user
    posted_data = request.get_json()
    post = Post.query.get(posted_data['id'])
    if not user.id == post.user_id:
        return make_response("You can only delete your own posts.", 403)
    if not post:
        return make_response(f"Post id: {posted_data['id']} does not exist", 404)
    #won't have access to post after deleted so creating variable
    p_id=post.id
    post.delete()
    return make_response(f"Post id: {p_id} has been deleted", 200)