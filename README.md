

### DATABASE:
Using inplace Database named "News" we are provided with three tables
  1. Authors
  2. Title
  3. Log

### Schema of Tables
#### Authors:
```
|Column |  #Type  |   #Modifiers                       
--- | ---  --- | ---  --- | ---
name   | text    | not null
bio    | text    | 
id     | integer | not null default nextval('authors_id_seq'::regclass)
Indexes:
    "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)
    '''
```
#### Articles:
```
 Column |           Type           |                       Modifiers                       
--------+--------------------------+-------------------------------------------------------
 author | integer                  | not null
 title  | text                     | not null
 slug   | text                     | not null
 lead   | text                     | 
 body   | text                     | 
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('articles_id_seq'::regclass)
Indexes:
    "articles_pkey" PRIMARY KEY, btree (id)
    "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
Foreign-key constraints:
    "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)
```

#### Log:
```
 Column |           Type           |                    Modifiers                     
--------+--------------------------+--------------------------------------------------
 path   | text                     | 
 ip     | inet                     | 
 method | text                     | 
 status | text                     | 
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
    "log_pkey" PRIMARY KEY, btree (id)
``` 
Uisng these three tables we need to get answers to three questions by using Pyhton Script
#### Questions

##### 1. What are the most popular three articles of all time?

_Using Logs table created view named **title** using following query which performs **string operation**  on path of article and results title of article._ 
```
Crated a view named **title** using following Query
  SELECT "substring"(log.path, 10) AS "substring",+
     log.status,                                  +
     log.id,                                      +
     log."time"                                   +
    FROM log;
```
_Joined title table with articles table and extracted top three article of all time_
```
select b.title, count(a.status) 
        from title a join articles b 
        on a.substring = b.slug 
        group by a.substring, b.title 
        order by count desc limit 3;
```


##### 2. Who are the most popular article authors of all time?
_Created a view **top_3_articles** using following query to get top 3 articles(Query of Question 1)_
```
  SELECT b.title,                                   +
     count(a.status) AS count                       +
    FROM (title a                                   +
      JOIN articles b ON ((a."substring" = b.slug)))+
   GROUP BY a."substring", b.title                  +
   ORDER BY (count(a.status)) DESC                  +
  LIMIT 3;
(1 row)
```
_Used following query to join **authors** with **articles** and then with **top_3_articles** to get **Authors** of top 3 titles_
```
select distinct a.name, b.title 
              from authors a inner join articles b on a.id = b.author 
              right join top_3_authors c on b.title = c.title;
```


##### 3. On which days did more than 1% of requests lead to errors?
_Created a view **Percentage1** to get total number of requests on a single day_
```
  SELECT count(log.status) AS count,+
     date(log."time") AS date       +
    FROM log                        +
   GROUP BY (date(log."time"));
```
_Created view **error_code** to get number of requests resulted in error on a day_
```
  SELECT count(log.status) AS count,   +
     date(log."time") AS date          +
    FROM log                           +
   WHERE (log.status <> '200 OK'::text)+
   GROUP BY (date(log."time"));
```
_Used following query to calcuate percentage and select row with more than 1% errors_
```
select * from ("
              "select error_code.date, "
              "error_code.count*100/percentage1.count::float as result "
              "from error_code,percentage1 "
              "where error_code.date=percentage1.date ) as result1"
              " where result >1;
```
___

### Python Script
Used Python[script](https://github.com/RevanthRedi/newsLogReport/blame/master/logDb.py) that connects to `PostgreSQL` DB and gets result
