########################
# see also info_seed.txt
########################

import psycopg2

from random import uniform, choice, randint

from constants import *
from tables_dml import *
from util_seed import *
from properties import *

from faker import Factory
fake = Factory.create()

card_provider_ids, category_ids, subcategory_ids, ranking_ids = [], [], [], []

def printSnippet(curs, table_name):
	curs.execute(buildSnippetQuery(table_name))
	for row in curs.fetchall():
		print(row, flush=True)
	print('...', flush=True)

def getAll(curs, table_name, print_bool=True):
	arr_ids = []
	curs.execute(buildAllQuery(table_name))
	for row in curs.fetchall():
		if print_bool:
			print(row, flush=True)
		arr_ids.append(row[0])
	return arr_ids

def getCount(curs, table_name, print_bool=True):
	curs.execute(buildAllCountQuery(table_name))
	count, = curs.fetchone()
	if print_bool:
		printFinishInfo(table_name, count)
	return count

def getBoarders(curs, table_name):
	curs.execute(buildIdBoardersQuery(table_name))
	mini, maxi = curs.fetchone()
	return mini, maxi


INSERTS = {
	'auth' : INSERT_INTO_AUTH, 
	'card_provider' : INSERT_INTO_CARD_PROVIDER, 
	'card' : INSERT_INTO_CARD, 
	'category' : INSERT_INTO_CATEGORY, 
	'subcategory' : INSERT_INTO_SUBCATEGORY, 
	'product' : INSERT_INTO_PRODUCT, 
	'ranking' : INSERT_INTO_RANKING, 
	'review' : INSERT_INTO_REVIEW, 
	'commentary' : INSERT_INTO_COMMENTARY, 
	'inquiry' : {
		'auth' : INSERT_INTO_INQUIRY_AUTH, 
		'anonymous' : INSERT_INTO_INQUIRY_ANONYMOUS 
		}, 
	'inquiry_item' : INSERT_INTO_INQUIRY_ITEM
}

progress_unit = 10
commit_unit = 1000


