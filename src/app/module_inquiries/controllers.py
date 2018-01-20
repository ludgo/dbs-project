import re
from flask import Blueprint, request, render_template, redirect, url_for, abort, flash, jsonify

from app.module_inquiries.providers import InquiryProvider
from app.pagination import Pagination
from app import engine

# 1+ digits regex
PATTERN_DIGITS = re.compile("^[0-9]+$")

# static web page
blueprint_inquiries = Blueprint('inquiries', __name__, url_prefix='/inquiries')

inquiry_provider = InquiryProvider(engine)

# GET main page of paged inquiries
# POST filter inquiries' min. total price
@blueprint_inquiries.route('/', defaults={'page': 1, 'per_page': 20, 'pending_only': 0, 'min_total_price': 0}, methods=['GET', 'POST'])
@blueprint_inquiries.route('/<int:page>/<int:per_page>/<int:pending_only>', defaults={'min_total_price': 0}, methods=['GET', 'POST'])
@blueprint_inquiries.route('/<int:page>/<int:per_page>/<int:pending_only>/<float:min_total_price>')
def inquiries_list(page, per_page, pending_only, min_total_price):
	if request.method == 'POST':
		return redirect( url_for('inquiries.inquiries_list', page=page, per_page=per_page, pending_only=pending_only, min_total_price=float(request.form['input__total__price'])) )
	inquiries = inquiry_provider.getInquiries(page, per_page, pending_only==1, min_total_price)
	pagination = Pagination(page, per_page)
	return render_template('module_inquiries/inquiries.html', inquiries=inquiries, pagination=pagination, pendingOnly=pending_only==1, minTotalPrice=min_total_price)

# GET display inquiry detail
@blueprint_inquiries.route('/detail/<int:inquiry_id>')
def inquiry_detail(inquiry_id):
	inquiry = inquiry_provider.getInquiry(inquiry_id)
	if not inquiry:
		abort(404)
	return render_template('module_inquiries/inquiry_detail.html', inquiry=inquiry)

# GET json inquiry representation
@blueprint_inquiries.route('/detail/<int:inquiry_id>/json')
def inquiry_detail_json(inquiry_id):
	inquiry = inquiry_provider.getInquiry(inquiry_id)
	if not inquiry:
		abort(404)
	return jsonify(inquiry=inquiry.serialize)

# GET display editable inquiry detail
# POST edit inquiry
@blueprint_inquiries.route('/edit/<int:inquiry_id>', methods=['GET', 'POST'])
def inquiry_edit(inquiry_id):
	if request.method == 'POST':
		items = {}
		for item_id in request.form.keys():
			if PATTERN_DIGITS.match(item_id):
				amount = request.form['amount_{}'.format(item_id)]
				price = request.form['price_{}'.format(item_id)]
				items[item_id] = {'amount': amount, 'price': price}
		if inquiry_provider.respondInquiry(inquiry_id, items):
			flash('Inquiry succesfully responded')
		else:
			flash('Inquiry responding failed')
		return redirect( url_for('inquiries.inquiry_detail', inquiry_id=inquiry_id) )
	else:
		inquiry = inquiry_provider.getInquiry(inquiry_id)
		if not inquiry:
			abort(404)
		return render_template('module_inquiries/inquiry_edit.html', inquiry=inquiry)

# GET display screen for adding new inquiry
# POST create inquiry
@blueprint_inquiries.route('/new', methods=['GET', 'POST'])
def inquiry_new():
	if request.method == 'POST':
		email = request.form['email']
		items = {}
		for product_id in request.form.keys():
			if product_id != 'email':
				amount = request.form[product_id]
				items[product_id] = amount

		if inquiry_provider.newInquiry(email, items):
			flash('Inquiry succesfully created')
		else:
			flash('Inquiry creating failed')
		return redirect( url_for('inquiries.inquiries_list') )
	else:
		categories = inquiry_provider.getCategoryAll()
		return render_template('module_inquiries/inquiry_new.html', categories=categories)

# POST delete inquiry and its items
@blueprint_inquiries.route('/delete/<int:inquiry_id>', methods=['POST'])
def inquiry_delete(inquiry_id):
	if inquiry_provider.deleteInquiry(inquiry_id):
		flash('Inquiry succesfully deleted')
	else:
		flash('Inquiry deleting failed')
	return redirect( url_for('inquiries.inquiries_list') )

# POST delete single inquiry item from inquiry
@blueprint_inquiries.route('/delete_item/<int:inquiry_id>/<int:item_id>', methods=['POST'])
def inquiry_delete_item(inquiry_id, item_id):
	inquiry_provider.deleteInquiryItem(item_id)
	return redirect( url_for('inquiries.inquiry_edit', inquiry_id=inquiry_id) )

