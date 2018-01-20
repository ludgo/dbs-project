from flask import Blueprint, request, jsonify

from app.module_api.providers import ApiProvider
from app import engine

# JSON API
blueprint_api = Blueprint('api', __name__, url_prefix='/api')

api_provider = ApiProvider(engine)

# GET search product by code
@blueprint_api.route('/_search_by_code')
def _search_by_code():
	code = request.args.get('phrase_code', '', type=str)
	found_product = api_provider.searchProductByCode(code)
	body = None
	if found_product:
		body = found_product.serialize
	return jsonify(result=body)

# GET search product by title match
@blueprint_api.route('/_search_by_title')
def _search_by_title():
	title = request.args.get('phrase_title', '', type=str)
	subcategory_id = request.args.get('subcategory_id', '', type=str)
	found_products = api_provider.searchProductByTitle(title, subcategory_id)
	body = [found_product.serialize for found_product in found_products]
	return jsonify(result=body)

# GET subcategories by category
@blueprint_api.route('/_subcategory_by_category')
def _subcategory_by_category():
	category_id = request.args.get('category_id', '', type=str)
	subcategories = api_provider.getSubcategory(category_id)
	body = [subcategory.serialize for subcategory in subcategories]
	return jsonify(result=body)

