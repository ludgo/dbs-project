import json

class Product:

	def __init__(self, product_id, code, ean, title, description):
		self.product_id = product_id
		self.code = code
		self.ean = ean
		self.title = title
		self.description = description

	@property
	def serialize(self):
		return {
			'product_id': self.product_id,
			'code': self.code,
			'ean': self.ean,
			'title': self.title,
			'description': self.description,
		}

class Subcategory:

	def __init__(self, subcategory_id, subcategory_name):
		self.subcategory_id = subcategory_id
		self.subcategory_name = subcategory_name

	@property
	def serialize(self):
		return {
			'subcategory_id': self.subcategory_id,
			'subcategory_name': self.subcategory_name
		}
