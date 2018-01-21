#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""This is the third project in Udacity's Full Stack Web Developer Nanodegree.

Running the python file will display the results of three database queries:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?
"""

import sys
import psycopg2
# Establish a name for the database to connect to queries

DBNAME = "news"


def pop_articles():
    """Public function connects to database and prints results of SQL query."""
    conn = None
    """Creates a database connection and prints information based on view queries
    """
    try:
        conn = psycopg2.connect(database=DBNAME)
        cur = conn.cursor()
        query = """
            SELECT articles.title, count(articles.title)
            FROM articles
            JOIN log
            ON CONCAT('/article/',articles.slug) = log.path
            GROUP BY articles.title
            ORDER BY count DESC
            LIMIT 3;
            """
        cur.execute(query)

# Print query, results, extra line for ease of reading
        print("The most popular 3 articles of all time are: ")
        for (articles, log) in cur.fetchall():
            print(" {} - {} views".format(articles, log))
        print("*************** END OF QUERY ***********")

        cur.close
    except (psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    """ Close cursor and database connections.
    """

# Execute second query: most popular article authors of all time


def pop_authors():
    """Function connects to database and retuns result of SQL query."""
    conn = None
    try:
        conn = psycopg2.connect(database=DBNAME)
        cur = conn.cursor()
        query = """
            SELECT authors.name, count(authors.id) AS views
            FROM log, authors, articles
            WHERE log.path != '/' AND
            articles.slug = SUBSTR(log.path, LENGTH('/article/') +1)
            AND articles.author = authors.id
            GROUP BY authors.name, authors.id
            ORDER BY views DESC
            LIMIT 3;

            """
        cur.execute(query)
        print("The most popular article authors of all time are: ")
        for (name, id) in cur.fetchall():
            print(" {} - {} views".format(name, id))
        print("*************** END OF QUERY ***********")

        cur.close
    except (psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    """    Close cursor and database connections
    """


def errors():
    """Execute third query and display days with error % greater than 1."""
    conn = None
    try:
        conn = psycopg2.connect(database=DBNAME)
        cur = conn.cursor()
        query = """
            WITH M AS
                (SELECT DATE(log.time) AS faildate,
                ROUND((SUM(CASE WHEN
                    SUBSTRING(log.status, 0, 4)::INTEGER >= 400
                    THEN 1
                    ELSE 0
                    END
                )  * 100.0)::DECIMAL /
                (COUNT(log.status)), 1) AS totalfail
                FROM log GROUP BY DATE(log.time)
                )
            SELECT CONCAT(M.totalfail, '%') AS fail,
            TO_CHAR(M.faildate, 'FMMonth FMDD, YYYY') AS date
            FROM M
            WHERE M.totalfail > 1
            """
        cur.execute(query)
        print("There were greater than 1% errors on the following days:")
        for (row) in cur.fetchall():
            print(row)
        print("*************** END OF QUERY ***********")
        cur.close
    except (psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    pop_articles()
    pop_authors()
    errors()
    """Executes each of the queries shown above and prints results.
    """

""""
    Websites used:
    https://docs.microsoft.com/en-us/sql/t-sql/functions/
    aggregate-functions-transact-sql
    https://www.pythonlearn.com/html-008/cfbook015.html
    http://www.postgresqltutorial.com/postgresql-python/query/
    http://www.postgresqltutorial.com/postgresql-python/
    https://pythonspot.com/python-database-postgresql/
    https://www.postgresql.org/docs/9.5/static/sql-createview.html
    http://www.postgresqltutorial.com/postgresql-python/call-stored-procedures/
    https://www.postgresql.org/docs/9.1/static/functions-string.html
"""
