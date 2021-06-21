import os

import click

from commands import (apex_export, apex_import, apex_nitro, create_import_sql,
                      github_commit)
from config import settings
from parameters import parameters_template


@click.group()
def apex_ei():
	pass


@apex_ei.command()
@click.option('--apex-nitro-project', prompt='Apex Nitro project')
@click.option('--export-connection', prompt='Export connection string')
@click.option('--export-user', prompt='Export user')
@click.option('--export-password', prompt='Export password', hide_input=True)
@click.option('--export-workspaceid', prompt='Export Workspace ID')
@click.option('--export-appid', prompt='Export App ID')
@click.option('--import-connection', prompt='Import connection string')
@click.option('--import-user', prompt='Import user')
@click.option('--import-password', prompt='Import password', hide_input=True)
@click.option('--import-schema', prompt='Import schema')
@click.option('--import-appid', prompt='Import App ID')
@click.option('--import-alias', prompt='Import App alias')
@click.option('--github-project', prompt='Github project')
@click.option('--github-branch', prompt='Github branch')
def init(
	apex_nitro_project,
	export_connection,
	export_user,
	export_password,
	export_workspaceid,
	export_appid,
	import_connection,
	import_user,
	import_password,
	import_schema,
	import_appid,
	import_alias,
	github_project,
	github_branch
):
	with open('settings.toml', 'w') as file:
		parameters = parameters_template.format(
			export_connection=export_connection,
			export_user=export_user,
			export_password=export_password,
			export_workspaceid=export_workspaceid,
			export_appid=export_appid,
			import_connection=import_connection,
			import_user=import_user,
			import_password=import_password,
			import_schema=import_schema,
			import_appid=import_appid,
			import_alias=import_alias,
			github_project=github_project,
			github_branch=github_branch
		)
		file.write(parameters)


@apex_ei.command()
@click.option('--commit-message', prompt='Github commit message')
def publish(commit_message):
	#os.system(apex_nitro.format({settings.APEXNITRO.PROJECT})
	apex_nitro_command = apex_nitro(settings.APEXNITRO.PROJECT)
	apex_export_command = apex_export(
		settings.EXPORT.CONNECTION_STRING,
		settings.EXPORT.USER,
		settings.EXPORT.PASSWORD,
		settings.EXPORT.WORKSPACEID,
		settings.EXPORT.APPLICATIONID
	)
	apex_export_split_command = apex_export(
		settings.EXPORT.CONNECTION_STRING,
		settings.EXPORT.USER,
		settings.EXPORT.PASSWORD,
		settings.EXPORT.WORKSPACEID,
		settings.EXPORT.APPLICATIONID,
		True
	)
	create_import_sql_command = create_import_sql(
		settings.IMPORT.SCHEMA,
		settings.IMPORT.APPLICATIONID,
		settings.IMPORT.ALIAS
	)
	github_commit_command = github_commit(
		settings.GITHUB.PROJECT,
		settings.GITHUB.BRANCH
	)
	apex_import_command = apex_import(
		settings.IMPORT.CONNECTION_STRING,
		settings.IMPORT.USER,
		settings.IMPORT.PASSWORD
	)

	os.system(apex_nitro_command)
	os.system(apex_export_command)
	os.system(apex_export_split_command)
	with open('import.sql', 'w') as file:
		file.write(create_import_sql_command)
	os.system(github_commit_command)
	os.system(apex_import_command)


if __name__ == '__main__':
	apex_ei()
