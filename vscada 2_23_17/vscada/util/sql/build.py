#!/usr/bin/env python3

import argparse
import csv
import sqlite3
import os

#import database schema
from schema import *

DB_PATH = '../../data/sql/'
CSV_PATH = './csv/'

#accepts descriptive dictionary, sql_db cursor
def create_table(table_dict, sql_db):
	print("Creating Table: ", table_dict['Table'])
	
	#create table SQL query
	#  fields read from dict
	sql_query = 'CREATE TABLE ' + table_dict['Table'] + '(\n'
	for column in table_dict['Field_List']:
		sql_query += column['Field'] + ' ' + column['Type'] + ',\n'
	if 'Foreign Key' in table_dict:
		for fkey, fvalue in table_dict['Foreign Key']:
			sql_query += 'FOREIGN KEY(' + fkey + ') REFERENCES '
			sql_query += fvalue + ' ON DELETE CASCADE ON UPDATE CASCADE,\n'
	sql_query = sql_query[:-2] #remove comma, newline
	sql_query += '\n);'
	#execute sql commmand
	sql_db.execute(sql_query)

def populate_table(table_dict, sql_db):
	print("Populating Table:", table_dict['Table']) 
	
	#csv filename from table name, directory
	filename = CSV_PATH + table_dict['Table'] + '.csv'
	
	#check if csv file exists
	if not os.path.isfile(filename):
		print("Creating Empty CSV: ", filename)
		
		#file does not exist, create one
		with open(filename, 'w', newline='') as csv_file:
			#csv formatter using: "A", "B", "C"...
			table_writer = csv.writer(csv_file)
			
			#create title row for csv
			sql_head = []
			for field in table_dict['Field_List']:
				sql_head.append(field['Field'])
			
			#write row to database
			table_writer.writerow(sql_head)
	else:
		#file already exists, populate database
		with open(filename, newline='') as csv_file:
			#csv formatter using: "A", "B", "C"...
			table_reader = csv.reader(csv_file)
			
			#skip csv header row
			next(table_reader, None)
			
			#add all other rows to database
			for row in table_reader:
				#generate list of table fields for sql query
				field_list = '('
				for field in table_dict['Field_List']:
					field_list += field['Field'] + ', '
				field_list = field_list[:-2] #remove comma, space
				field_list += ')'
				data_list = '('
				
				#generate list of values to be added for sql query 
				for field in row:
					data_list += field + ', '
				data_list = data_list[:-2] #remove comma, space
				data_list += ')'
				
				#sql insert query
				sql_query = 'INSERT INTO ' + table_dict['Table'] + \
						' ' + field_list + ' VALUES ' + data_list
				
				print('\t', sql_query)
				sql_db.execute(sql_query)
				
def check_path(path):
	if not os.path.exists(path):
		check_ok = input('Creating Path: \'' + CSV_PATH + '\' (Y/N)? ')
		if check_ok.upper() == 'Y':
			os.makedirs(path)
		else:
			print('ABORT')
			exit()

def create_db():
	#check before deleting files
	check_ok = input('WARNING: This will delete all sql data, continue (Y/N)? ')
	if  check_ok.upper() == 'Y':
		#check if sql path exits
		check_path(DB_PATH)

		#check if CSV_PATH exists
		check_path(CSV_PATH)
		
		#iterate through SQLite *.db files 
		for sql_file in SQL_List:
			#SQLite database filename
			filename = DB_PATH + sql_file['Filename']
			
			#delete old *.db file (if exists)
			os.remove(filename) if os.path.exists(filename) else None
			
			#iterate through each table in 'filename'
			for table in sql_file['Data']:
				#open SQLite connection
				sql_db = sqlite3.connect(filename)
				cur = sql_db.cursor()
				
				#create SQL table
				create_table(table, cur)
				
				#fill SQL table with values
				populate_table(table, cur)
				
				#save SQL changes
				sql_db.commit()
				sql_db.close()
	else:
		#user did not say 'Y' or 'y', abort
		print('ABORTED')
	
def save_db(dirname):
	#check if sql path exits
	check_path(DB_PATH)

	#iterate through SQLite *.db files 
	for sql_file in SQL_List:
		#SQLite database filename
		filename = DB_PATH + sql_file['Filename']
			
		conn = sqlite3.connect(filename)
		c = conn.cursor()
		c.execute('SELECT name FROM sqlite_master WHERE type="table"')
		
		table_list = c.fetchall()
		for table in table_list:
			table_name = table[0]
			print('Table ' + table_name)
			c.execute('SELECT * FROM ' + table_name)
			csv_head = list(map(lambda x: x[0], c.description))
			row_list = c.fetchall()
			for row in row_list:
				print(list(row))
			filename = 'sav/' + dirname + '/' + table_name + '.csv'
			with open(filename, 'w', newline='') as csv_file:
				#csv formatter using: "A", "B", "C"...
				table_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
				
				#write row to database
				table_writer.writerow(csv_head)
				
				for row in row_list:
					table_writer.writerow(list(row))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
			description="VSCADA SQLite Database Parser: create, save, load, and restore database schema")
	fileMode = parser.add_mutually_exclusive_group(required=True)
	fileMode.add_argument("-l","--load", metavar='dir', type=str,
			help="load a saved database values")
	fileMode.add_argument("-s", "--save", metavar='dir', type=str,
			help="save current database values")
	fileMode.add_argument("-d", "--default", action="store_true",
			help="load the default database values")
	parser.add_argument("-q", "--quiet", action="store_true")
	args = parser.parse_args()
	
	if args.default:
		print('DEFAULT...')
		create_db()
	elif args.load:
		print('SAVING...')
		load_db(args.load)
	elif args.save:
		print('SAVING...')
		save_db(args.save)
	else:
		print("Error, Command not understood, use -h for help")
