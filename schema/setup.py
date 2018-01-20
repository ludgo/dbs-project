import psycopg2

DB_NAME = 'enterprise'
USERNAME = 'enterprise'
PASSWORD = 'enterprise'

with psycopg2.connect(database=DB_NAME, user=USERNAME, password=PASSWORD) as conn:
	with conn.cursor() as curs:
		curs.execute(open("tables_ddl.sql", "r").read())
