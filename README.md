In-order to run this program we need a PC with Python3 installed and Virtual Box

### Install Python3
Python2 comes preinstalled wiht MAC's and Linux PC. To run this program we need Python3. Python3 can be installed from this [link](https://www.python.org/downloads/)

### Setup
1. install git from this [link][https://git-scm.com/book/en/v2/Getting-Started-Installing-Git]
2. Windows users are recomended to use **git Bash** which comes with git
3. [Install virtual box from here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
4. [Download Vagrant here](https://www.vagrantup.com/downloads.html)
5. Download VM configuration from [here](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) or fork and clone it using this [github link](https://github.com/udacity/fullstack-nanodegree-vm) 

*_Following content taken from Udacity course_*
Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory

##### Start the virtual machine
From your terminal, inside the vagrant subdirectory, run the command ```vagrant up```. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When vagrant up is finished running, you will get your shell prompt back. At this point, you can run ```vagrant ssh``` to log in to your newly installed Linux VM!

Logged in!
If you are now looking at a shell prompt that starts with the word vagrant (as in the above screenshot), congratulations — you've gotten logged into your Linux VM.

If not, take a look at the Troubleshooting section below.

The files for this course
Inside the VM, change directory to ```/vagrant``` and look around with ls.

The files you see here are the same as the ones in the vagrant subdirectory on your computer (where you started Vagrant from). Any file you create in one will be automatically shared to the other. This means that you can edit code in your favorite text editor, and run it inside the VM.

Files in the VM's /vagrant directory are shared with the vagrant folder on your computer. But other data inside the VM is not. For instance, the PostgreSQL database itself lives only inside the VM.

##### Running the database
The PostgreSQL database server will automatically be started inside the VM. You can use the psql command-line tool to access it and run SQL statements:

Running `psql`, the PostgreSQL command interface, inside the VM.

Logging out and in
If you type exit (or Ctrl-D) at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're in the same directory and type vagrant ssh again.

If you reboot your computer, you will need to run vagrant up to restart the VM.

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
create view title as select "substring"(log.path, 10), status, id, time from log;

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
create view top_3_articles as select b.title, count(a.status) from title a join articles b on a.substring = b.slug group by a.substring, b.title order by count desc limit 3;

  SELECT b.title,                                   +
     count(a.status) AS count                       +
    FROM (title a                                   +
      JOIN articles b ON ((a."substring" = b.slogDb.pylug)))+
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
create view percentage1 as select count(status),date(time) from log   group by date(time);

  SELECT count(log.status) AS count,+
     date(log."time") AS date       +
    FROM log                        +
   GROUP BY (date(log."time"));
```
_Created view **error_code** to get number of requests resulted in error on a day_
```
create view error_code as SELECT count(status), date(time) from log where status != '200 OK' group by date(time);

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

### Running Program
1. SSH to vagrant
2. Run Python [script](https://github.com/RevanthRedi/newsLogReport/blob/master/logDb.py) that connects to `PostgreSQL` DB and gets result
Result will be displayed in terminal similar to [this](https://github.com/RevanthRedi/newsLogReport/blob/master/result.png)
