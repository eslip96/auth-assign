from flask import jsonify
from db import db
from models import *
from models.category import category_schema, categories_schema
from util.reflection import populate_object
from lib.authenicate import *


@auth_admin
def create_category(req):
    post_data = req.form if req.form else req.get_json()
    new_category = Categories.new_category_obj()
    populate_object(new_category, post_data)

    try:
        db.session.add(new_category)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "failed to create category."}), 400
    return jsonify({'message': 'category created', 'results': category_schema.dump(new_category)}), 201


@auth
def get_all_categories(req):
    categories = db.session.query(Categories).all()
    try:
        if not categories:
            return jsonify({"message": "no categories in database"}), 404
    except:
        return jsonify({"message": "failed to retrive categories"}), 400
    return jsonify({"message": "current categories avaliable", "results": categories_schema.dump(categories)}), 201


@auth_admin
def update_category(req, category_id):
    post_data = req.form if req.form else req.json
    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    try:
        if not category:
            return jsonify({"message": "category not found"}), 404
        if 'category_name' in post_data:
            category.category_name = post_data['category_name']

        db.session.commit()

        return jsonify({"message": "category updated!", "result": category_schema.dump(category)}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "failed to update category."}), 400


@auth
def get_category_by_id(req, category_id):
    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    try:
        if not category:
            return jsonify({"message": "no category found with id"}), 404
    except:
        return jsonify({"message": "failed to retrieve category"}), 400
    return jsonify({"message": "product requested", "result": category_schema.dump(category)}), 200


@auth_admin
def delete_category(req, category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({'message': "no category found category id"}), 404

    try:
        db.session.query(products_categories_association_table).filter(products_categories_association_table.c.category_id == category_id).delete
        db.session.delete(category_query)
        db.session.commit()
        return jsonify({'message': 'category has been deleted'}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete category"}), 400
