import os

import mysql.connector
import configparser

class MariaDBConnect:

    def createConnection(self):

        # Create a configparser object and read the configuration file
        config = configparser.ConfigParser()
        config.read('./connection.ini')

        # Read name-value pairs from the 'Database' section
        host = config.get('Database', 'host')
        port = config.getint('Database', 'port')
        user = config.get('Database', 'username')
        # Prefer the DB_PASSWORD environment variable so the real password
        # never has to live in connection.ini or in source control.
        password = os.environ.get('DB_PASSWORD') or config.get('Database', 'password')
        database = config.get('Database', 'database')

        # Create a connection to the MariaDB server
        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )

            if conn.is_connected():
                print("Connected to MariaDB on remote server")
                
        except mysql.connector.Error as e:
            print(f"Error connecting to MariaDB: {e}")

        return conn

