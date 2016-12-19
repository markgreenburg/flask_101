"""
CRUD models for our wiki app
"""
import mysql.connector
import config

class Page(object):
    """
    Object map for pages in the database
    """
    def __init__(self, page_id=0):
        if not isinstance(page_id, int):
            page_id = int(page_id)
        query = ('SELECT id, name, content, last_modified, modified_by'
                 'FROM page WHERE id=%d"' % page_id)
        # Query our db to see if this page ID exists
        result_set = Database.get_result(query, True)
        # If page exists, set Page attributes to what's in the db
        if result_set:
            self.page_id = page_id
            self.title = result_set[1]
            self.content = result_set[2]
            self.last_modified = result_set[3]
            self.modified_by = result_set[4]
        return

    def insert(self):
        """
        Inserts new page into wiki. Should not be called directly - instead,
        use the Page.save() method.
        """
        query = ("INSERT INTO page (title, content, last_modified, "
                 "modified_by, VALUES (\"%s\", \"%s\", \"%s\", \"%s\")" % \
                 (Database.escape(self.title), \
                  Database.escape(self.content),\
                  Database.escape(self.last_modified), \
                  Database.escape(self.modified_by)))
        return Database.do_query(query)

    def update(self):
        """
        Updates page in wiki. Should not be called directly - instead, use the
        Page.save() method.
        """
        query = ("UPDATE page set title = '%s', content = '%s', last_modified"
                 " = '%s', modified_by = '%s' WHERE id = %d" % \
                (Database.escape(self.title),\
                 Database.escape(self.content),\
                 Database.escape(self.last_modified),\
                 Database.escape(self.modified_by),\
                 self.page_id))
        return Database.do_query(query)

    def save(self):
        """
        Saves action to database by calling insert() or update() methods. If
        page already exists, will call update(), else will call insert().
        Returns the respective method calls.
        """
        if self.page_id > 0:
            return self.update()
        else:
            return self.insert()

    def delete(self):
        """
        Sets a page's status to 'deleted' so it won't show in the index. Page
        does not actually get destroyed.
        """
        query = "UPDATE page SET deleted = 1 WHERE id = %d" %(self.page_id)
        return Database.do_query(query)

    @staticmethod
    def get_pages():
        """
        Fetches all undeleted pages from the database. Returns all rows.
        """
        query = ("SELECT id, title, content, last_modified, modified_by FROM"
                 "page WHERE deleted = 0")
        return Database.get_result(query)


class Database(object):
    """
    Collection of static methods that setup our DB connection and create
    generalized methods for running queries / establish and release
    connections in mysql
    """
    @staticmethod
    def get_connection():
        """
        Sets up the mysql connection. Uses settings from the config file.
        """
        return mysql.connector.connect(
            user=config.user_name,
            password=config.password,
            host=config.host,
            database=config.database
        )

    @staticmethod
    def escape(value):
        """
        Escapes apostrophes in SQL
        """
        return value.replace("'", "''")

    @staticmethod
    def get_result(query, get_one=False):
        """
        Opens a connection to the db, executes a query, fetches results, and
        then closes the connection.
        Args: query to execute, get_one (false by default, default is fetchall)
        Returns: the fetchOne or fetchAll of the query
        """
        conx = Database.get_connection()
        cur = conx.cursor()
        conx.execute(query)
        if get_one:
            result_set = cur.fetchOne()
        else:
            result_set = cur.fetchAll()
        cur.close()
        conx.close()
        return result_set

    @staticmethod
    def do_query(query):
        """
        Takes care of opening and then closing our database connections. Also
        executes our SQL and auto-commits queries. Takes SQL query as arg and
        returns the lastrowid in case we need to insert it as foreign key
        elsewhere.
        """
        conx = Database.get_connection()
        cur = conx.cursor()
        cur.execute(query)
        conx.commit()
        last_id = cur.lastrowid
        cur.close()
        conx.close()
        return last_id
