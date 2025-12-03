import mysql.connector
from mysql.connector import Error


class EtlUtil:
    def __init__(self):
        self.mysql_conn = self.create_mysql_connection()

    def create_mysql_connection(self):
        try:
            conn = mysql.connector.connect(
                host="hair-club-server-mgr.mysql.database.azure.com",
                user="tuahhxuiua",
                password="Mzs3$yUMMzdHsKnt",
                database="hairclubbr"
            )
            print("Connected")
            return conn
        except Error as e:
            raise Error(f"❌ Erro ao conectar ao Mysql: {e}")

    def extract(self, operation):
        cursor = self.mysql_conn.cursor(dictionary=True)
        cursor.execute(operation)
        rows = cursor.fetchall()
        return rows
