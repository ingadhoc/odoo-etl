[![Build Status](https://travis-ci.org/ingadhoc/odoo-etl.svg?branch=8.0)](https://travis-ci.org/ingadhoc/odoo-etl)
[![Coverage Status](https://coveralls.io/repos/ingadhoc/odoo-etl/badge.png?branch=8.0)](https://coveralls.io/r/ingadhoc/odoo-etl?branch=8.0)

#odoo-etl

Odoo data manipulation, like an small ETL (Extract, Transform and Load) for odoo databases.

The main idea of the project is to give functional users the availability to move data from one odoo database to another odoo database. The design is quite simple, it use native odoo methods (primarily load and export_data).

The aim of this project is different from odoo migration or OpenUpgrade, it allows to start from a clean database, merging  different odoo databases into a single multicompany db, etc.

This project was developed by a non developer so for sure you are gonna find lot of ugly statements and ideas.

It was developed using xmi2oerp tool, thanks Cristian Sebastian Rocha for that great work!

You can see an ugly example video in the following links, in this example we are going to show how to move data from a v6.1 database with demo data to a trunk database without demo data. Links:
* https://www.youtube.com/watch?v=HZQQaNQ9k7U
* https://www.youtube.com/watch?v=VmScwCM3whg
* https://www.youtube.com/watch?v=PS2ShlY1gLI

Any feedback is welcome, if someone likes the idea, please don't hesitate to contact us so we can work together.

You can find some kind of tutorial on: https://docs.google.com/document/d/1HWERCUp9rMHqEibT7B_mfu9jePV-FBkYbo--OB0jXqA