conn = None
try:	
	conn = psycopg2.connect(database=DB_NAME, user=USERNAME, password=PASSWORD)

	# setup schema
	if True:
		with conn.cursor() as cursor:
			print('init schema...', flush=True)
			cursor.execute(open('tables_ddl_without_index.sql', 'r').read())
			conn.commit()
			print('done\n', flush=True)

	# auth
	if True:
		printInitInfo('auth')
		for i in range(progress_unit):
			with conn.cursor() as cursor:
				printProgress(i)
				for j in range(40):
					for k in range(commit_unit):
						email = fake.email()
						password_hash = fake.pystr(min_chars=40, max_chars=40)
						cursor.execute(INSERTS['auth'], (email, password_hash))
					conn.commit()
		printEnd()
	with conn.cursor() as cursor:
		printSnippet(cursor, 'auth')
		count_auth = getCount(cursor, 'auth')
		auth_min_id, auth_max_id = getBoarders(cursor, 'auth')

	# card_provider
	if True:
		with conn.cursor() as cursor:
			printInitInfo('card_provider')
			for provider in CREDIT_CARD_PROVIDERS:
				cursor.execute(INSERTS['card_provider'], (provider, ))
			conn.commit()
	with conn.cursor() as cursor:
		card_provider_ids = getAll(cursor, 'card_provider')
		count_card_provider = getCount(cursor, 'card_provider')
	assert(count_card_provider == len(CREDIT_CARD_PROVIDERS))

	# card
	if True:
		printInitInfo('card')
		for i in range(progress_unit):
			with conn.cursor() as cursor:
				printProgress(i)
				for j in range(40):
					for k in range(commit_unit):
						number_encrypted = fake.pystr(min_chars=32, max_chars=32)
						holder_encrypted = fake.pystr(min_chars=32, max_chars=32)
						security_code_encrypted = fake.pystr(min_chars=32, max_chars=32)
						expire_encrypted = fake.pystr(min_chars=32, max_chars=32)
						card_provider_id = choice(card_provider_ids)
						auth_id = randint(auth_min_id, auth_max_id)
						cursor.execute(INSERTS['card'], (number_encrypted, holder_encrypted, security_code_encrypted, expire_encrypted, card_provider_id, auth_id))
					conn.commit()
		printEnd()
	with conn.cursor() as cursor:
		printSnippet(cursor, 'card')
		count_card = getCount(cursor, 'card')

	# category
	if True:
		with conn.cursor() as cursor:
			printInitInfo('category')
			for name in CATEGORIES.keys():
				cursor.execute(INSERTS['category'], (name, ))
			conn.commit()
			cursor.execute(buildAllQuery('category'))
			for row in cursor.fetchall():
				print(row, flush=True)
				category_ids.append(row[0])
	with conn.cursor() as cursor:
		cursor.execute(buildAllCountQuery('category'))
		count_category, = cursor.fetchone()
		printFinishInfo('category', count_category)
	assert(count_category == len(CATEGORIES.keys()))

	# subcategory
	if True:
		with conn.cursor() as cursor:
			printInitInfo('subcategory')
			for category_name in CATEGORIES.keys():
				cursor.execute(SELECT_CATEGORY_ID, (category_name, ))
				category_id, = cursor.fetchone()
				for name in CATEGORIES[category_name]:
					cursor.execute(INSERTS['subcategory'], (name, category_id))
				conn.commit()
	with conn.cursor() as cursor:
		printSnippet(cursor, 'subcategory')
		subcategory_ids = getAll(cursor, 'subcategory', False)
		count_subcategory = getCount(cursor, 'subcategory')
	assert(count_subcategory == sum(len(v) for v in CATEGORIES.values()))

	# product
	if True:
		printInitInfo('product')
		for i in range(progress_unit):
			with conn.cursor() as cursor:
				printProgress(i)
				for j in range(200):
					for k in range(commit_unit):
						code = fake.ean8()
						ean = None
						# 80% : 20%
						if j < 160:
							ean = fake.ean13()
						price = round(uniform(0.5, 10000.), 2)
						available = not (fake.pybool() and fake.pybool()) # 75% : 25%
						thumbnail_url = fake.image_url(width=200, height=200)
						image_url = fake.image_url(width=500, height=500)
						title = fake.sentence(nb_words=8, variable_nb_words=True)
						description = fake.paragraph(nb_sentences=30, variable_nb_sentences=True)
						subcategory_id = choice(subcategory_ids)
						cursor.execute(INSERTS['product'], (code, ean, price, available, thumbnail_url, image_url, title, description, subcategory_id))
					conn.commit()
		printEnd()
	with conn.cursor() as cursor:
		printSnippet(cursor, 'product')
		count_product = getCount(cursor, 'product')
		product_min_id, product_max_id = getBoarders(cursor, 'product')

	# ranking
	if True:
		with conn.cursor() as cursor:
			printInitInfo('ranking')
			for ranking in RANKINGS:
				cursor.execute(INSERTS['ranking'], (ranking, ))
			conn.commit()
	with conn.cursor() as cursor:
		ranking_ids = getAll(cursor, 'ranking')
		count_ranking = getCount(cursor, 'ranking')
	assert(count_ranking == len(RANKINGS))

	# review
	if True:
		printInitInfo('review')
		for i in range(progress_unit):
			with conn.cursor() as cursor:
				printProgress(i)
				for j in range(40):
					for k in range(commit_unit):
						time_created = fake.date_time_this_decade()
						time_updated = None
						# 20% : 80%
						if j < 8:
							time_updated = fake.date_time_between(start_date=time_created, end_date='now')
						title = fake.sentence(nb_words=6, variable_nb_words=True)
						body = fake.paragraph(nb_sentences=20, variable_nb_sentences=True)
						auth_id = randint(auth_min_id, auth_max_id)
						ranking_id = choice(ranking_ids)
						product_id = randint(product_min_id, product_max_id)
						cursor.execute(INSERTS['review'], (time_created, time_updated, title, body, ranking_id, auth_id, product_id))
					conn.commit()
		printEnd()
	with conn.cursor() as cursor:
		printSnippet(cursor, 'review')
		count_review = getCount(cursor, 'review')
		review_min_id, review_max_id = getBoarders(cursor, 'review')

	# commentary
	if True:
		printInitInfo('commentary')
		for i in range(progress_unit):
			with conn.cursor() as cursor:
				printProgress(i)
				for j in range(40):
					for k in range(commit_unit):
						time_created = fake.date_time_this_decade()
						body = fake.sentence(nb_words=50, variable_nb_words=True)
						auth_id = randint(auth_min_id, auth_max_id)
						review_id = randint(review_min_id, review_max_id)
						cursor.execute(INSERTS['commentary'], (time_created, body, auth_id, review_id))
					conn.commit()
		printEnd()
	with conn.cursor() as cursor:
		printSnippet(cursor, 'commentary')
		count_commentary = getCount(cursor, 'commentary')

	# inquiry
	if True:
		printInitInfo('inquiry')
		for i in range(progress_unit):
			with conn.cursor() as cursor:
				printProgress(i)
				for j in range(200):
					for k in range(commit_unit):
						time_issued = fake.date_time_this_decade()
						time_responded = None
						# 80% : 20%
						if j < 160:
							time_responded = fake.date_time_between(start_date=time_issued, end_date='now')
						# 50% : 50%
						if j >= 50 and j < 150:
							auth_id = randint(auth_min_id, auth_max_id)
							cursor.execute(INSERTS['inquiry']['auth'], (time_issued, time_responded, auth_id))
						else:
							email = fake.email()
							cursor.execute(INSERTS['inquiry']['anonymous'], (email, time_issued, time_responded))
					conn.commit()
		printEnd()
	with conn.cursor() as cursor:
		printSnippet(cursor, 'inquiry')
		count_inquiry = getCount(cursor, 'inquiry')
		inquiry_min_id, inquiry_max_id = getBoarders(cursor, 'inquiry')

	# inquiry_item
	if True:
		printInitInfo('inquiry_item')
		for i in range(progress_unit):
			with conn.cursor() as cursor:
				printProgress(i)
				for j in range(600):
					for k in range(commit_unit):
						amount = 1
						while fake.pybool():
							amount += 1
						product_id = randint(product_min_id, product_max_id)
						inquiry_id = randint(inquiry_min_id, inquiry_max_id)
						cursor.execute(INSERTS['inquiry_item'], (amount, product_id, inquiry_id))
					conn.commit()
		printEnd()
	with conn.cursor() as cursor:
		printSnippet(cursor, 'inquiry_item')
		count_inquiry_item = getCount(cursor, 'inquiry_item')

	# keep 1 : 1..*
	if True:
		with conn.cursor() as cursor:
			cursor.execute(DELETE_EMPTY_INQUIRY)
			count_deleted = cursor.rowcount
			conn.commit()
			print('deleted {} empty inquiries\n'.format(count_deleted), flush=True)

	print('seed done\n', flush=True)

	# add indexes
	if True:
		with conn.cursor() as cursor:
			print('add indexes...', flush=True)
			cursor.execute(open('tables_ddl_add_index.sql', 'r').read())
			conn.commit()
			print('done\n', flush=True)

except psycopg2.DatabaseError as e: 
	print('\nerror:')
	print(e.__class__.__name__)
	print(e)

finally:
	if conn:
		conn.close()

