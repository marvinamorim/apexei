import cx_Oracle
from commands import (get_ddl_query, get_ddl_options, get_ddl_template)
import os
import shutil
from config import settings


def output_type_handler(cursor, name, default_type, size, precision, scale):
	if default_type == cx_Oracle.DB_TYPE_CLOB:
		return cursor.var(cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize)
	if default_type == cx_Oracle.DB_TYPE_BLOB:
		return cursor.var(cx_Oracle.DB_TYPE_LONG_RAW, arraysize=cursor.arraysize)


def tuple_to_dict(cursor):
    columnNames = [d[0] for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow


def check_ddl_folder():
	print("Checking of ddl folder exists")
	if not os.path.isdir('ddl'):
		os.makedirs('ddl')
		return True
	return False


def clear_ddl_dir():
	if check_ddl_folder():
		return
	for root, dirs, files in os.walk('ddl'):
		for f in files:
			os.unlink(os.path.join(root, f))
		for d in dirs:
			shutil.rmtree(os.path.join(root, d))


def create_object_file(object_type, object_name, object_ddl):
	#check if folder already exists, if not, create
	filename = f'ddl\\{object_type}_{object_name}.sql'
	print("Creating new/changed file:", filename)
	object_file = open(filename, "w")
	object_file.write(object_ddl)
	object_file.close()


def create_ddls():
	clear_ddl_dir()
	print("Getting WMS schema objects ddl")
	conn_str = (
		f'{settings.DDL.USER}/{settings.DDL.PASSWORD}@'
		f'{settings.DDL.CONNECTION_STRING}'
	)
	con = cx_Oracle.connect(conn_str)
	con.outputtypehandler = output_type_handler
	cur = con.cursor()
	query = get_ddl_query(settings.DDL.OWNER, settings.DDL.PREFIX)
	cur.execute(get_ddl_options())
	data = cur.execute(query)
	data.rowfactory = tuple_to_dict(data)
	ddls = [row for row in data]
	filename = "ddl\\0_SINGLE_FILE_DDL.sql"
	print("Creating single file", filename)
	single_file = open(filename, "w")
	for row in ddls:
		ddl = get_ddl_template(
			object_type=row["type"],
			object_name=row["name"],
			object_ddl=row["ddl"].strip()
		)
		single_file.write(ddl)
		create_object_file(
			object_type=row["type"],
			object_name=row["name"],
			object_ddl=row["ddl"].strip()
		)
	single_file.close()
