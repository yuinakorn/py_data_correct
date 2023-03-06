import pymysql
from dotenv import dotenv_values

config_env = dotenv_values(".env")

connection = pymysql.connect(host=config_env['DB_HOST'],
                             user=config_env['DB_USER'],
                             password=config_env['DB_PASS'],
                             db=config_env['DB_NAME'],
                             charset='utf8mb4',
                             port=int(config_env["DB_PORT"]),
                             )
