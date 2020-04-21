import os
import json
import ast
import mysql.connector

quotes = "'"


def loaddb(path, files):
    mydb = {}
    abs_path = os.popen('echo ~/parser/.aws.txt').read().strip()
    with open(abs_path) as file:
        for line in file:
            name, val = line.partition("=")[::2]
            mydb[name] = val.strip()

    cnx, cursor = establish_connection(mydb)
    # print(files)

    newdic = {}
    for file in files[1:]:
        file = path + file + '.txt'
        print("Uploading file " + file)
        with open(file, 'r') as f:
            newdic = ast.literal_eval(f.read())

        for item in (newdic['tweets']):
            text = item['text'].replace('\n', ' ').replace('\r', ' ')

            try:
                insert_kwargs(cursor, "webapp_tweets", text=text, year=item['created_at'])
                cnx.commit()
            except:
                continue

            if item['hashtag']:
                # a = "SELECT id FROM webapp_tweets WHERE text = {}".format(quotes + text + quotes)
                id = cursor.lastrowid
                insert_kwargs(cursor, "webapp_tags", id=str(id), hashtag=' '.join(item['hashtag']))
                cnx.commit()
        newdic.clear()
    cnx.close()


def establish_connection(dict):
    cnx = mysql.connector.connect(
        host=dict['RDS_HOSTNAME'],
        user=dict['RDS_USERNAME'],
        passwd=dict['RDS_PASSWORD'],
        database=dict['RDS_DB_NAME'],
    )
    cursor = cnx.cursor(buffered=True)
    return (cnx, cursor)


def insert_kwargs(cursor, db_table, **kwargs):
    """
    add a record to the database, using keyword arguments
        i.e. insert(cursor, name="john", emp_id=12039,...)
    """
    params = []
    valuestrs = []
    for k, v in kwargs.items():
        # ensure this is a key in database...
        # ...
        params.append(k)
        valuestrs.append(quotes + v + quotes)
    params = ', '.join(params)
    valuestrs = ', '.join(valuestrs)

    statement = "INSERT INTO {db} ({p}) VALUES ({v})".format(
        db=db_table, p=params, v=valuestrs
    )
    # print(statement)
    cursor.execute(statement)

