parameters_template = '''#Export parameters
[APEXNITRO]
PROJECT="{apex_nitro_project}"
[EXPORT]
CONNECTION_STRING="{connection_string}"
USER="{export_user}"
PASSWORD="{export_password}"
WORKSPACEID={export_workspaceid}
APPLICATIONID={export_appid}

#Import Paramaters
[IMPORT]
CONNECTION_STRING="{connection_string}"
USER="{import_user}"
PASSWORD="{import_password}"
SCHEMA="{import_schema}"
APPLICATIONID={import_appid}
ALIAS="{import_alias}"

#DDL Parameters
[DDL]
CONNECTION_STRING="{connection_string}"
USER="{ddl_user}"
PASSWORD="{ddl_password}"
OWNER="{ddl_onwer}"
PREFIX="{ddl_prefix}"

#Github Parameters
[GITHUB]
PROJECT="{github_project}"
BRANCH="{github_branch}"
'''
