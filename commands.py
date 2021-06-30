def apex_nitro(project_name):
	return f'apex-nitro publish {project_name}'


def apex_export(connection_string, user, password, workspaceid, applicationid, split=False):
	return (
		f"java oracle.apex.APEXExport "
		f"-db {connection_string} "
		f"-user {user} "
		f"-password {password} "
		f"-workspaceid {workspaceid} "
		f"-applicationid {applicationid} "
		f"{'-split' if split else ''} "
		"-dir apex-export"
	)


def github_commit(message, branch):
	return (
		f'git add . && git commit -m "{message}" && git push origin {branch}'
	)


def apex_import(connection_string, user, password):
	return f'sql {user}/{password}@{connection_string} @import.sql'


def create_import_sql(schema,applicationid,alias):
	return (
		"begin\n"
		f"	apex_application_install.set_workspace('{schema.upper()}');\n"
		f"	apex_application_install.set_application_id({applicationid});\n"
		f"	apex_application_install.generate_offset;\n"
		f"	apex_application_install.set_application_alias( '{alias}' );\n"
		"end;\n"
		"/\n"
		f"@apex-export/f{applicationid}.sql\n"
		"quit;"
	)

def get_ddl_query(owner, prefix=''):
	return '''
		select dbms_metadata.get_ddl(
				 OBJECT_TYPE,
				 OBJECT_NAME,
				 OWNER
			   ) as "ddl",
			   OBJECT_NAME as "name",
			   OBJECT_TYPE as "type"
		from ALL_OBJECTS
		WHERE OWNER = upper('{}')
		and OBJECT_TYPE not in ('LOB','JOB','PACKAGE BODY','INDEX')
		and OBJECT_NAME not like ('APEX$%')
		and (OBJECT_NAME like upper('{}%') or '{}' = '')
		order by case 
					when OBJECT_TYPE = 'TABLE'    then 0
					when OBJECT_TYPE = 'INDEX' then 1
					when OBJECT_TYPE = 'SEQUENCE' then 2
					when OBJECT_TYPE = 'VIEW' then 3
					else 4
				end, OBJECT_TYPE, OBJECT_NAME
	'''.format(owner, prefix, prefix)

def get_ddl_options():
	return '''
	begin
		DBMS_METADATA.set_transform_param (DBMS_METADATA.session_transform, 'SQLTERMINATOR', true);
		DBMS_METADATA.set_transform_param (DBMS_METADATA.session_transform, 'PRETTY', true);
		DBMS_METADATA.set_transform_param (DBMS_METADATA.session_transform, 'SEGMENT_ATTRIBUTES', false);
		DBMS_METADATA.set_transform_param (DBMS_METADATA.session_transform, 'STORAGE', false);
	end;
	'''

def get_ddl_template(object_type, object_name, object_ddl):
	return (
		f'--{object_type}: {object_name}--------------------------------------------------------\n'
		f'{object_ddl}\n'
		'--------------------------------------------------------------------------------\n'
	)