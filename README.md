# APEX Export Import (ApexEI)
This is a personal project aiming to help git version control and export/import the apex applications between development and production environments.

To achieve this, 4 different CLI are being used:
* apex-nitro
* APEXEport
* sqlcl
* git


## To do:
* Create installation and usage guide
* Make accept an array of elements over APEXNITRO.PROJECT, EXPORT.APPLICATIONID, IMPORT.APPLICATIONID, IMPORT.ALIAS, to deal with several Apex applications over the same github project.
* Create parameter for custom path for APEXExport files and DDL export.