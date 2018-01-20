#####################
# see also report.txt
#####################

import psycopg2
import sys

from util_analyze import *
from properties import *



def calcCountRows(curs, table_name):
	curs.execute(buildCountRowsQuery(table_name))
	count, = curs.fetchone()
	printCountRows(count)

def calcNumStats(curs, table_name, col_name):
	curs.execute(buildNumStatsQuery(table_name, col_name))
	minimum, maximum, average, mode, quartile25, quartile50, quartile75 = curs.fetchone()
	printNumStats(col_name, minimum, maximum, average, mode, quartile25, quartile50, quartile75)

def calcCountNull(curs, table_name, col_name):
	curs.execute(buildCountNullQuery(table_name, col_name, False))
	count_notnull, = curs.fetchone()
	curs.execute(buildCountNullQuery(table_name, col_name, True))
	count_null, = curs.fetchone()
	printCountNull(col_name, count_notnull, count_null)

def calcCountBool(curs, table_name, col_name):
	curs.execute(buildCountBoolQuery(table_name, col_name, False))
	count_false, = curs.fetchone()
	curs.execute(buildCountBoolQuery(table_name, col_name, True))
	count_true, = curs.fetchone()
	printCountBool(col_name, count_true, count_false)

def calcStats(curs, table_name, cols_num=[], cols_null=[], cols_bool=[]):
	print(table_name, flush=True)
	calcCountRows(curs, table_name)
	for col_num in cols_num:
		calcNumStats(curs, table_name, col_num)
	for col_null in cols_null:
		calcCountNull(curs, table_name, col_null)
	for col_bool in cols_bool:
		calcCountBool(curs, table_name, col_bool)



def calcNomStats(curs, table_name, cols_nom=[]):
	print(table_name, flush=True)
	for col_nom in cols_nom:
		curs.execute(buildCountValuesQuery(table_name, col_nom))
		printCountValues(col_nom, curs.fetchall())



with psycopg2.connect(database=DB_NAME, user=USERNAME, password=PASSWORD) as conn:

	conn.set_session(autocommit=True)
	
	with conn.cursor() as cursor:

		cursor.execute(COMMAND_ANALYZE)

		print('--- NUMERICAL STATISTICS---', flush=True)
		calcStats(cursor, 'auth'
			)
		calcStats(cursor, 'card_provider'
			)
		calcStats(cursor, 'card', 
			cols_num=['card_provider_id', 'auth_id']
			)
		calcStats(cursor, 'category'
			)
		calcStats(cursor, 'subcategory', 
			cols_num=['category_id']
			)
		calcStats(cursor, 'product', 
			cols_num=['price', 'subcategory_id'],
			cols_null=['ean'],
			cols_bool=['available']
			)
		calcStats(cursor, 'ranking', 
			cols_num=['num_stars']
			)
		calcStats(cursor, 'review', 
			cols_num=['auth_id', 'ranking_id', 'product_id'],
			cols_null=['time_updated']
			)
		calcStats(cursor, 'commentary', 
			cols_num=['auth_id', 'review_id']
			)
		calcStats(cursor, 'inquiry', 
			cols_num=['auth_id'],
			cols_null=['time_responded', 'auth_id']
			)
		calcStats(cursor, 'inquiry_item', 
			cols_num=['amount', 'price', 'product_id', 'inquiry_id']
			)

		print('--- NOMINAL STATISTICS---', flush=True)
		calcNomStats(cursor, 'card', 
			['card_provider_id']
			)
		calcNomStats(cursor, 'subcategory', 
			['category_id']
			)
		calcNomStats(cursor, 'product', 
			['subcategory_id']
			)
		calcNomStats(cursor, 'review', 
			['ranking_id']
			)
		calcNomStats(cursor, 'inquiry_item', 
			['amount']
			)

