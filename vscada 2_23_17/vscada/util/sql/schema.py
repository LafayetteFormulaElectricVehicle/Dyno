PRIM_KEY = 'integer primary key autoincrement'

#SQLite file to be created
Sensor_DB = [
	{
		'Table'       : 'can',
		'Field_List'  :
			[
				{'Field' : 'can_id',      'Type' : PRIM_KEY },
				{'Field' : 'rtr',         'Type' : 'integer'},
				{'Field' : 'sample_rate', 'Type' : 'integer'},
				{'Field' : 'system_id',   'Type' : 'integer'},
				{'Field' : 'essential',   'Type' : 'integer'}
			],
		'Foreign_Key' : 
			[
				{'system_id' : 'system(system_id)'}
			]
	},
	{
		'Table'      : 'system',
		'Field_List' :
			[
				{'Field' : 'system_id',   'Type' : PRIM_KEY},
				{'Field' : 'system_name', 'Type' : 'text'  },
				{'Field' : 'description', 'Type' : 'text'  }
			]
	},
	{
		'Table'      : 'sensor',
		'Field_List' :
			[
				{'Field' : 'sensor_id',      'Type' : PRIM_KEY },
				{'Field' : 'can_id',         'Type' : 'integer'},
				{'Field' : 'type_id',        'Type' : 'integer'},
				{'Field' : 'address_offset', 'Type' : 'integer'},
				{'Field' : 'byte_size',      'Type' : 'integer'},
				{'Field' : 'sensor_name',    'Type' : 'text'   },
				{'Field' : 'unit',           'Type' : 'text'   }
			],
		'Foreign_Key' : 
			[
				{'can_id'  : 'can(can_id)'  },
				{'type_id' : 'type(type_id)'}
			]
	},
	{
		'Table'      : 'type',
		'Field_List' :
			[
				{'Field' : 'type_id',   'Type' : PRIM_KEY},
				{'Field' : 'io',        'Type' : 'text'  },
				{'Field' : 'type_name', 'Type' : 'text'  },
			]
	},
	{
		'Table'      : 'input_sensor',
		'Field_List' :
			[
				{'Field' : 'sensor_id',          'Type' : 'integer'},
				{'Field' : 'rrd_filename',       'Type' : 'text'   },
				{'Field' : 'overwrite_period',   'Type' : 'integer'},
				{'Field' : 'pow_square',         'Type' : 'real'   },
				{'Field' : 'pow_linear',         'Type' : 'real'   },
				{'Field' : 'pow_constant',       'Type' : 'real'   },
				{'Field' : 'pow_inverse',        'Type' : 'real'   },
				{'Field' : 'pow_inverse_square', 'Type' : 'real'   }
			]
	},
	{
		'Table'      : 'default_output',
		'Field_List' :
			[
				{'Field' : 'sensor_id',      'Type' : 'integer'},
				{'Field' : 'default_value',  'Type' : 'integer'}
			],
		'Foreign_Key' : 
			[
				{'sensor_id' : 'sensor(sensor_id)'}
			]
	},
	{
		'Table'      : 'warning',
		'Field_List' :
			[
				{'Field' : 'sensor_id',  'Type' : 'integer'},
				{'Field' : 'range_low',  'Type' : 'integer'},
				{'Field' : 'range_high', 'Type' : 'integer'},
				{'Field' : 'action_id',  'Type' : 'integer'}
			],
		'Foreign_Key' : 
			[
				{'sensor_id' : 'sensor(sensor_id)'},
				{'action_id' : 'action(action_id)'}
			]
	},
	{
		'Table'      : 'action',
		'Field_List' :
			[
				{'Field' : 'action_id',      'Type' : PRIM_KEY },
				{'Field' : 'action_name_id', 'Type' : 'integer'},
				{'Field' : 'param1',         'Type' : 'integer'},
				{'Field' : 'param2',         'Type' : 'integer'},
				{'Field' : 'param3',         'Type' : 'text'   },
				{'Field' : 'description',    'Type' : 'text'   }
			],
		'Foreign_Key' : 
			[
				{'action_name_id' : 'action_name(action_name_id)'},
			]
	},
	{
		'Table'      : 'action_name',
		'Field_List' :
			[
				{'Field' : 'action_name_id',   'Type' : PRIM_KEY },
				{'Field' : 'action_name',      'Type' : 'text'},
				{'Field' : 'param1_name',      'Type' : 'text'},
				{'Field' : 'param2_name',      'Type' : 'text'},
				{'Field' : 'param3_name',      'Type' : 'text'}
			]
	},
	{
		'Table'      : 'startup',
		'Field_List' :
			[
				{'Field' : 'sequence_number', 'Type' : 'integer'},
				{'Field' : 'sensor_id',       'Type' : 'integer'},
				{'Field' : 'direction',       'Type' : 'text'   },
				{'Field' : 'value_await',     'Type' : 'integer'},
				{'Field' : 'time_await',      'Type' : 'integer'},
				{'Field' : 'action_id',       'Type' : 'integer'},
				{'Field' : 'description',     'Type' : 'text'   }
			],
		'Foreign_Key' : 
			[
				{'sensor_id' : 'sensor(sensor_id)'},
				{'action_id' : 'action(action_id)'}
			]
	}
]

#list of all SQLite *.db files to create
SQL_List = [
	{'Filename': 'sensor.db', 'Data': Sensor_DB}
]
