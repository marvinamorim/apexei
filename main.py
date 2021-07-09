import os

import click

from commands import (apex_export, apex_import, apex_nitro, create_import_sql,
                      github_commit)
from config import settings
from parameters import parameters_template
from ddl_export import create_ddls


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


def commit_message(ctx, param, github):
	if github:
		message = click.prompt('Github commit message')
		return message



@apex_ei.command()
@click.option('--nitro/--no-nitro',   is_flag=True, default=True, help="Publish apex-nitro static files. Default: True")
@click.option('--single/--no-single', is_flag=True, default=True, help="Export single file application sql. Default: True")
@click.option('--split/--no-split',   is_flag=True, default=True, help="Export split files application sql. Default: True")
@click.option('--ddl/--no-ddl',   	  is_flag=True, default=True, help="Export DDL files for this application. Default: True")
@click.option('--github/--no-github', is_flag=True, default=False, help="Commit and push changes to github. Default: True", callback=commit_message)
@click.option('--import-sql/--no-import-sql', is_flag=True, default=False, help="Import application on production environment. Default: False")
def publish(nitro, single, split, ddl, github, import_sql):
	#Export Apex-nitro static files
	if nitro and settings.APEXNITRO.PROJECT:
		apex_nitro_command = apex_nitro(settings.APEXNITRO.PROJECT)
		click.echo("*****Publishing static files into development environment...")
		os.system(apex_nitro_command)
	#Generate Apex single file export
	if single and settings.EXPORT.CONNECTION_STRING:
		apex_export_command = apex_export(
			settings.EXPORT.CONNECTION_STRING,
			settings.EXPORT.USER,
			settings.EXPORT.PASSWORD,
			settings.EXPORT.WORKSPACEID,
			settings.EXPORT.APPLICATIONID
		)
		click.echo("*****Exporting single file from Apex Application...")
		os.system(apex_export_command)
	#Generate Apex split files export
	if split and settings.EXPORT.CONNECTION_STRING:
		apex_export_split_command = apex_export(
			settings.EXPORT.CONNECTION_STRING,
			settings.EXPORT.USER,
			settings.EXPORT.PASSWORD,
			settings.EXPORT.WORKSPACEID,
			settings.EXPORT.APPLICATIONID,
			True
		)
		click.echo("*****Exporting explit files from Apex Application...")
		os.system(apex_export_split_command)
	if import_sql and settings.IMPORT.CONNECTION_STRING:
		#Generate import sql file to sync application into prod env
		create_import_sql_command = create_import_sql(
			settings.IMPORT.SCHEMA,
			settings.IMPORT.APPLICATIONID,
			settings.IMPORT.ALIAS
		)
		click.echo("*****Generating import file to be imported on production environment...")
		with open('import.sql', 'w') as file:
			file.write(create_import_sql_command)
		#Import application on prod env
		apex_import_command = apex_import(
			settings.IMPORT.CONNECTION_STRING,
			settings.IMPORT.USER,
			settings.IMPORT.PASSWORD
		)
		click.echo("*****Importing application on production environment...")
		os.system(apex_import_command)
	#Export DDL files
	if ddl:
		click.echo("*****Exporting DDL files...")
		create_ddls()
	#Commit and push alterations into github
	if github:
		github_commit_command = github_commit(
			github,
			settings.GITHUB.BRANCH
		)
		click.echo("*****Publishing changes into Github...")
		os.system(github_commit_command)


if __name__ == '__main__':
	apex_ei()
