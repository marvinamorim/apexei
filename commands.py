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