from flask import jsonify, request
from db import db
from models.company import *
from models.company import company_schema, companies_schema, Companies
from models.product import product_schema, products_schema, Products
from models.product_category_xref import *
from util.reflection import populate_object
from models.product_category_xref import *
from lib.authenicate import *


@auth_admin
def add_company(req):
    post_data = req.form if req.form else req.json
    new_company = Companies.new_company_obj()
    populate_object(new_company, post_data)
    try:
        db.session.add(new_company)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create company"}), 400

    return jsonify({"message": "company created", "result": company_schema.dump(new_company)}), 201


@auth
def get_all_companies(req):
    try:
        companies = db.session.query(Companies).all()
        if not companies:
            return jsonify({"message": "no companies found"}), 404

        return jsonify({"message": "current companies in database", "results": companies_schema.dump(companies)}), 200
    except:
        return jsonify({"message": "failed to retrieve companies"}), 400


@auth_admin
def update_company(req, company_id):
    post_data = req.form if req.form else req.json

    try:
        company = db.session.query(Companies).filter(Companies.company_id == company_id).first()
        if not company:
            return jsonify({"message": "Company not found"}), 404

        if 'company_name' in post_data:
            company.company_name = post_data['company_name']

        db.session.commit()

        return jsonify({"message": "company updated successfully", "result": company_schema.dump(company)}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "failed to update company."}), 400


@auth
def get_company_by_id(req, company_id):
    company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    try:
        if not company:
            return jsonify({"message": "no company in database"}), 404
    except:
        return jsonify({"message": "failed to retrive company"}), 400
    return jsonify({"message": "company requested", "result": company_schema.dump(company)}), 200


@auth_admin
def delete_company(req, company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "no company found with the given company id"}), 404

    try:
        delete_company_result = product_schema.dump(company_query)

        db.session.query(products_categories_association_table).filter(products_categories_association_table.c.product_id == company_id).delete()

        db.session.query(Products).filter(Products.company_id == company_id).delete()
        db.session.delete(company_query)
        db.session.commit()

        return jsonify({"message": "company and any associated products have been deleted", "deleted company": delete_company_result}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "failed to delete company"}), 400
