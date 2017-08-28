# python2.7
#
# Small script to analyse a database for Udacity's Intro to Programming Nanodegree.
#

import psycopg2

# imported from https://pypi.python.org/pypi/tabulate. Thanks to Sergey Astanin. Makes lists readable.
from tabulate import tabulate


def top_articles(conn):
    """
    Executes the Query for the top 5 articles sorted from most popular according to total no of views

    :param conn: Connection to the database
    :return: returns results table as list and according headers for their interpretation
    """

    result_headers = ["Article Name", "Number views"]

    cursor = conn.cursor()
    cursor.execute("""select articles.title, count(log.path) as num
                    from articles 
                    right join log on log.path like '%' || articles.slug
                    where log.path != '/' and log.status = '200 OK'
                    group by articles.title
                    order by num desc
                    limit 5;""")
    result_data = cursor.fetchall()

    return result_data, result_headers


def top_authors(conn):
    """
    Executes the Query for the top 5 authors sorted from most popular according to total no of views

    :param conn: Connection to the database
    :return: returns results table as list and according headers for their interpretation
    """

    result_headers = ["Author's Name", "Number views"]

    cursor = conn.cursor()
    cursor.execute("""select authors.name, count(log.path) as num
                    from articles
                    left join authors on articles.author = authors.id
                    right join log on log.path like '%' || articles.slug
                    where log.path != '/' and authors.name != '' and log.status = '200 OK'
                    group by authors.name
                    order by num desc
                    limit 5;""")
    result_data = cursor.fetchall()

    return result_data, result_headers


def top_article_errors(conn):
    """
    Executes the Query for all days that have above 1% '404 error' rate on visited sites

    :param conn: Connection to the database
    :return: returns results table as list and according headers for their interpretation
    """

    result_headers = ["Date", "404 Error rate"]

    cursor = conn.cursor()
    cursor.execute(""" select time::date, sum(percent_total) 
                    from (select log.time::date, 
                        round( 100.0 * sum( case when status = '404 NOT FOUND' then 1 else 0 end) / 
                        count(status), 2) as percent_total
                        from log
                        group by log.time::date) as percent_query
                    where percent_total >= 1.0
                    group by time::date
                    order by sum(percent_total) desc;""")
    result_data = cursor.fetchall()

    return result_data, result_headers


def main():
    """
    The main function takes and returns no arguments.
    It initializes the database connection and runs all analyses of the db, printing them on the command line
    :return: -
    """

    try:
        conn = psycopg2.connect("dbname='news'")
    except:
        print "I am unable to connect to the database"
        return

    print ("\n\n These are the top 5 articles to date: \n")
    result_data, result_headers = top_articles(conn)
    print tabulate(result_data, headers=result_headers)

    print ("\n\n These are the top 5 authors to date: \n")
    result_data, result_headers = top_authors(conn)
    print tabulate(result_data, headers=result_headers)

    print ("\n\n The articles resulting in most error cases are: \n")
    result_data, result_headers = top_article_errors(conn)
    print tabulate(result_data, headers=result_headers)

    conn.close()

main()
