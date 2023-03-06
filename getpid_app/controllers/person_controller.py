from py_data_correct import database

connection = database.connection


def person(hoscode, cid):
    # global results

    if hoscode is not None or cid is not None:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT PID,TYPEAREA FROM person WHERE HOSPCODE = '" + hoscode + "' AND CID = '" + cid + "'"
                cursor.execute(sql)
                rows = cursor.fetchall()
                results = []
                for row in rows:
                    result = {
                        'pid': row[0],
                        'typearea': row[1],
                    }
                    results.append(result)

                return results

        except Exception as e:
            print(e)
            print("Error: unable to fetch data")

    return results
