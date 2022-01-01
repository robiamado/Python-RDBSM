# Python RDBSM

## Introduction

A tool introducing relation database management in Python as desktop application.
A pydb is a class with rows,cols and elems_matrix attributes.

- rows and cols are two 1-dimensional arrays and represent rows and coloumns.
- elems_matrix is a 2-dimensional array and represent db elements.



## Release Notes:

- 1.0.0 Initial Release
	
## Requirements

- Python >=3.9

## Install

No install available package is released as source code.

## Methods

**\_\_init\_\_**

A database is created giving a name as input parameter. If the database already exists it is imported from existing .pydb file with corresponding name.

**\_\_repr\_\_**

Meethod is used to print the database using a tabular form.

**log**

Method is called each time any modify is performed on database and it logs each activity using date-time,process,description format in .log extension.

**save**

Saves db instance as .pydb file in '../dbs' folder which is located in root folder. Cannot use $,%,&,# symbols in any entrance of any db arguments.

**delete**

Delete corresponding .pydb file.

**read**

Used to read db data. Accepts only one argument and returns corresponding row, coloumn or element.

**write**

Used to write db data directly to .pydb file. Accepts multiple arguments and can save:

- rows (row=)
- coloumns (cols=)
- elements on a rows (rows=,elems=)
- elements on a coloumns (cols=,elems=)
- a single element on rows and coloumns (rows=,cols=,elems=)

**imports**

Used to import other extensions files and be used as pydb. Method is called automatically on any class instance to import exisitng saved data. 

- .csv files are imported with empty rows. The first line is interpreted as cols and each other line is added as elements.

**format unformat**

Methods used to format and unformat .pydb and other imported extensions files data.

**add**

Used to add data to db. Accepts multiple arguments:

- rows (row=)
- coloumns (cols=)
- elements on a rows (rows=,elems=)
- elements on a coloumns (cols=,elems=)
- a single element on rows and coloumns (rows=,cols=,elems=)

**get**

Used to get data from db, returns the arguments values. Accepts multiple arguments:

- rows (row=)
- coloumns (cols=)
- elements on a rows (rows=,elems=)
- elements on a coloumns (cols=,elems=)
- a single element on rows and coloumns (rows=,cols=,elems=)

**remove**

Used to remove data from db. Accepts multiple arguments:

- rows (row=)
- coloumns (cols=)
- elements on a rows (rows=,elems=)
- elements on a coloumns (cols=,elems=)
- a single element on rows and coloumns (rows=,cols=,elems=)

## Contacts

robiamado@gmail.com
