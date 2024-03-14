from flask import jsonify, request
from db import db
from models import *
from models.product import product_schema, products_schema
from util.reflection import populate_object
from lib.authenicate import *


@auth_admin
def add_product(req):
    post_data = req.form if req.form else req.json
    new_product = Products.new_product_obj()
    populate_object(new_product, post_data)

    try:
        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "failed to create product."}), 400
    return jsonify({'message': 'product created', 'result': product_schema.dump(new_product)}), 201


@auth
def get_all_products(req):
    try:
        products = db.session.query(Products).all()
        if not products:
            return jsonify({"message": "no products"}), 404
        return jsonify({"message": "current product in database", "results": products_schema.dump(products)}), 201
    except:
        return jsonify({"message": "failed to retrieve products"}), 400


@auth
def get_active_products(req):
    try:
        active_products = db.session.query(Products).filter(Products.active == True).all()
        if not active_products:
            return jsonify({"message": "no active products"}), 400
        return jsonify({"message": "active products in database", "results": products_schema.dump(active_products)}), 201
    except:
        return jsonify({"message": "failed to retrieve active products"}), 400


@auth
def get_product_by_id(req, product_id):
    prods = db.session.query(Products).filter(Products.product_id == product_id).first()

    try:
        if not prods:
            return jsonify({"message": "no products in database"}), 404
    except:
        return jsonify({"message": "failed to retrieve product"}), 400
    return jsonify({"message": "product requested", "result": product_schema.dump(prods)}), 200


@auth_admin
def update_product(req, product_id):
    try:
        post_data = req.form if req.form else req.json
        product = db.session.query(Products).filter(Products.product_id == product_id).first()
        if not product:
            return jsonify({"message": "Product not found"}), 404
        if 'product_name' in post_data:
            product.product_name = post_data['product_name']
        if 'description' in post_data:
            product.description = post_data['description']
        if 'price' in post_data:
            product.price = post_data['price']
        if 'active' in post_data:
            product.active = post_data['active']

        db.session.commit()
        return ({"message": "product updated", "result": product_schema.dump(product)}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "failed to update product"}), 400


@auth
def add_product_to_category(req):
    post_data = req.json
    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    if not product_id or not category_id:
        return jsonify({'message': 'both product id and category id are required.'}), 400

    product = Products.query.get(product_id)
    category = Categories.query.get(category_id)

    if not product or not category:
        return jsonify({'message': 'product or category not found.'}), 404

    if category in product.categories:
        return jsonify({'message': 'product is already associated with the category.'}), 400

    product.categories.append(category)

    try:
        db.session.commit()
        num_product = product_schema.dump(product)
        num_category = category_schema.dump(category)

        return jsonify({'message': 'product added to category successfully.',
                        'product': num_product,
                        'category': num_category}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'failed to add product to category.'}), 400


@auth
def get_products_by_company_id(req, company_id):
    try:
        products = db.session.query(Products).filter(Products.company_id == company_id).all()
        if not products:
            return jsonify({"message": "no products found for the given company id."}), 404
        return jsonify({"message": "products retrieved successfully.", "results": products_schema.dump(products)}), 200
    except:
        return jsonify({"message": "failed to retrieve products"}), 400


@auth_admin
def delete_product(req, product_id):
    try:
        product_to_delete = Products.query.get(product_id)

        if product_to_delete is None:
            return jsonify({'message': 'product not found'}), 404

        db.session.query(products_categories_association_table).filter(products_categories_association_table.c.product_id == product_id).delete()
        db.session.delete(product_to_delete)
        db.session.commit()

        return jsonify({'message': 'product deleted successfully'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to delete product'}), 400
