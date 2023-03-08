from py_data_correct import database


# connection = database.connection


# not in use.
def query_ncd(sql):
    try:
        connection = database.connection
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            result = []
            # key is column name
            for row in rows:
                columns = [column[0] for column in cursor.description]
                result = dict(zip(columns, row))
                # print(result)

                return result

            return result
    except Exception as e:
        print(e)
        print("Error: unable to fetch data")


def ncd(cid):
    # global results1, results2, results3, results4, results5
    if cid is not None:
        results1 = None
        results2 = None
        results3 = None
        results4 = None
        results5 = None

        try:
            connection = database.connection
            with connection.cursor() as cursor:

                # chronic
                sql = "SELECT chronic.PID,CHRONIC,DATE_DIAG,chronic.HOSPCODE,chospital.hosname FROM chronic " \
                      "INNER JOIN person ON chronic.PID = person.PID and chronic.HOSPCODE = person.HOSPCODE " \
                      "INNER JOIN chospital on chronic.HOSPCODE = chospital.hoscode " \
                      "WHERE person.CID = '" + cid + "' ORDER BY chronic.HOSPCODE, chronic.DATE_DIAG DESC"

                # results1 = query_ncd(sql)
                cursor.execute(sql)
                rows = cursor.fetchall()
                results1 = []
                for row in rows:
                    result = {
                        'pid': row[0],
                        'chronic': row[1],
                        'date_diag': row[2],
                        'hospcode': row[3],
                        'hosname': row[4].replace('โรงพยาบาลส่งเสริมสุขภาพตำบล', 'รพ.สต.'),
                    }
                    results1.append(result)

                # diagnosis_opd ความดัน
                sql = "SELECT diagnosis_opd.PID,diagnosis_opd.SEQ,diagnosis_opd.DIAGCODE,diagnosis_opd.DATE_SERV,diagnosis_opd.HOSPCODE,chospital.hosname " \
                      "FROM diagnosis_opd " \
                      "INNER JOIN person on person.PID = diagnosis_opd.PID AND person.HOSPCODE = diagnosis_opd.HOSPCODE " \
                      "INNER JOIN chospital on diagnosis_opd.HOSPCODE = chospital.hoscode " \
                      "WHERE person.CID = '" + cid + "' and diagnosis_opd.DIAGCODE BETWEEN 'I10' and 'I159' " \
                                                     "ORDER BY diagnosis_opd.HOSPCODE, diagnosis_opd.DATE_SERV DESC"
                # results2 = query_ncd(sql)
                cursor.execute(sql)
                rows = cursor.fetchall()
                results2 = []
                for row in rows:
                    result = {
                        'pid': row[0],
                        'seq': row[1],
                        'diagcode': row[2],
                        'date_serv': row[3],
                        'hospcode': row[4],
                        'hosname': row[5].replace('โรงพยาบาลส่งเสริมสุขภาพตำบล', 'รพ.สต.'),
                    }
                    results2.append(result)

                # diagnosis_ipd ความดัน
                sql = "SELECT diagnosis_ipd.PID,diagnosis_ipd.AN,diagnosis_ipd.DIAGCODE,diagnosis_ipd.DATETIME_ADMIT, diagnosis_ipd.HOSPCODE,chospital.hosname " \
                      "FROM diagnosis_ipd " \
                      "INNER JOIN person on person.PID=diagnosis_ipd.PID AND person.HOSPCODE=diagnosis_ipd.HOSPCODE " \
                      "INNER JOIN chospital on diagnosis_ipd.HOSPCODE=chospital.hoscode " \
                      "WHERE person.CID='" + cid + "' AND diagnosis_ipd.DIAGCODE BETWEEN 'I10' AND 'I159' " \
                                                   "ORDER BY diagnosis_ipd.HOSPCODE"
                # results3 = query_ncd(sql)
                cursor.execute(sql)
                rows = cursor.fetchall()
                results3 = []
                for row in rows:
                    result = {
                        'pid': row[0],
                        'an': row[1],
                        'diagcode': row[2],
                        'datetime_admit': row[3],
                        'hospcode': row[4],
                        'hosname': row[5].replace('โรงพยาบาลส่งเสริมสุขภาพตำบล', 'รพ.สต.'),
                    }
                    results3.append(result)

                # diagnosis_opd เบาหวาน ผู้ป่วยนอก
                sql = "SELECT diagnosis_opd.PID,diagnosis_opd.SEQ,diagnosis_opd.DIAGCODE,diagnosis_opd.DATE_SERV,diagnosis_opd.HOSPCODE,chospital.hosname " \
                      "FROM diagnosis_opd " \
                      "INNER JOIN person on person.PID = diagnosis_opd.PID AND person.HOSPCODE = diagnosis_opd.HOSPCODE " \
                      "INNER JOIN chospital on diagnosis_opd.HOSPCODE = chospital.hoscode " \
                      "where person.CID = '" + cid + "' AND diagnosis_opd.DIAGCODE BETWEEN 'E10' AND 'E149' " \
                                                     "ORDER BY diagnosis_opd.HOSPCODE"
                # results4 = query_ncd(sql)

                cursor.execute(sql)
                rows = cursor.fetchall()
                results4 = []
                for row in rows:
                    result = {
                        'pid': row[0],
                        'seq': row[1],
                        'diagcode': row[2],
                        'date_serv': row[3],
                        'hospcode': row[4],
                        'hosname': row[5].replace('โรงพยาบาลส่งเสริมสุขภาพตำบล', 'รพ.สต.'),
                    }
                    results4.append(result)

                # diagnosis_opd เบาหวาน ผู้ป่วยใน
                sql = "SELECT diagnosis_ipd.PID,diagnosis_ipd.AN,diagnosis_ipd.DIAGCODE,diagnosis_ipd.DATETIME_ADMIT, diagnosis_ipd.HOSPCODE,chospital.hosname " \
                      "FROM diagnosis_ipd " \
                      "INNER JOIN person on person.PID = diagnosis_ipd.PID AND person.HOSPCODE = diagnosis_ipd.HOSPCODE " \
                      "INNER JOIN chospital on diagnosis_ipd.HOSPCODE = chospital.hoscode " \
                      "WHERE person.CID = '" + cid + "' and diagnosis_ipd.DIAGCODE BETWEEN 'E10' and 'E149' " \
                                                     "ORDER BY diagnosis_ipd.HOSPCODE"

                # results5 = query_ncd(sql)
                cursor.execute(sql)
                rows = cursor.fetchall()
                results5 = []
                for row in rows:
                    result = {
                        'pid': row[0],
                        'an': row[1],
                        'diagcode': row[2],
                        'datetime_admit': row[3],
                        'hospcode': row[4],
                        'hosname': row[5].replace('โรงพยาบาลส่งเสริมสุขภาพตำบล', 'รพ.สต.')
                    }
                    results5.append(result)

        except Exception as e:
            print(e)
            print("Error: unable to fetch data")

    # results1 = chronic
    # results2 = diagnosis_opd ความดัน ผู้ป่วยนอก
    # results3 = diagnosis_ipd ความดัน ผู้ป่วยใน
    # results4 = diagnosis_opd เบาหวาน ผู้ป่วยนอก
    # results5 = diagnosis_ipd เบาหวาน ผู้ป่วยใน

    results1 = results1 if results1 is not None else []
    results2 = results2 if results2 is not None else []
    results3 = results3 if results3 is not None else []
    results4 = results4 if results4 is not None else []
    results5 = results5 if results5 is not None else []
    context = {'results1': results1, 'results2': results2, 'results3': results3, 'results4': results4,
               'results5': results5}
    # print(context)
    return context
