import logging
import sqlite3

class SQLDatabaseHandler():
	"""Handler for SQL database."""

	def __init__(self, db_name):
		"""Constructor"""
		self.db_name = db_name
		print(self.db_name)
		self.logger = logging.getLogger('VSCADA.server.' + __name__)

	def select(self, table_names, *fields, **constraints):
		"""Executes a SQL SELECT statement."""
		conn = sqlite3.connect(self.db_name)
		db = conn.cursor()
		
		cvalues = []
		ckeys = []

		if fields:
			columns = ', '.join(map(str, fields))
		else:
			columns = '*'

		if type(table_names) not in [list, tuple]:
			tables = str(table_names)
		else:
			if 'join_type' not in constraints:
				tables = ' NATURAL JOIN '.join(map(str, table_names))
			else:
				pass

		if not constraints:
			where = ''
		else:
			for ckey, cvalue in constraints.items():
				if ckey != 'join_type':
					if cvalue is None:
						continue
					ckeys.append(ckey + '=?')
					cvalues.append(cvalue)
			if ckeys:
				where = 'WHERE ' + 'AND '.join(ckeys)
			else:
				where = ''
				cvalues = []

		query = 'SELECT %s FROM %s %s' % (columns, tables, where)

		self.logger.error('send query: %s' % query)
		print(constraints)
		# input()
		
		response = {}

		try:
			db.execute(query, tuple(cvalues))
			results = db.fetchall()
		except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
			response['query_status'] = 'error'
			response['reason'] = e
			response['query'] = query
			return response

		if results:
			response['query_status'] = 'success'
		else:
			response['query_status'] = 'no_result'
			response['reason'] = 'no results matching criteria'
			return response

		entries = [] 
		entry = {}

		if fields:
			header = fields
		else:
			header = [i[0] for i in db.description]
		entries = [dict(zip(header, result)) for result in results]

		response['vals'] = entries
		conn.commit()
		conn.close()
		# print(response)
		return response

	def insert(self, **fields):
		"""Executes a SQL INSERT statement."""
		conn = sqlite3.connect(self.db_name)
		db = conn.cursor()

		response = {}
		for table, tblfields in fields.items():
			fkeys = []
			fvalues = []
			vallist = []
			for fkey, fvalue in tblfields.items():
				fkeys.append(fkey)
				fvalues.append(fvalue)
				vallist.append('?')
			valstring = '(' + ', '.join(vallist) + ')'
			query = 'INSERT INTO %s %s VALUES %s' % (table, 
													 tuple(fkeys), 
													 valstring)
			# print(query)
			try:
				db.execute(query, tuple(fvalues))
				if db.rowcount == 1:
					print("Success")
					response['query_status'] = 'success'
				else:
					response['query_status'] = 'error'
			except sqlite3.OperationalError as e:
				response = {}
				response['query_status'] = 'error'
				response['reason'] = e
				response['query'] = query
				return response
		conn.commit()
		conn.close()
		# print(response)
		return response

	def update(self, **fields_constraints):
		"""Executes a SQL UPDATE statement."""
		conn = sqlite3.connect(self.db_name)
		db = conn.cursor()

		response = {}
		for table, tblvals in fields_constraints.items():
			fkeys = []
			fvalues = []
			ckeys = []
			cvalues = []
			fstring = ''
			cstring = ''
			if 'fields' in tblvals:
				for fkey, fvalue in tblvals['fields'].items():
					fkeys.append(fkey + '=?')
					fvalues.append(fvalue)
				fstring = ', '.join(fkeys)
			if 'constraints' in tblvals:
				for ckey, cvalue in tblvals['constraints'].items():
					ckeys.append(ckey + '=?')
					cvalues.append(cvalue)
				cstring = ' AND '.join(ckeys)
			query = 'UPDATE %s SET %s WHERE %s' % (table, 
												   fstring, 
												   cstring)

			try:
				db.execute(query, tuple(fvalues + cvalues))
				if db.rowcount == 1:
					print("Success")
					response['query_status'] = 'success'
				else:
					response['query_status'] = 'error'
			except sqlite3.OperationalError as e:
				response = {}
				response['query_status'] = 'error'
				response['reason'] = e
				response['query'] = query
				return response

		conn.commit()
		conn.close()
		print(response)
		return response

	def delete(self, **constraints):
		"""Executes a SQL DELETE statement."""
		conn = sqlite3.connect(self.db_name)
		db = conn.cursor()

		response = {}
		for table, tblfields in constraints.items():
			ckeys = []
			cvalues = []
			for ckey, cvalue in tblfields.items():
				ckeys.append(ckey + '=?')
				cvalues.append(cvalue)
			cstring = ' AND '.join(ckeys)
			query = 'DELETE FROM %s WHERE %s' % (table, cstring)
			try:
				db.execute(query, tuple(cvalues))
				if db.rowcount == 1:
					print("Success")
					response['query_status'] = 'success'
				else:
					response['query_status'] = 'error'
			except sqlite3.OperationalError as e:
				response = {}
				response['query_status'] = 'error'
				response['reason'] = e
				response['query'] = query
				return response
		conn.commit()
		conn.close()
		print(response)
		return response

