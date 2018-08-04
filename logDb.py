import psycopg2
'''
Run sql
'''
DBNAME ="news"

def get_posts():
    db=psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from log")
    logs= c.fetchall()
    db.close()
    return logs