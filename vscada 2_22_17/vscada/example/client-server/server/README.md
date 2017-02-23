# VSCADA TCP protocol Overview #

## Overview ##
VSCADA implements a client-server model. The server is passive. The header and data structure is introduced here. 

## Format ##
**Header:**
```
class_type-action_type:{argument_key:[argument_value]}
```

### class_type ###
SQL:		for reading and writing configuration information stored in SQL database. 

RRD:		for reading raw and calibrated data stored in RRD database

Massage:	for reading most recent system logs

### action_type ###
used by client:
	GET
	SET
	CREATE

Used by server:
	RETURN

### argument_type ###
type
name
value
data