class vscada_database():
	"""
	VSCADA specific SQL commands
	"""
	def __init__(self, db_name = None):
		self.handler_sql = SQLDatabaseHandler(db_name)
		self.logger = logging.getLogger('VSCADA.server.' + __name__)

	def _search_table_to_list(self, tables, *colums, **constraints):
		query_result = self.handler_sql.select(
					tables,
					*colums,
					**constraints)

		query_status = query_result['query_status']
		if query_status == 'success':

			# if not dict_key:
			return query_result['vals']

			# result_dict = {}

			# for query_tuple in query_result['vals']:
			# 	key = query_tuple.pop(dict_key, None)
			# 	if key not in result_dict:
			# 		result_dict[key] = [query_tuple]
			# 	else:
			# 		result_dict[key].append(query_tuple)

			# return result_dict

		elif query_status == 'error':
			self.logger.error(query_result)
			raise RuntimeError('error querying database')
		else:
			return []

	def get_cans(self, rtr = 1, essential = 0):
		return self._search_table_to_list(['can'],
			'can_id', 'sample_rate', 'rtr',
			rtr = rtr, essential = essential)

	def get_startup(self):
		startup_query = self.handler_sql.select(['startup'])
		if startup_query['query_status'] == 'success':
			return sorted(startup_query['vals'], key = lambda k: k['sequence_number'])
		else:
			return []

	def get_sensor_position(self, raise_error = False, sensor_id = None, io = None):

		try:
			return self._search_table_to_list(['sensor', 'type'],
				'sensor_id', 'can_id', 'address_offset', 'byte_size',
				sensor_id = sensor_id, io = io)
		except Exception as e:
			if raise_error:
				raise e
			else:
				return []

	def get_full_sensor(self, can_id = None, io = None, raise_error = False):
		try:
			return self._search_table_to_list(['sensor','type','input_sensor', 'can'], 
	            'sensor_id', 'sensor_name', 'address_offset', 'byte_size',
	            'rrd_filename', 'unit', 'sample_rate', 'overwrite_period',
				can_id = can_id, io = 'input')
		except Exception as e:
			if raise_error:
				raise e
			else:
				return []

	def get_full_input_sensor_from_can(self, can_id):
		return self.get_full_sensor(can_id = can_id, io = 'input')

	def get_full_warning_sensor_from_can(self, can_id, dict_key = 'sensor_id'):

		query_result = self._search_table_to_list(
			['sensor','type', 'warning', 'action', 'action_name'], 
            'sensor_id', 'sensor_name', 'range_low', 'range_high',
            'action_name', 'param1', 'param2', 'param3',
			can_id = can_id, io = 'input')
		result_dict = {}
		for query_tuple in query_result:
			key = query_tuple.pop(dict_key, None)
			if key not in result_dict:
				result_dict[key] = [query_tuple]
			else:
				result_dict[key].append(query_tuple)
		return result_dict

	def add_sensor(self, can_id = 0, type_id = 0, address_offset = 0, 
				   byte_size = 0, sensor_name = "", unit = ""):
		fields = {}
		sensor = {}
		sensor['can_id']         = can_id
		sensor['type_id']        = type_id
		sensor['address_offset'] = address_offset
		sensor['byte_size']      = byte_size
		sensor['sensor_name']    = sensor_name
		sensor['unit']           = unit
		fields['sensor'] = sensor
		return self.handler_sql.insert(**fields)

	def modify_sensor(self, sensor_id = 0, can_id = 0, type_id = 0, 
					  address_offset = None, byte_size = None, sensor_name = None, 
					  unit = ""):
		fields_constraints = {}
		fields = {}
		constraints = {}

		if address_offset:
			fields['address_offset'] = address_offset

		if byte_size:
			fields['byte_size'] = byte_size

		if sensor_name:
			fields['sensor_name'] = sensor_name

		if unit:
			fields['unit'] = unit
		constraints['sensor_id'] = sensor_id
		constraints['can_id'] = can_id
		constraints['type_id'] = type_id
		fields_constraints['fields'] = fields
		fields_constraints['constraints'] = constraints
		return self.handler_sql.update(**fields_constraints)

	def delete_sensor(self, sensor_id = 0):
		constraints = {}
		constraints['sensor_id'] = sensor_id
		return self.handler_sql.delete(**constraints)

	def add_rule(self):
		pass

	def modify_rule(self):
		pass

	def delete_rule(self):
		pass
