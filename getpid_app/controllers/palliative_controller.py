from django.db import connection


def palliative(cid):
    results = None
    if cid is not None:
        sql = "SELECT * FROM tmp_pallitive WHERE cid = %s"

        with connection.cursor() as cursor:
            cursor.execute(sql, cid)
            rows = cursor.fetchall()
            results = []
            for row in rows:
                columns = [column[0] for column in cursor.description]
                result = dict(zip(columns, row))
                results.append(result)
    return results
