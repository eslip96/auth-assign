from flask import Blueprint, request, jsonify

import controllers

products= Blueprint('products', __name__)

@products.route('/product', methods=['POST'])
def add_product():
    return controllers.add_product(request)

@products.route('/products', methods=['GET'])
def get_all_products():
    return controllers.get_all_products(request)

@products.route('/product/active', methods=['GET'])
def get_active_products():
    return controllers.get_active_products(request)

@products.route('/product/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    return controllers.get_product_by_id(request,product_id)

@products.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    return controllers.update_product(request, product_id)

@products.route('/product', methods=['PUT'])
def add_product_to_category():
    return controllers.add_product_to_category(request)


@products.route('/products/company/<company_id>', methods=['GET'])
def get_products_by_company_id(company_id):
    return controllers.get_products_by_company_id(request,company_id)

@products.route('/product/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    return controllers.delete_product(product_id)