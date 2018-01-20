class Inquiry:

	def __init__(self, inquiry_id, time_issued, time_responded, email):
		self.inquiry_id = inquiry_id
		self.time_issued = time_issued
		self.time_responded = time_responded
		self.email = email

class InquiryListItem(Inquiry):

	def __init__(self, inquiry_id, time_issued, time_responded, email, items_count, total_sum):
		Inquiry.__init__(self, inquiry_id, time_issued, time_responded, email)
		self.items_count = items_count
		self.total_sum = total_sum

class InquiryItem:

	def __init__(self, item_id, item_amount, item_price, product_code, product_title, product_price):
		self.item_id = item_id
		self.item_amount = item_amount
		self.item_price = item_price
		self.product_code = product_code
		self.product_title = product_title
		self.product_price = product_price

	@property
	def serialize(self):
		return {
			'item_id': self.item_id,
			'item_amount': self.item_amount,
			'item_price': float(self.item_price),
			'product_code': self.product_code,
			'product_title': self.product_title,
			'product_price': float(self.product_price)
		}

class InquiryWithItems(Inquiry):

	def __init__(self, inquiry_id, time_issued, time_responded, email, items):
		Inquiry.__init__(self, inquiry_id, time_issued, time_responded, email)
		self.items = items

	@property
	def amount_sum(self):
		return sum(item.item_amount for item in self.items)

	@property
	def price_sum(self):
		return sum(item.item_amount * item.item_price for item in self.items)

	@property
	def serialize(self):
		return {
			'inquiry_id': self.inquiry_id,
			'time_issued': str(self.time_issued),
			'time_responded': str(self.time_responded),
			'email': self.email,
			'items': [i.serialize for i in self.items]
		}

class Category:

	def __init__(self, category_id, category_name):
		self.category_id = category_id
		self.category_name = category_name
