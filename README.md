odoo-elt
========

Odoo data manipulation, like an small ELT (Extract, Load, Transform) for odoo databases.

The main idea of the project is to give functional users the availability to move data from one odoo database to another odoo database. The design is quite simple, it use native odoo methods (primarily load and export_data).

The aim of this project is different from odoo migration or OpenUpgrade, it allows to start from a clean database, merging  different odoo databases into a single multicompany db, etc.

This project was developed by a non developer so for sure you are gonna find lot of ugly statements and ideas.

It was developed using xmi2oerp tool, thanks Cristian Sebastian Rocha for that great work!

You can see an ugly example video in the following link http://youtu.be/01nEOFoHeus, in this example we are going to show how to move data from a v6.1 database with demo data to a trunk database without demo data.

Any feedback is welcome, if someone likes the idea, please don't hesitate to contact us so we can work together.
