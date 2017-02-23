import json

cmd = ('SQL GET {"fields":["id","Name","id_CAN","key_Type"],' +
	   '"table":"Sensor","constraints":["lol","blah","what"],' +
	   '"values":[1,3,2]}')
cmd = cmd.split(' ')
class_type     = cmd[0]
action_type    = cmd[1]
request_params = json.loads(cmd[2]) 
print(json.dumps(request_params, sort_keys=True, indent=4))
query = ''
query = query + 'SELECT ' 
for field in request_params['fields']:
	query = query + field + ', '
if len(request_params['fields']) > 0:
	query = query[:-2]
else:
	query = query + '*'
query = query + ' FROM '
query = query + request_params['table'] + ' WHERE '
for constraint in request_params['constraints']:
	query = query + constraint + '=?' + ' AND '
if len(request_params['constraints']) > 0:
	query = query[:-4]
print(query)