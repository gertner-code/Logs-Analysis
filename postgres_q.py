#!/usr/bin/env python3


"""
A logs anaylsis answering 3 different requests with a single query each.
"""


import psycopg2


class My_base:
    """Class for use with databases"""
    def __init__(self, dbname):
        """Initiate the My_base class"""
        self.dbname = dbname
        self.db = 'None'
        self.c = 'None'

    def db_connect(self):
        """Connect to provided database, check connection."""
        try:
            self.db = psycopg2.connect(database=self.dbname)
        except DatabaseError:
            print("I am unable to connect to the database")
            exit()

        self.c = self.db.cursor()

    def execute_query(self, query):
        """Call db_connect, recieve a query. Return the result of query"""
        self.c.execute(query)
        answer = self.c.fetchall()
        return answer

    def close(self):
        """Close database"""
        self.db.close()


def print_top_articles():
    """Send query to find top 3 articles""""
    print("What are the most popular three articles of all time?")
    articles = conn.execute_query("""SELECT articles.title, count(*) AS views
                                FROM articles INNER JOIN log
                                ON log.path = '/article/' || articles.slug
                                WHERE log.status LIKE '%200%'
                                GROUP BY articles.title
                                ORDER BY views DESC LIMIT 3;""")

    for article in articles:
        print(article[0], "--", article[1], " views")

    print("")


def print_top_authors():
    """Send query to find top authors"""
    print("Who are the most popular article authors of all time?")
    authors = conn.execute_query("""SELECT authors.name, count(*) AS views
                               FROM articles INNER JOIN
                               authors ON articles.author = authors.id
                               INNER JOIN log
                               ON log.path = '/article/' || articles.slug
                               WHERE log.status LIKE '%200%'
                               GROUP BY authors.name
                               ORDER BY views DESC;""")

    for author in authors:
        print(author[0], "--", author[1], " views")

    print("")


def print_error_rate():
    """Send query to find days with over 1% error rate"""
    print("On which days did more than 1% of requests lead to errors?")

    errors = conn.execute_query("""SELECT dates,
                              CONCAT(ROUND(((errornum + 0.0) / (total + 0.0)
                              * 100 ), 1), '%') AS errors
                              FROM (SELECT DATE(time) AS day, count(*) AS total
                              FROM log GROUP BY DATE(time)) AS one
                              INNER JOIN
                              (select DATE(time) AS dates,
                              count(*) AS errornum FROM log
                              WHERE status NOT LIKE '200%'
                              GROUP BY DATE(time)) AS two
                              ON two.dates = one.day WHERE (errornum +0.00) /
                              (total + 0.00) >= .01;""")

    for error in errors:
        print('{:%B %d, %Y} -- {} errors'.format(error[0], error[1]))

    print("")


if __name__ == '__main__':
    """Runs only if module is executed directly"""
    conn = My_base("news")
    conn.db_connect()
    print_top_articles()
    print_top_authors()
    print_error_rate()
    conn.close()
