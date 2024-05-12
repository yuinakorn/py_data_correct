from py_data_correct import database
import pymysql
from dotenv import dotenv_values
from django.db import connection

config_env = dotenv_values(".env")


# def query(sql):
#     connection = pymysql.connect(host=config_env['DB_HOST'],
#                                  user=config_env['DB_USER'],
#                                  password=config_env['DB_PASS'],
#                                  db=config_env['DB_NAME'],
#                                  charset='utf8mb4',
#                                  port=int(config_env["DB_PORT"]),
#                                  )
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(sql)
#             rows = cursor.fetchall()
#             results = []
#             # key is column name
#             for row in rows:
#                 columns = [column[0] for column in cursor.description]
#                 result = dict(zip(columns, row))
#                 results.append(result)
#
#                 # print(result)
#     except Exception as e:
#         print(e)
#         print("Error: unable to fetch data")
#
#     # print(results)
#     connection.close()
#     return results


def labor(cid):
    results = None
    if cid is not None:
        sql = "SELECT labor.PID,labor.GRAVIDA,labor.BDATE, " \
              "labor.LMP,labor.EDC,labor.BRESULT,labor.BPLACE,labor.BHOSP,labor.LBORN,labor.HOSPCODE,chospital.hosname " \
              "FROM labor " \
              "INNER JOIN person ON labor.hospcode = person.HOSPCODE AND labor.PID = person.PID " \
              "INNER JOIN chospital on labor.HOSPCODE = chospital.hoscode " \
              "WHERE person.CID = %s ORDER BY labor.HOSPCODE, labor.BDATE DESC"

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
