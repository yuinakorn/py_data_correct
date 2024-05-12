from dotenv import dotenv_values
import pymysql
from django.db import connection

config_env = dotenv_values(".env")

source_host = config_env['DB_HOST']
source_user = config_env['DB_USER']
source_password = config_env['DB_PASS']
source_db = config_env['DB_NAME']

#
# def get_connection():
#     # Connect to the source database
#     conn = pymysql.connect(host=source_host, user=source_user, password=source_password, db=source_db)
#     cursor = conn.cursor()
#
#     try:
#         conn.ping()
#         print("Connected to source database")
#     except Exception as e:
#         print(f"Error: {e}")
#
#     return conn, cursor


def person(cid):
    results = None
    print(f"cid: {cid}")
    if cid is not None:
        sql = """SELECT person.HOSPCODE,PID,TYPEAREA,concat('(',DISCHARGE,')',cdischarge.dischargedesc) AS dc_status,D_UPDATE 
              FROM person INNER JOIN cdischarge on cdischarge.dischargecode = person.DISCHARGE 
              WHERE CID = %s ORDER BY D_UPDATE DESC
              """
        with connection.cursor() as cursor:
            cursor.execute(sql, [cid])
            results = cursor.fetchall()

    # print(results)
    return results


def hoscode(hoscode):
    results = None
    if hoscode is not None:
        sql = "SELECT chospital.hoscode,chospital.hosname,chospital.hdc_regist,chospital.`status`, " \
              "chostype.hostypename,campur.ampurname,ctambon.tambonname " \
              "FROM chospital " \
              "INNER JOIN chostype ON chospital.hostype = chostype.hostypecode " \
              "INNER JOIN campur ON concat(chospital.provcode,chospital.distcode) = campur.ampurcodefull " \
              "INNER JOIN ctambon ON concat(chospital.provcode,chospital.distcode,chospital.subdistcode) = ctambon.tamboncodefull " \
              "WHERE hoscode = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, [hoscode])
            results = cursor.fetchall()

    return results


def provider(cid):
    results = None
    if cid is not None:
        sql = """SELECT provider.*, cprovidertype.providertype FROM provider
              INNER JOIN cprovidertype ON provider.PROVIDERTYPE = cprovidertype.id_providertype 
              WHERE cid = %s ORDER BY D_UPDATE DESC"""

        with connection.cursor() as cursor:
            cursor.execute(sql, cid)
            rows = cursor.fetchall()
            results = []
            for row in rows:
                columns = [column[0] for column in cursor.description]
                #  สร้าง dictionary ที่ key เป็นชื่อ column และ value เป็นข้อมูลในแต่ละ row
                result = dict(zip(columns, row))
                # เพิ่ม dictionary ที่สร้างขึ้นในขั้นตอนก่อนหน้านี้เข้าไปใน list results
                results.append(result)

    return results
