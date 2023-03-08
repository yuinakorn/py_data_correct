from py_data_correct import database
import pymysql
from dotenv import dotenv_values

config_env = dotenv_values(".env")


# connection = database.connection


def person(hoscode, cid):
    global results
    connection = pymysql.connect(host=config_env['DB_HOST'],
                                 user=config_env['DB_USER'],
                                 password=config_env['DB_PASS'],
                                 db=config_env['DB_NAME'],
                                 charset='utf8mb4',
                                 port=int(config_env["DB_PORT"]),
                                 )
    if hoscode is not None or cid is not None:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT PID,TYPEAREA,concat('(',DISCHARGE,')',cdischarge.dischargedesc) AS dc_status,D_UPDATE " \
                      "FROM person INNER JOIN cdischarge on cdischarge.dischargecode = person.DISCHARGE " \
                      "WHERE HOSPCODE = '" + hoscode + "' AND CID = '" + cid + "'"
                cursor.execute(sql)
                rows = cursor.fetchall()
                results = []
                for row in rows:
                    result = {
                        'pid': row[0],
                        'typearea': row[1],
                        'dc_status': row[2],
                        'd_update': str(row[3]),
                    }
                    results.append(result)

                return results

        except Exception as e:
            print(e)
            print("Error: unable to fetch data")

    connection.close()
    return results
