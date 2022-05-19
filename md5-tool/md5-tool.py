import hashlib
import os
import argparse
import sys
import sqlite3
from sqlite3 import OperationalError
from sqlite3 import DatabaseError


class MD5Tool():

    def __init__(self, directory=None, db=None):
        self.db = db
        self.directory = directory

    def run(self):
        if self.db and self.directory:
            self.hash_directory(self.directory)

    def scan_and_delete(self, directory):
        '''
        Parse the given directory and compare all
        the files in it and remove the duplicates.
        '''
        md5_list = list()
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                file = os.path.join(root, name)
                md5 = hashlib.md5(open(file, 'rb').read()).hexdigest()
                if md5 in md5_list:
                    print("Deleting {}".format(file))
                    os.remove(file)
                else:
                    md5_list.append(md5)

    def hash_directory(self, directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                file = os.path.join(root, name)
                md5 = hashlib.md5(open(file, 'rb').read()).hexdigest()
                in_database = self.db.is_hash_in_table(md5)
                if in_database:
                    print("{} already in database. Skipping...".format(file))
                    continue
                else:
                    print("Adding {}".format(file))
                    self.db.add_row(file, md5)


class Database():

    def __init__(self, name):
        self.db = sqlite3.connect("{}".format(name))
        self.table = "hashes"
        self.cursor = self.db.cursor()
        self._create_hashes_table()

    def _create_hashes_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS "
                            "{}("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "file text,"
                            "hash text)"
                            .format(self.table))

    def add_row(self, file, md5):
        self.cursor.execute("INSERT INTO "
                            "{}("
                            "file,"
                            "hash) "
                            "VALUES (?, ?)"
                            .format(self.table),
                            ('{}'.format(file),
                             '{}'.format(md5)))
        self.commit()

    def is_hash_in_table(self, value):
        return self.column_contains(self.table, "hash", value)

    def is_file_in_table(self, value):
        return self.column_contains(self.table, "file", value)

    def column_contains(self, table, column, value):
        sql = "\
        SELECT CASE WHEN EXISTS(\
          SELECT {column}\
          FROM {table}\
          WHERE {column}= '{value}'\
        )\
        THEN CAST(True AS BIT)\
        ELSE CAST(False AS BIT)\
        END".format(column=column, table=table, value=value)

        for row in self.cursor.execute(sql):
            return True if row[0] == 1 else False

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("{} -h".format(sys.argv[0]))
        sys.exit(0)
    parser = argparse.ArgumentParser()
    parser.add_argument("-hd", "--hash-directory", help="Hash the contents of the given directory.")
    parser.add_argument("-d","--directory", help="The directory to scan through and parse for duplicates.", required=True)
    parser.add_argument("-db", "--database", help="Create the database with the given name.")
    parser.add_argument("-l", "--logging", help="Set the log level.")
    args = parser.parse_args()

    db = None

    try:
        if args.database:
            db = Database(args.database)

        tool = MD5Tool(args.directory, db)
        tool.run()
    except OperationalError as e:
        print("{}".format(e))
        sys.exit(0)
    except DatabaseError as e:
        print("{}".format(e))
        sys.exit(0)
    finally:
        if db:
            db.close()
