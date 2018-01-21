# Madisonbold459@gmail.com
#Logs Analysis project in the Udacity Full Stack Web Developer Nanodegree.
Running this python file will yield the results of the following queries: 

1.  What are the most popular three articles of all time?
2.  Who are the most popular article authors of all time?
3.  On which days did more than 1% of requests lead to errors?

Open output.txt to see a dump of the expected output after running log.py.

# Setup
## Software
Make sure the following programs are installed on your computer.  In brackets I have listed the versions I am using for this project.

[Python 3.6.x]  (https://www.python.org/downloads/)

[PostgreSQL 9.5.10]   (https://www.postgresql.org/download/)

# Test data
Download and extract files from [newsdata.zip]
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip 
Build the database by running ```psql -d news -f newsdata.sql```


```
psql -d news
```
SQL query for # 1. Top articles and views.
'''
  SELECT articles.title, count(articles.title)
  FROM articles
  JOIN log
  ON CONCAT('/article/',articles.slug) = log.path
  GROUP BY articles.title
  ORDER BY count DESC
  LIMIT 3;
'''

SQL query for # 2. Top article authors and views.
'''
  SELECT authors.name, count(authors.id) AS views
  FROM log, authors, articles
  WHERE log.path != '/' AND 
  articles.slug = SUBSTR(log.path, LENGTH('/article/') +1) 
  AND articles.author = authors.id
  GROUP BY authors.name, authors.id 
  ORDER BY views DESC;
'''
  
SQL query for # 3. On which days did more than 1% of requests lead to errors?
```
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
```

# How to run the application

Here's a couple of alternatives on how to run the application.

## Using command prompt

### cd into the project folder
Open a command prompt and navigate to the Vagrant folder

### Run the application
Type

```
python3 log.py
```

## Using the Python IDLE
* File --> Open...
* Navigate to log.py
* OK

A new windows pops up, in that window:
* Select Run --> Run Module
