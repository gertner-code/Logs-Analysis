# Logs Analysis

## Project Description
* Contains a class designed for accessing a database and querying it
* Class must be initialized with database name
* Methods output the answers to the following queries upon the file being run
  * What are the most popular three articles of all time?
  * Who are the most popular article authors of all time?
  * On which days did more than 1% of requests lead to errors?

## Requirements
### To begin all of the following must be installed
* PostgreSQL
* Python 3
* psycopg2

## Database Setup
1. open the terminal to the location where the unzipped files are located
1. enter: sudo -u postgres createuser --interactive (vagrant is listed in the .sql file)
1. enter vagrant when prompted for name of role and y for superuser
1. enter sudo -u postgres createdb news   (to create a database)
1. enter psql -d news -f newsdata.sql   (to import the data from the included file)
1. enter psql -d news   (to open the database)
1. enter \dt    (if no tables present check previous steps else you are now setup)
1. enter python3 postgres_q.py (runs file )

The file should output each question with the answers queried from the db on
the following lines.
