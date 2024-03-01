from flask import jsonify, request
from flask_bcrypt import generate_password_hash
from db import db
from models.users import Users, user_schema, users_schema
from util.reflection import populate_object


def add_user(req):
    post_data = request.form if request.form else request.json
    new_user = Users.get_new_user()
    populate_object(new_user, post_data)
    new_user.password = generate_password_hash(new_user.password).decode('utf8')
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create user'}), 400
    return jsonify({'message': 'user created', 'results': user_schema.dump(new_user)})


def get_all_users(req):
    try:
        all_users = db.session.query(Users).all()

        num_user = users_schema.dump(all_users)
        return jsonify({"message": 'success', 'results': num_user}), 200
    except:
        return jsonify({"message": "unable to pull users"}), 400
