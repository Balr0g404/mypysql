#!/usr/bin/python3
#coding : utf-8

"""
Library based on mysql.connector to interact with mysql as simply as possible
You can easily perform pre-made querys, or create your custom querys using the
mysql.connector library with the database.cursor attribute
Dev : Balr0g404
"""

####### Class

import mysql.connector
import sys

class database():
    """Create a database object full of usefull methods"""

    def __init__(self, db_user, db_password, db_name, db_host="localhost"):
        """Create a database object with the following attributes:
           - name : the database's name
           - db : a mysql.connector database objectif allowing us to connect to mysql
           - cursor : a mysql.connector cursor
           - tables : list of all the table of the database
        """

        try:
            self.name = db_name
            self.db = mysql.connector.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)
            self.cursor = self.db.cursor()
            self.cursor.execute("SHOW TABLES")
            self.tables = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print("[+] This error occured while attempting to connect to the database : {}".format(err))
            sys.exit()

    def __repr__(self):
        """Print some infos about the database"""
        return "Database '{}' with {} tables.".format(self.name, len(self.tables))

    def help():
        """Print some help about the class"""
        pass

    def show_tables(self):
        """list all the tables from the database"""
        for table in self.tables:
            print(table)

    def select(self, select="*", fm=None, where=None, gb=None, having=None, ob=None, limit=None, show_query=False):
        """Perform a select query.
        """
        query_syntax = ["SELECT", "FROM", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT"]
        query_params = [select, fm, where, gb, having, ob, limit]
        query = ""
        for i in range(len(query_params)):
            if query_params[i] is not None:
                query += " {} {}".format(query_syntax[i], query_params[i])

        try:
            if show_query is True:
                print("[+] The executed query is \n {}".format(query))
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result

        except mysql.connector.Error as err:
            print("[+] This error occured while attempting to connect to the database : {}".format(err))
            return None

    def insert(self, table_name="", columns=(), values=[], show_query=False):
        """Perform an insert query"""

        #sql = "INSERT INTO {} {} VALUES ({}%s)".format(table_name, columns, "%s, "* (len(values[0])-1))
        sql = "INSERT INTO {} (".format(table_name)
        for column in columns:
            if column == columns[-1]:
                sql += column + ")"
            else:
                sql += column + ","
        sql += " VALUES ("
        for value in values[0]:
            if value == values[0][-1]:
                sql += "%s)"
            else:
                sql += "%s,"
        #print(sql)
        try:
            if len(values) == 1:
                val = values[0]
                if show_query==True:
                    print("[+] The python mysql.connector executed query is \n {}".format(sql))
                self.cursor.execute(sql,val)
                self.db.commit()
                print("[+] {} records inserted.".format(self.cursor.rowcount))

            elif len(values) > 1:
                if show_query==True:
                    print("[+] The python mysql.connector executed query is \n {}".format(sql))
                self.cursor.executemany(sql,values)
                self.db.commit()
                print("[+] {} records inserted.".format(self.cursor.rowcount))
            else:
                raise ValueError
        except mysql.connector.Error as err:
            print("[+] This error occured while attempting to connect to the database : {}".format(err))
        except ValueError as valerr:
            print("[+] You must give some values")



#### DEBUG
#I created a database called test and a table called customers with two row: name and adress, both varchar
if __name__ == '__main__':

    #db = database("YOUR USER","YOUR PASSWORD","YOUR DATABASE")
    columns = ("name","address")
    val = [("John", "Highway 21")]
    vals = [
  ('Peter', 'Lowstreet 4'),
  ('Amy', 'Apple st 652'),
  ('Hannah', 'Mountain 21'),
  ('Michael', 'Valley 345'),
  ('Sandy', 'Ocean blvd 2'),
  ('Betty', 'Green Grass 1'),
  ('Richard', 'Sky st 331'),
  ('Susan', 'One way 98'),
  ('Vicky', 'Yellow Garden 2'),
  ('Ben', 'Park Lane 38'),
  ('William', 'Central st 954'),
  ('Chuck', 'Main Road 989'),
  ('Viola', 'Sideway 1633')
]
    db.insert("customers", columns, vals, show_query=True)
    result = db.select(select="*", fm="customers")
    for row in result:
        print(row)
