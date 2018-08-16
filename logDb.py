import psycopg2

DB_NAME = "news"


def get_posts():
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(
        "select b.title, count(a.status) "
        "from title a join articles b "
        "on a.substring = b.slug "
        "group by a.substring, b.title "
        "order by count desc limit 3;")
    logs = c.fetchall()
    print("1. What are the most popular three articles of all time?")
    print("---------------------------------------------------------")
    for i in logs:
        print(str(i[0]) + '\t | \t ' + str(i[1]) + '\n')
    print('\n')
    db.close()
    return logs


def get_posts1():
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute("select distinct a.name, b.title "
              "from authors a inner join articles b on a.id = b.author "
              "right join top_3_authors c on b.title = c.title;")
    logs1 = c.fetchall()
    print("2. Who are the most popular article authors of all time?")
    print("---------------------------------------------------------")
    for j in logs1:
        print(str(j[0]) + '\t | \t' + str(j[1]) + '\n')
    print('\n')
    db.close()
    return logs1


def get_posts2():
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute("select * from ("
              "select error_code.date, "
              "error_code.count*100/percentage1.count::float as result "
              "from error_code,percentage1 "
              "where error_code.date=percentage1.date ) as result1"
              " where result >1;")
    logs2 = c.fetchall()
    print("3. On which days did more than 1% of requests lead to errors?")
    print("---------------------------------------------------------")
    for k in logs2:
        print(str(k[0]) + '\t | \t' + str(k[1]) + ' errors \n')
    print('\n')
    print(logs2)

    db.close()
    return logs2


def main():
    """
    Generates the report.
    """
    get_posts()
    get_posts1()
    get_posts2()


if __name__ == "__main__":
    main()

