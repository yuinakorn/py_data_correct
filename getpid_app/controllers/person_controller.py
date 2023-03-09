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
    if cid is not None:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT person.HOSPCODE,PID,TYPEAREA,concat('(',DISCHARGE,')',cdischarge.dischargedesc) AS dc_status,D_UPDATE " \
                      "FROM person INNER JOIN cdischarge on cdischarge.dischargecode = person.DISCHARGE " \
                      "WHERE CID = '" + cid + "' ORDER BY D_UPDATE DESC"
                cursor.execute(sql)
                rows = cursor.fetchall()
                results = []
                for row in rows:
                    result = {
                        'hoscode': row[0],
                        'pid': row[1],
                        'typearea': row[2],
                        'dc_status': row[3],
                        'd_update': str(row[4]),
                    }
                    results.append(result)

                return results

        except Exception as e:
            print(e)
            print("Error: unable to fetch data")

    connection.close()
    return results
