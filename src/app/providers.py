# contains connection pool engine thereby provides controllers with query execution
class PostgreSqlProvider:

	def __init__(self, engine):
		self.engine = engine
