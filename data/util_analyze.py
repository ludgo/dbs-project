COMMAND_ANALYZE = 'VACUUM ANALYZE;'

QUERY_COUNT_ROWS = 'SELECT COUNT(*) FROM {};'

QUERY_NUM_STATS = '''SELECT min({c_name}),
						max({c_name}),
						avg({c_name}),
						mode() WITHIN GROUP (ORDER BY {c_name}),
						percentile_cont(0.25) WITHIN GROUP (ORDER BY {c_name}),
						percentile_cont(0.5) WITHIN GROUP (ORDER BY {c_name}),
						percentile_cont(0.75) WITHIN GROUP (ORDER BY {c_name})
					FROM {t_name};'''

QUERY_COUNT_NULL = 'SELECT COUNT(*) FROM {} WHERE {} IS NULL;'
QUERY_COUNT_NOT_NULL = 'SELECT COUNT(*) FROM {} WHERE {} IS NOT NULL;'

QUERY_COUNT_TRUE = 'SELECT COUNT(*) FROM {} WHERE {}=TRUE;'
QUERY_COUNT_FALSE = 'SELECT COUNT(*) FROM {} WHERE {}=FALSE;'

QUERY_COUNT_VALUES = '''SELECT {c_name}, COUNT({c_name}) 
					FROM {t_name} 
					GROUP BY {c_name};'''



def buildCountRowsQuery(table_name):
	return QUERY_COUNT_ROWS.format(table_name)

def buildNumStatsQuery(table_name, col_name):
	return QUERY_NUM_STATS.format(t_name=table_name, c_name=col_name)

def buildCountNullQuery(table_name, col_name, isNull):
	if isNull:
		return QUERY_COUNT_NULL.format(table_name, col_name)
	else:
		return QUERY_COUNT_NOT_NULL.format(table_name, col_name)

def buildCountBoolQuery(table_name, col_name, isTrue):
	if isTrue:
		return QUERY_COUNT_TRUE.format(table_name, col_name)
	else:
		return QUERY_COUNT_FALSE.format(table_name, col_name)

def buildCountValuesQuery(table_name, col_name):
	return QUERY_COUNT_VALUES.format(t_name=table_name, c_name=col_name)



def printCountRows(count):
	print('\tCount: {}'.format(count))
	print(flush=True)

def printNumStats(col_name, minimum, maximum, average, mode, quartile25, quartile50, quartile75):
	print('\t{}'.format(col_name))
	print('\t\tMin: {}'.format(minimum))
	print('\t\tMax: {}'.format(maximum))
	print('\t\tAverage: {}'.format(average))
	print('\t\tMode: {}'.format(mode))
	print('\t\tQuartile 0.25: {}'.format(quartile25))
	print('\t\tQuartile 0.5: {}'.format(quartile50))
	print('\t\tQuartile 0.75: {}'.format(quartile75))
	print(flush=True)

def printCountNull(col_name, count_notnull, count_null):
	print('\t{}'.format(col_name))
	print('\t\tNot NULL: {}'.format(count_notnull))
	print('\t\tNULL: {}'.format(count_null))
	total = count_notnull + count_null
	ratio = count_notnull / total
	print('\t\tNot NULL %: {}'.format(100 * ratio))
	print(flush=True)

def printCountBool(col_name, countTrue, countFalse):
	print('\t{}'.format(col_name))
	print('\t\tTrue: {}'.format(countTrue))
	print('\t\tFalse: {}'.format(countFalse))
	total = countTrue + countFalse
	ratio = countTrue / total
	print('\t\tTrue %: {}'.format(100 * ratio))
	print(flush=True)

def printCountValues(col_name, rows):
	print('\t{}'.format(col_name))
	rows.sort(key=lambda tup: tup[0])
	for key, value in rows:
		print('\t\t{}: {}'.format(key, value))
	print(flush=True)
