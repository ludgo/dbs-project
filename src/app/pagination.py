from math import ceil
from flask import request, url_for


# make flask remember arguments when changing page
def url_for_other_page(page):
	args = request.view_args.copy()
	args['page'] = page
	return url_for(request.endpoint, **args)

# flask pagination pattern logic class
class Pagination:

	PAGE_LIMIT = 99999

	def __init__(self, page, per_page, total_count=PAGE_LIMIT):
		self.page = page
		self.per_page = per_page
		self.total_count = total_count

	@property
	def pages(self):
		return int(ceil(self.total_count / float(self.per_page)))

	@property
	def has_prev(self):
		return self.page > 1

	@property
	def has_next(self):
		return self.page < self.pages

	'''
	def iter_pages(self, left_edge=3, left_current=3, right_current=3, right_edge=3):
		nums = list(range(1, left_edge + 1)) \
				+ list(range(self.page - left_current, self.page + right_current + 1)) \
				+ list(range(self.pages - right_edge, self.pages + 1))
		previous = None
		for num in sorted(set(nums)):
			if num >= 1 and num <= self.pages:
				if previous and previous + 1 < num:
					yield None
				yield num
				previous = num
	'''

	# 1,2,left_edge,None,current minus left_current,..,current plus right_current,None
	def iter_pages(self, left_edge=3, left_current=3, right_current=3):
		nums = list(range(1, left_edge + 1)) \
				+ list(range(self.page - left_current, self.page + right_current + 1))
		previous = None
		for num in sorted(set(nums)):
			if num >= 1 and num <= self.pages:
				if previous and previous + 1 < num:
					yield None
				yield num
				previous = num
		if self.has_next:
			yield None

