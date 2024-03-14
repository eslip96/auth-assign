from flask import jsonify, request
from flask_bcrypt import generate_password_hash
from db import db
from models.users import Users, user_schema, users_schema
from models.product import products_categories_association_table
from models.product import *
from util.reflection import populate_object
from lib.authenicate import *


def add_user(req):
    post_data = request.form if request.form else request.json
    new_user = Users.get_new_user()
    populate_object(new_user, post_data)
    if 'password' not in post_data or not isinstance(post_data['password'], str):
        return jsonify({'message': 'password is required thats not numbers and must be in qoutes'}), 400

    new_user.password = generate_password_hash(post_data['password']).decode('utf8')
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create user'}), 400
    return jsonify({'message': 'user created', 'result': user_schema.dump(new_user)})


@auth
def get_all_users(req):
    try:
        all_users = db.session.query(Users).all()

        num_user = users_schema.dump(all_users)
        return jsonify({"message": 'success', 'results': num_user}), 200
    except:
        return jsonify({"message": "unable to pull users"}), 400


@auth_admin
def delete_user(request, user_id):
    if not validate_token(request):
        return jsonify({'message': 'invalid token'}), 401

    try:
        user_to_delete = Users.query.get(user_id)

        if user_to_delete is None:
            return jsonify({'message': 'user not found'}), 404

        db.session.delete(user_to_delete)
        db.session.commit()

        return jsonify({'message': 'user deleted successfully'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to delete user'}), 400
