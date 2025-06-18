import os
from flask import Flask, request
import MySQLdb

app = Flask(__name__)
conn = ""

def get_db_conn():
    global conn
    if not conn or not conn.open:
        conn = MySQLdb.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME")
        )
    return conn

def db_init():
    global conn
    try:
        conn = MySQLdb.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME")
        )
        cur = conn.cursor()
        cur.execute("show tables like 'employee'")
        if not cur.rowcount:
            cur.execute("create table employee(id int, name varchar(20))")
            conn.commit()
        else:
            print("Database table already present")
    except Exception as msg:
        print("Exception while initializing database : %s" % msg)

@app.route('/')
def greet():
    return 'Valar Morghulis!!'

@app.route("/storedata", methods=["POST"])
def store_data():
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("insert into employee values (%s, '%s')" % (request.form['id'], request.form['name']))
        conn.commit()
        msg = "Inserted Data for Employee : %s" % (request.form['name'])
    except Exception as msg:
        print("Exception : %s" % msg)
        msg = "Exception while inserting data %s" % msg
    return msg

@app.route("/getdata/<int:id>", methods=["GET"])
def get_data(id):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("select * from employee where id=%d" % id)
        if cur.rowcount:
            res = cur.fetchone()
            msg = "Employee Details ID : %d  Name : %s" % (res[0], res[1])
        else:
            msg = "Data for Employee ID : %d not present" % id
    except Exception as msg:
        print("Exception : %s" % msg)
        msg = "Exception while fetching data %s" % msg
    return msg

if __name__ == '__main__':
    db_init()
    app.run(host="0.0.0.0", port=5000)
