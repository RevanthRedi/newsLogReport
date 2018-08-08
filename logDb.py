import psycopg2
'''
Run sql
'''
DBNAME ="news"

def get_posts():
    db=psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select path, count(path) from log group by path order by count desc limit 4;")
    logs= c.fetchall()
    print("******")
    print(type(logs))
    print(logs)
    db.close()
    return logs
