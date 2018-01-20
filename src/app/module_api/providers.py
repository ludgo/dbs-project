from app.providers import PostgreSqlProvider
from app.module_api.models import Product, Subcategory
from app.module_api.constants import *


# database query provider serving to api route calls
class ApiProvider(PostgreSqlProvider):

	# get single product with specified code
	def searchProductByCode(self, code):

		row_match_code = self.engine.execute(SELECT_PRODUCT_BY_CODE, code=code).fetchone()

		match_product = None
		if row_match_code:
			product_id, code, ean, title, description = row_match_code
			match_product = Product(product_id, code, ean, title, description)

		return match_product

	# get limited number of products with specified title ignore-case match
	def searchProductByTitle(self, title, subcategory_id):

		expr_title = '%%{}%%'.format(title)
		rows_match_title = self.engine.execute(SELECT_PRODUCT_BY_TITLE, expr_title=expr_title, subcategory_id=subcategory_id).fetchall()

		match_products = []
		if rows_match_title:
			for product_id, code, ean, title, description in rows_match_title:
				match_products.append( Product(product_id, code, ean, title, description) )
		
		return match_products

	# get all subcategories for particular category
	def getSubcategory(self, category_id):

		rows_subcategory = self.engine.execute(SELECT_SUBCATEGORY_BY_CATEGORY, category_id=category_id).fetchall()

		subcategories = []
		for subcategory_id, subcategory_name in rows_subcategory:
			subcategories.append( Subcategory(subcategory_id, subcategory_name) )
		return subcategories

