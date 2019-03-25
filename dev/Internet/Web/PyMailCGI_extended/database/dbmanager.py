import sqlite3


class DataBaseManager:
    def __init__(self, db_path):
        self.path = db_path
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def login(self):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        self.connection, self.cursor = connection, cursor
        return connection, cursor

    def close(self):
        self.cursor.close()
        self.connection.close()

    def __fetch_generator(self):
        while True:
            record = self.cursor.fetchone()
            if not record: break
            yield record

    def fields(self, table):
        self.do_safe_query("SELECT * FROM {0}".format(table))
        return [name for name, *_ in self.cursor.description]

    def do_safe_query(self, query, values=''):
        try:
            self.cursor.execute(query, values)
        except sqlite3.DatabaseError as exc:
            print("Error at exec query [{}]:\n\t{}".format(query, exc))
            raise
        else:
            if self.cursor.rowcount > 0:
                self.connection.commit()
            return self.cursor

    def search(self, table, field_names, comp_field, comp_value, relation):
        if isinstance(field_names, (list, tuple, set)):
            field_names = ', '.join(field_names)
        query = 'SELECT {1} FROM {0}'.format(table, field_names)
        if comp_field and comp_value:
            if comp_value != "NULL": comp_value = "\"{}\"".format(comp_value)
            relation = relation or '='
            query = '{0} WHERE {1} {3} {2}'.format(query, comp_field, comp_value, relation)
        return self.do_safe_query(query)

    def dump(self, table, fields, values):
        query = "INSERT INTO {0}{1} VALUES ({2})".format(table, fields, ', '.join('?' for _ in values))
        self.do_safe_query(query, values)

    def update(self, table, field, new_value, comp_filed, comp_value, relation='='):
        if comp_value != "NULL":
            comp_value = "\"{}\"".format(comp_value)
        if new_value != "NULL":
            new_value = "\"{}\"".format(new_value)
        query = 'UPDATE {0} SET {1} = {2} WHERE {3} {5} {4}'.format(table, field, new_value,
                                                                    comp_filed, comp_value, relation)
        self.do_safe_query(query)

    def contains(self, table, comp_field, comp_value):
        self.search(table, 'rowid', comp_field, comp_value, '=')
        return bool(self.cursor.fetchone())

    def fetch_one(self, table, field_names, comp_field, comp_value, relation=None):
        self.search(table, field_names, comp_field, comp_value, relation)
        return self.cursor.fetchone()

    def fetch_one_dictionary(self, table, field_names, comp_field, comp_value, relation=None):
        return {field: data for (field, data) in
                zip(field_names if isinstance(field_names, (list, tuple, set)) else (field_names, ),
                    self.fetch_one(table, field_names, comp_field, comp_value, relation))}

    def fetch_some(self, table, field_names, comp_field=None, comp_value=None, relation=None):
        self.search(table, field_names, comp_field, comp_value, relation)
        return self.__fetch_generator()

    def fetch_some_dictionary(self, table, field_names, comp_field=None, comp_value=None, relation=None):
        return (
            {field: data for (field, data) in zip(field_names, row)}
            for row in self.fetch_some(table, field_names, comp_field, comp_value, relation)
        )

    def fetch_all(self, table):
        return self.fetch_some(table, '*', None, None)

    def fetch_all_dictionary(self, table):
        fields = self.fields(table)
        return (
            {field: data for (field, data) in zip(fields, row)}
            for row in self.fetch_all(table)
        )


# if __name__ == "__main__":
#     with DataBaseManager('database.sqlite3') as dbm:
        # dbm.update('test_table', 'passwd', "aspirin", 'passwd', 'NULL', 'is')
        # dbm.update('test_table', 'passwd', "NULL", 'passwd', 'aspirin')
        # print(dbm.fetch_one_dictionary('test_table', 'passwd', 'passwd', "NULL", 'is'))
        # dbm.dump('test_table', '', (655, 'frank', 'punch'))
        # print(dbm.fields('test_table'))
        # print(dbm.contains('test_table', 'login', 'bob'))
        # print(dbm.contains('test_table', 'id', 555))
        # print(dbm.fetch_one('users', 'user_passwd', 'user_name', 'burkovski'))
        # print(dbm.fetch_one_dictionary('users', 'user_passwd', 'user_name', 'burkovski'))
        # print(list(dbm.fetch_some('test_table', ('id', 'login'), 'login', 'bob')))
        # print(list(dbm.fetch_some_dictionary('test_table', ('id', 'login'), 'login', 'bob')))
        # print(list(dbm.fetch_all('test_table')))
        # print(dbm.fetch_all_dictionary('test_table'))
