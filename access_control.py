import sqlite3
import hashlib
from chinese_wall import ChineseWall


def encode_password(passwd):
    result = hashlib.md5(passwd.encode())
    return result.hexdigest()


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_companies():
    conn = get_db_connection()
    comps = conn.execute("SELECT * FROM companies").fetchall()
    conn.close()
    return comps


def is_valid_user(eid, passwd):
    conn = get_db_connection()
    spwd = conn.execute(
        f"SELECT emp_password FROM users WHERE emp_id = {eid};"
    ).fetchall()
    conn.close()
    if len(spwd) == 0:
        return False
    if encode_password(passwd) == spwd[0][0]:
        return True
    else:
        return False


def get_files():
    conn = get_db_connection()
    files = conn.execute("SELECT * FROM files").fetchall()
    conn.close()
    return files


def get_query_files(query):
    conn = get_db_connection()
    files = conn.execute(
        f"SELECT * FROM files WHERE file_name LIKE '%{query}%' or cd LIKE '%{query}%'"
    ).fetchall()
    conn.close()
    return files


CW = ChineseWall()
EST_USERS = {}


def establish_chinese_wall():
    comps = get_companies()
    for x in comps:
        CW.addCompany(x[0], x[1])

    files = get_files()
    for x in files:
        CW.addFile(x[0], CW.company_name_to_companyid[x[3]], x[2])


establish_chinese_wall()


def establish_new_user(eid):
    conn = get_db_connection()
    comps = conn.execute(
        f"SELECT emp_id, emp_role, companies FROM users WHERE emp_id = {eid}"
    ).fetchall()
    conn.close()

    if len(comps) == 0:
        print("No such user")
        return

    companies = comps[0][2].split(",")
    cwid = CW.addUser(comps[0][0], comps[0][1], companies)
    return cwid


def check_read_req(eid, path):
    if eid not in EST_USERS.keys():
        EST_USERS[eid] = establish_new_user(eid)
    return CW.requestRead(
        CW.users[EST_USERS[eid]], CW.files[CW.file_name_to_fileid[path]]
    )


def check_write_req(eid, path):
    if eid not in EST_USERS.keys():
        EST_USERS[eid] = establish_new_user(eid)
    return CW.requestWrite(
        CW.users[EST_USERS[eid]], CW.files[CW.file_name_to_fileid[path]]
    )
