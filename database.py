from mysql.connector import MySQLConnection,Error
from configparser import ConfigParser


class Database:
    """Database Related Operation

    Methods
    --------
        1.insert(data)
        2.read_db_config(filename, section)

    Objcet Creation
    --------------
        db=Database(table_name='crawler', fields=fields)

        Parameters:
        ----------
            table_name : name of table
            fields     : dictionary of field_name and their_type
            filename   : configuration filename
            section    : database section

    """

    def __init__(self, table_name=None, fields=None, filename='config.ini', section='mysql'):
        """
        Initialize the connection with the database and make the required table.
        :param table_name: name of the table to be inserted
        :param fields: a dictionary of field_name and their_type to be inserted in the table table_name
        :optional param filename: name of the configuration file
        :optional param section: section of database configuration
        """
        self.table_name = table_name
        db_config = self.read_db_config(filename, section)

        try :
            self.conn = MySQLConnection(**db_config)
        except Error as error:
            print(error)
            return

        self.cursor = self.conn.cursor()

        if table_name is not None and fields is not None:
            self.cursor.execute(f"show tables like '{self.table_name}'")
            output = self.cursor.fetchone()
            #if no such table exits create one
            if output is None:
                fields_list = (f'{k} {v}' for k, v in fields.items())
                self.cursor.execute(f"CREATE TABLE {self.table_name}({','.join(fields_list)})")
                print('Table successfully created')
                self.conn.commit()


    def insert(self, data):
        """
        This function is used to insert data into the table.
        :param data: dictonary contain the pair wise data {field_name:value}
        """

        values = list(data.values())
        s = ','.join('%s' for _ in data)
        if not values({s}):                                                        # Changed by
            insert_statement = f"INSERT INTO {self.table_name} values({s})"        # RoyCoding8
            self.cursor.execute(insert_statement, values)                          # 3 lines
        self.conn.commit()

    @staticmethod
    def read_db_config(filename,section):
        """
        Read database configuration from the file and return dictionary object
        :param filename: name of the configuration file
        :param section: section of database configuration
        :return: a dictionary of database parameters
        """

        parser = ConfigParser()
        parser.read(filename)

        db = {}
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception(f'{section} not found in the {filename} file')

        return db

    def __del__(self):
        self.cursor.close()
        self.conn.close()
