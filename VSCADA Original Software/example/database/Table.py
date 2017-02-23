import sqlite3
import csv

Database = 'Test.db'

db = sqlite3.connect(Database);

cursor = db.cursor()

# cursor.execute('drop table sensorList')

# cursor.execute('drop table mainList')

create_sensorTable = "CREATE TABLE sensor_table(id integer, name text, id_CAN integer, id_Sensor integer, Type integer, Sample_rate integer, Overwrite_peroid integer, Units text, Factor integer, Offset integer, RRD_DB text);"

create_sensorType = "CREATE TABLE sensor_type(id integer, Description text, type text, direction text)"

create_sensorLevel = "CREATE TABLE sensor_level(id integer, warning_low integer, warning_high integer, error_low integer, error_high integer, fail_low integer, fail_high integer )" 

create_sensorActions = "CREATE TABLE sensor_actions(id integer, action_name text, priority_level text, effector_name text, effector_state text)"


cursor.execute(create_sensorTable)
cursor.execute(create_sensorType)

cursor.execute(create_sensorLevel)

cursor.execute(create_sensorActions)





db.commit()
