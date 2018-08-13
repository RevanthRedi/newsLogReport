import psycopg2
'''

Created Views for the following
1. create view percentage1 as select count(status),date(time) from log   group by date(time);
2. create view error_code as SELECT count(status), date(time) from log where status != '200 OK' group by date(time);
'''
DBNAME ="news"

def get_posts():
    db=psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select path, count(path) from log group by path order by count desc limit 4 offset 1;")
    logs= c.fetchall()
    print("******")
    print(type(logs))
    # logs.
    print(logs)

    db.close()
    return logs

def get_posts1():
    db = psycopg2.connect(database = DBNAME)
    c= db.cursor()
    c.execute("select distinct a.name, b.title from authors a inner join articles b on a.id = b.author right join toptitle c on b.slug = c.title;")
    logs1 = c.fetchall()
    print(type(logs1))
    print(logs1)

    db.close()
    return logs1

def get_posts2():
    db = psycopg2.connect(database = DBNAME)
    c = db.cursor()
    c.execute("select * from (select error_code.date, error_code.count*100/percentage1.count::float as result from error_code,percentage1 where error_code.date=percentage1.date ) as result1 where result >1;")
    logs2 = c.fetchall()
    print(logs2)

    db.close()
    return logs2