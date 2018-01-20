from app.providers import PostgreSqlProvider
from app.module_inquiries.models import InquiryListItem, InquiryWithItems, InquiryItem, Category
from app.module_inquiries.constants import *


# database query provider serving to application front-end route calls
class InquiryProvider(PostgreSqlProvider):

	# get page-sized inquiries sorted by descending create time based on eventual parameters
	def getInquiries(self, page, per_page, not_responded, min_total_price):

		inquiries = []
		
		if page < 1:
			return inquiries
		if per_page < 1 or per_page > 100:
			per_page = 20
		not_responded = not_responded and True

		offset = (page-1) * per_page

		if min_total_price > 50000:
			# choice from responded inquiries only
			# page size or less
			rows_inquiries = self.engine.execute(SELECT_INQUIRIES_LIST_MIN_TOTAL_PRICE_BIG, limit=per_page, offset=offset, minTotalPrice=min_total_price).fetchall()
		elif min_total_price > 0:
			# choice from responded inquiries only
			# page size
			rows_inquiries = self.engine.execute(SELECT_INQUIRIES_LIST_MIN_TOTAL_PRICE_SMALL, limit=per_page, offset=offset, minTotalPrice=min_total_price).fetchall()
		elif not_responded:
			# choice from not responded inquiries only
			# page size
			rows_inquiries = self.engine.execute(SELECT_INQUIRIES_LIST_NOT_RESPONDED, limit=per_page, offset=offset).fetchall()
		else:
			# choice from all inquiries
			# page size
			rows_inquiries = self.engine.execute(SELECT_INQUIRIES_LIST_ALL, limit=per_page, offset=offset).fetchall()

		if rows_inquiries:
			for inquiry_id, time_issued, time_responded, email, items_count, total_sum in rows_inquiries:

				inquiries.append( InquiryListItem(inquiry_id, time_issued, time_responded, email, items_count, total_sum) )
		
		return inquiries

	# get inquiry and related product details
	def getInquiry(self, inquiry_id):
		inquiry = None

		rows_inquiry_items = self.engine.execute(SELECT_INQUIRY_WITH_ITEMS, inquiry_id=inquiry_id).fetchall()

		if rows_inquiry_items:
			inquiry_id, time_issued, time_responded, email = rows_inquiry_items[0][0:4]
			items = []
			for inquiry_id, time_issued, time_responded, email, \
				item_id, item_amount, item_price, \
				product_code, product_title, product_price \
				in rows_inquiry_items:

				items.append( InquiryItem(item_id, item_amount, item_price, product_code, product_title, product_price) )

			inquiry = InquiryWithItems(inquiry_id, time_issued, time_responded, email, items)

		return inquiry

	# create inquiry and its items
	def newInquiry(self, email, items):

		if not(email and items):
			return False

		connection = self.engine.connect()
		transaction = connection.begin()
		try:
		    row_inquiry_id = connection.execute(INSERT_INQUIRY, email=email).fetchone()
		    inquiry_id, = row_inquiry_id

		    for product_id in items.keys():
		    	amount = items[product_id]
		    	connection.execute(INSERT_INQUIRY_ITEM, amount=amount, product_id=product_id, inquiry_id=inquiry_id)

		    transaction.commit()
		except:
		    transaction.rollback()
		    return False

		return True

	# edit inquiry and its items
	def respondInquiry(self, inquiry_id, items):

		if not(inquiry_id and items):
			return False

		connection = self.engine.connect()
		transaction = connection.begin()
		try:
			# update inquiry with responded timestamp
		    connection.execute(UPDATE_INQUIRY, inquiry_id=inquiry_id)

		    # update inquiry items with user specified amounts and prices
		    for item_id in items.keys():
		    	amount = items[item_id]['amount']
		    	price = items[item_id]['price']
		    	connection.execute(UPDATE_INQUIRY_ITEM, item_id=item_id, amount=amount, price=price)

		    transaction.commit()
		except:
		    transaction.rollback()
		    return False

		return True

	# remove inquiry and all its items
	def deleteInquiry(self, inquiry_id):
		rows_deleted = self.engine.execute(DELETE_INQUIRY_WITH_ITEMS, inquiry_id=inquiry_id).fetchall() # default autocommit
		return rows_deleted and len(rows_deleted)==1

	# remove single item from inquiry
	def deleteInquiryItem(self, item_id):
		self.engine.execute(DELETE_INQUIRY_ITEM, item_id=item_id) # default autocommit

	# get all main categories
	def getCategoryAll(self):

		rows_category = self.engine.execute(SELECT_CATEGORY_ALL).fetchall()

		categories = []
		for category_id, category_name in rows_category:
			categories.append( Category(category_id, category_name) )
		return categories

