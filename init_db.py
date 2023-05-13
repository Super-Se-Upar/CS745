import sqlite3
import os

os.remove("database.db")
connection = sqlite3.connect("database.db")


with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open("companies.txt") as t:
    for x in t.readlines():
        x = x.split(",")
        cur.execute(
            "INSERT INTO companies (comp_name, coi) VALUES (?, ?)",
            (x[0], x[1]),
        )

with open("users.txt") as t:
    for x in t.readlines():
        x = x.split(",")
        companies = x[3:]
        p = str.lstrip(str.rstrip(",".join(companies)))
        cur.execute(
            "INSERT INTO users (emp_id, emp_password, emp_role, companies) VALUES (?, ?, ?, ?)",
            (x[0], x[1], x[2], p),
        )


with open("files.txt") as t:
    for x in t.readlines():
        x = x.split(",")
        cont = str(open("files/" + x[0]).read())
        x[1] = str.lstrip(str.rstrip(x[1]))
        cur.execute(
            "INSERT INTO files (file_name, file_cont, sanitized, cd) VALUES (?, ?, ?, ?)",
            (x[0], cont, False, x[1]),
        )
connection.commit()
connection.close()
