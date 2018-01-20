QUERY_SNIPPET = 'SELECT * FROM {} LIMIT {};'

QUERY_ALL = 'SELECT * FROM {};'

QUERY_ALL_COUNT = 'SELECT COUNT(*) FROM {};'

QUERY_ID_BOARDERS = 'SELECT MIN(id), MAX(id) FROM {};'

def buildSnippetQuery(table_name, limit=5):
	return QUERY_SNIPPET.format(table_name, limit)

def buildAllQuery(table_name):
	return QUERY_ALL.format(table_name)

def buildAllCountQuery(table_name):
	return QUERY_ALL_COUNT.format(table_name)

def buildIdBoardersQuery(table_name):
	return QUERY_ID_BOARDERS.format(table_name)



def printInitInfo(table_name):
	print('init {} seed...'.format(table_name), flush=True)

def printFinishInfo(table_name, rows_count):
	print('{} seed finished with {} items\n'.format(table_name, rows_count), flush=True)

def printProgress(coef):
	print('{}%-'.format(int(coef*10)), end='', flush=True)

def printEnd():
	print('100%', flush=True)
