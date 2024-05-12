# from django.db import connection


# def authenticate(request, username, password):
#     print(request)
#     results = None
#     if username is not None and password is not None:
#         sql = "SELECT * FROM sys_member WHERE username = %s AND password = md5(%s)"
#
#         with connection.cursor() as cursor:
#             cursor.execute(sql, (username, password))
#             rows = cursor.fetchall()
#             results = []
#             for row in rows:
#                 columns = [column[0] for column in cursor.description]
#                 result = dict(zip(columns, row))
#                 results.append(result)
#     return results
