from flask import Blueprint, request, jsonify

import controllers

companies = Blueprint('companies', __name__)


@companies.route('/company', methods=['POST'])
def add_company():
    return controllers.add_company(request)


@companies.route('/companies', methods=['GET'])
def get_all_companies():
    return controllers.get_all_companies(request)


@companies.route('/company/<company_id>', methods=['PUT'])
def update_company(company_id):
    return controllers.update_company(request, company_id)


@companies.route('/company/<company_id>', methods=['GET'])
def get_company_by_id(company_id):
    return controllers.get_company_by_id(request, company_id)


@companies.route('/company/delete/<company_id>', methods=['DELETE'])
def delete_company(company_id):
    return controllers.delete_company(request, company_id)
