INTRODUCTION
------------

The program is designed to connect to an existing database (news.sql) 
and use the stored logs for a quick analysis of top articles, 
top authors and top days where 404 errors occured to users.

No changes to the database are being made!

REQUIREMENTS
------------

This module requires the following modules:

Database: - news.sql (https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
Libraries: - tabulate (https://pypi.python.org/pypi/tabulate) to make the output easier readable.


CONFIGURATION
-------------

For ease of use it is assumed that the script is to be paired with the database provided.
To increase the number of "Top X articels/ authors" provided by the script, the search query is to be adapted.

An example output with default configuration can be found in the attached example_output.txt
