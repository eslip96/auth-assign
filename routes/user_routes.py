from flask import Blueprint, request, jsonify

import controllers

users = Blueprint('users', __name__)


@users.route('/user', methods=['POST'])
def add_user():
    return controllers.add_user(request)


@users.route('/users', methods=['GET'])
def get_users():
    return controllers.get_all_users(request)
